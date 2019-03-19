import '../../../node_modules/react-vis/dist/style.css';
import {groupBy} from 'lodash'
import * as React from 'react';
import {XAxis, YAxis, XYPlot, MarkSeries, LineSeries, LineMarkSeries} from 'react-vis';

import {DatasetRow} from "../../types/DatasetRow";
import {style} from "./style";

interface ChartProps {
  data: Array<DatasetRow>,
  isCompact: boolean;
}

interface ChartState {
  showOutlierData: boolean;
  showOutliers: boolean;
  showMarks: boolean;
}

export class Chart extends React.Component<ChartProps, ChartState> {
  state = {
    showOutlierData: false,
    showOutliers: false,
    showMarks: false,
  };

  getChartLength = () => {
    const width = window.innerWidth * this.props.data.length / 20;
    return this.props.isCompact
      ? window.innerWidth - 20
      : width < window.innerWidth
        ? window.innerWidth
        : width;
  };

  prepareData = (data, xKey) => data.map((row : any) => ({
      x: row[xKey],
      y: row.value,
      color: this.state.showOutliers ? (row.is_outlier ? 'red' : '#ddd') : row.label,
      size: 3
    }));

  renderChart = (data) => {
    const colorProp = this.state.showOutliers ? {
      colorType: "literal"
    } : {
      colorRange: ['red', 'blue']
    };

    return (
      <div style={style.chart}>
        {this.renderSummary(data)}
        <XYPlot height={window.innerHeight - 150} width={this.getChartLength() - 300} {...colorProp}>
          <XAxis tickLabelAngle={-45} tickFormat={v => v.toExponential()}/>
          <YAxis tickFormat={v => v.toExponential()}/>
          {this.state.showOutlierData
            ? <MarkSeries data={data} sizeRange={[3, 3]}/>
            : !this.state.showMarks
              ? <LineMarkSeries lineStyle={{stroke:"cornflowerblue"}} data={data} style={{strokeLinejoin: "round"}}  sizeRange={[3, 3]} strokeWidth={1}/>
              : <MarkSeries data={data} sizeRange={[3, 3]}/>
          }
        </XYPlot>
      </div>
    );
  }

  renderSummary = (data) => {
    const groupedData = groupBy(data, 'color');

    return (
      <div style={style.summary}>
        <button onClick={() => this.setState(state => ({showMarks: !state.showMarks}))}>
          {this.state.showMarks ? 'Line' : 'Marks'}
        </button>
        <button
          style={{background: this.state.showOutliers ? 'cornflowerblue' : ''}}
          onClick={() => this.setState(state => ({showOutliers: !state.showOutliers}))}>
          Outliers
        </button>
        <button
          style={{background: this.state.showOutlierData ? 'cornflowerblue' : ''}}
          onClick={() => this.setState(state => ({showOutlierData: !state.showOutlierData}))}>
          Features
        </button>
        {this.state.showOutliers && <ul style={{listStyle: 'none'}}>
          {Object.keys(groupedData)
            .map(color =>
              <li> <div style={{...style.colorBlock, background: color}} />{groupedData[color].length}</li>)}
        </ul>}
      </div>
    )
  };

  renderNoData = () => (
    <div style={style.noData}>
      No data found for collection
    </div>
  );

  render() {
    const data = this.prepareData(this.props.data, this.state.showOutlierData ? 'day' : 'timestamp');
    console.log(data);

    return (
      <React.Fragment>
        {this.props.data.length > 0
          ? this.renderChart(data)
          : this.renderNoData()
        }
      </React.Fragment>
    )
  }
}