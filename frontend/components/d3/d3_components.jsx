import React from 'react';
import * as d3 from "d3";

export class Chart extends React.Component {
  render() {
    return (
      <svg></svg>
    );
  }
}


// function Chart({width, height, paddingLeft, paddingTop}) {
//     return <svg width={width} height={height}>
//               <g transform={`translate(${paddingLeft}, ${paddingTop})`}>
//               </g>
//           </svg>;
// }

function Axis({ chart, className, generator, width, height, orientation, data, direction }) {
        const h = orientation === "x" ? 0 : height;
        const w = orientation === "y" ? 0 : width;
        const axis = d3.scaleLinear()
            .domain([d3.min(data), d3.max(data)])
            .range([h, w]);
        chart.append("g")
            .call(d3.axisLeft(axis));
    return;
}



const D3Components = {
    Chart,
    Axis,
};

export default D3Components;