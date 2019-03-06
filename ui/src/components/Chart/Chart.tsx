import {sortBy} from 'lodash';
import * as React from 'react';
import {Area, CartesianGrid, Line, XAxis, YAxis, Tooltip, ComposedChart} from 'recharts';

import {DatasetRow} from "../../types/DatasetRow";
import {style} from "./style";

interface CharProps {
  data: Array<DatasetRow>,
  isCompact: boolean;
}

export class Chart extends React.Component<CharProps> {

  prepareData = () => sortBy(this.props.data, 'timestamp').map((row: any) => {
      const date = new Date(row.date);
      const name = `${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`;
      return {
        name,
        value: row.value,
        is_outlier: row.is_outlier,
        centroid_value: row.centroid_value
      }
    });

  renderDot = ({cx, cy, payload}: any) => {
     let dot = {stroke: '#8884d8', fill: 'white'};

     if(payload.is_outlier) {
       dot = {stroke: 'red', fill: 'red'};
     }

    return (
      <circle
        key={payload.key}
        r="3"
        fill="white"
        strokeWidth="1"
        width="1056"
        height="738.1818181818181"
        cx={cx}
        cy={cy}
        {...dot}
      >
      </circle>
    )
  };

  renderChart = (data: any) => {
    const width = window.innerWidth * data.length / 20;
    const selectedWidth = this.props.isCompact
      ? window.innerWidth - 20
      : width < window.innerWidth
        ? window.innerWidth
        : width;

    return (
      <ComposedChart
        stackOffset="wiggle"
        style={{fontSize: '11px'}}
        width={selectedWidth}
        height={window.innerHeight / 1.1}
        margin={{top: 90}}
        data={data}
      >
        <Line type="monotone" dataKey="value" stroke="#8884d8" dot={this.renderDot} />
        <Line type="monotone" dataKey="centroid_value" stroke="red" dot={false} />
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5"/>
        <XAxis dataKey="name"/>
        <YAxis/>
        <Tooltip/>
      </ComposedChart>
    )
  };

  renderNoData = () => (
    <div style={style.noData}>
      No data found for collection
    </div>
  )

  render() {
    const data = this.prepareData();
    return (
      <React.Fragment>
        {data.length > 0
          ? this.renderChart(data)
          : this.renderNoData()
        }
      </React.Fragment>
    )
  }
}