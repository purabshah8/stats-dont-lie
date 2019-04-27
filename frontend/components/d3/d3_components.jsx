import React from 'react';
import * as d3 from "d3";

function Chart(props) {
    return <svg width={props.width} height={props.height}>
              <g transform={`translate(${props.paddingLeft}, ${props.paddingTop})`}>
              </g>
          </svg>;
}

function Axis(props) {
    function draw(chart, {className, generator, width, height, orientation, data }) {
        const h = orientation === "x" ? 0 : height;
        const w = orientation === "y" ? 0 : width;
        const axis = d3.scaleLinear()
            .domain([d3.min(data), d3.max(data)])
            .range([h, w]);
    }
    return;
}



const D3Components = {
    Chart,
};

export default D3Components;