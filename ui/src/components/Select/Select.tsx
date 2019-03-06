import {keyBy} from 'lodash';
import * as React from 'react';
import {style} from "./style";

export interface Option {
  key: string,
  value: any
}

interface SelectProps {
  data: Array<Option>
  onChange: (selected: Option) => void;
  selected: Option;
  disabled?: boolean;
}

export class Select extends React.Component<SelectProps> {
  onChange = (e: any) => {
    const value = e.target.value;
    const selected = keyBy(this.props.data, 'value')[value];
    this.props.onChange(selected);
  };

  render() {
    return (
      <select onChange={this.onChange} style={style.select} disabled={this.props.disabled}>
        <option selected={this.props.selected.key == null} disabled={true}>Select</option>
        {this.props.data.map((el, key) =>
          <option
            selected={this.props.selected.key == el.key}
            key={`${el.value}_${key}`}
            value={el.value}>{el.key}</option>
        )}
      </select>
    );
  }
}