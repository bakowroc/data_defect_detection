import { groupBy } from 'lodash';
import axios from 'axios';
import {uniq} from 'lodash';
import * as React from 'react';
import {Chart} from "../Chart/Chart";
import {DatasetRow} from "../../types/DatasetRow";
import {Operator} from "../../types/Operator";
import {Select, Option} from "../Select/Select";
import {DatasetMapRow} from "../../types/DatasetMapRow";
import {style} from "./style";
import {KpiDefinition} from "../../types/KpiDefinition";

interface AppState {
  data: Array<DatasetRow>;
  operators: Array<Option>;
  kpiNames: Array<Option>;
  acronyms: Array<Option>;
  kpiDefinition: KpiDefinition;
  dataset_keys: Array<DatasetMapRow>;
  selected: {
    operator: Option;
    acronym: Option;
    kpiName: Option;
    feature: Option;
    method: Option;
  },
  isChartCompact: boolean;
  isCalculating: boolean;
}

export class App extends React.Component<{}, AppState> {
  state: AppState = {
    data: [],
    kpiDefinition: {} as KpiDefinition,
    dataset_keys: [],
    operators: [],
    kpiNames: [],
    acronyms: [],
    selected: {
      operator: {key: null, value: null},
      acronym: {key: null, value: null},
      kpiName: {key: null, value: null},
      feature: {key: null, value: null},
      method: {key: null, value: null}
    },
    isChartCompact: true,
    isCalculating: false
  };

  static replaceVerticalScrollByHorizontal(event: any) {
    if (event.deltaY != 0) {
      window.scroll(window.scrollX + event.deltaY * 3, window.scrollY);

      event.preventDefault();
    }
    return;
  }

  async componentDidMount() {
    window.addEventListener('wheel', App.replaceVerticalScrollByHorizontal);

    try {
      const response = await axios.get('/api/operators');
      const operators: Array<Operator> = response.data.filter(operator => operator.has_enough);
      this.setState(state => ({
        ...state,
        operators: this.prepareOptions(operators, 'operator_name', 'operator_id')
      }));
    } catch (e) {
      console.log(e);
    }
  };

  prepareOptions = (data: Array<any>, key: string = null, value: string = null): Array<Option> => {
    if(key != null || value != null) {
      return data.map(e => ({key: `${e[key]}_${e[value]}`, value: e[value]}));
    }

    return data.map(e => ({key: e, value: e}));
  };


  onOperatorSelect = (selected: Option) => {
    this.setState(state => ({
      selected: {
        ...state.selected,
        operator: selected,
        acronym: {key: null, value: null},
        kpiName: {key: null, value: null}
      }}), async () => {
      try {
        const response = await axios.get(`/api/dataset_keys?operator_id=${this.state.selected.operator.value}`);
        const dataset_keys: Array<DatasetMapRow> = response.data.filter(dsk => dsk.has_enough === true);
        const acronyms: Array<Option> = this.prepareOptions(uniq(dataset_keys.map(dataset => dataset.acronym)));

        this.setState(state => ({ ...state, dataset_keys, acronyms}))
      } catch (e) {
        console.log(e);
      }
    });
  };

  onAcronymSelect = (selected: Option) =>
    this.setState(state => ({
      selected: {
        ...state.selected,
        acronym: selected,
        kpiName: {key: null, value: null}
      }}), () => {
      const dataSetsForKpi: Array<DatasetMapRow> = groupBy(this.state.dataset_keys, 'acronym')[this.state.selected.acronym.value];
      const kpiNames: Array<Option> = this.prepareOptions(uniq(dataSetsForKpi.map(dataset => dataset.kpi_name)));
      this.setState(state => ({ ...state, kpiNames}))
    });

  onKpiNameSelect = (selected: Option) =>
    this.setState(state => ({
      selected: {
        ...state.selected,
        kpiName: selected
      }}), async () => {
      try {
        const operator_id = this.state.selected.operator.value;
        const acronym = this.state.selected.acronym.value;
        const kpiName = this.state.selected.kpiName.value;
        const url = `/api/datasets?operator_id=${operator_id}&acronym=${acronym}&kpi_name=${kpiName}`;
        const dataResponse = await axios.get(url);
        const data: Array<DatasetRow> = dataResponse.data;

        const kpiDefinitionResponse = await axios.get(`/api/kpi_definitions?kpi_name=${kpiName}`);
        const kpiDefinition = kpiDefinitionResponse.data;

        this.setState({data, kpiDefinition})
      } catch (e) {
         console.log(e)
       }
    });

  calculateOutliers = async () => {
    try {
      this.setState({isCalculating: true});
      const operator_id = this.state.selected.operator.value;
      const acronym = this.state.selected.acronym.value;
      const kpiName = this.state.selected.kpiName.value;
      const feature = this.state.selected.feature.value;
      const method = this.state.selected.method.value;
      const url = `/api/outliers?operator_id=${operator_id}&acronym=${acronym}&kpi_name=${kpiName}&method=${method}&feature=${feature}`;
      const response = await axios.get(url);
      const dataWithOutliers = response.data;

      this.setState({data: dataWithOutliers})
    } catch (e) {
      console.log(e)
    }

    this.setState({isCalculating: false});
  };

  onCompactChange = () => this.setState(state => ({isChartCompact: !state.isChartCompact}));

  render() {
    return (
      <React.Fragment>
        {this.state.isCalculating && <div style={style.loading}><span style={style.spinner}>Calculating</span></div>}
       <div style={style.selectors}>
         <Select
           data={this.state.operators}
           onChange={this.onOperatorSelect}
           selected={this.state.selected.operator}
         />

         <Select
           data={this.state.acronyms}
           onChange={this.onAcronymSelect}
           selected={this.state.selected.acronym}
           disabled={this.state.acronyms.length === 0}
         />

         <Select
           data={this.state.kpiNames}
           onChange={this.onKpiNameSelect}
           selected={this.state.selected.kpiName}
           disabled={this.state.kpiNames.length === 0}
         />

         <Select
           data={[
             {key: 'sim', value: 'sim'},
             {key: 'dist', value: 'dist'},
             {key: 'reg', value: 'reg'},
             ]}
           onChange={(selected) => this.setState(state => ({
             selected: {
               ...state.selected,
               method: selected
             }}))}
           selected={this.state.selected.method}
           disabled={this.state.kpiNames.length === 0}
         />

         <Select
           data={[
             {key: 'day', value: 'day'},
             {key: 'weekday', value: 'weekday'},
             {key: 'monthday', value: 'monthday'},
             {key: 'timestamp', value: 'timestamp'}
           ]}
           onChange={(selected) => this.setState(state => ({
             selected: {
               ...state.selected,
               feature: selected
           }}))}
           selected={this.state.selected.feature}
           disabled={this.state.kpiNames.length === 0}
         />

          <input checked={this.state.isChartCompact} type="checkbox" onChange={this.onCompactChange} />
         {this.state.selected.feature.value !== null
            && this.state.selected.method.value !== null
            && <button onClick={this.calculateOutliers}>Find outliers</button> }

         {this.state.kpiDefinition.id > 0 &&
         <div style={style.definition}>
            <p style={style.p}>Description: {this.state.kpiDefinition.description}</p>
            <p style={style.p}>Unit: {this.state.kpiDefinition.unit}</p>
            <p style={style.p}>Tags: {this.state.kpiDefinition.tags}</p>
         </div>
         }
       </div>


        <Chart data={this.state.data} isCompact={this.state.isChartCompact}/>
      </React.Fragment>
    );
  }
}