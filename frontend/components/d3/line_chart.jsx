import React from 'react';
import * as d3 from 'd3';
import D3Components from "./d3_components";

export default class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this.data = this.props.stats[0]["fgPct"];
    }

    componentDidMount() {
        const width = 800;
        const height = 600;

        const chart = d3.select(this.chartRef);
            // .attr("width", width+100)
            // .attr("height", height+100)
            // .append("g")
            // .attr("transform", "translate(100,10)");

        const x = d3.scaleLinear()
            .domain([1,82])
            .range([0, width]);
        chart.append("g")
            .call(d3.axisBottom(x));

        const y = d3.scaleLinear()
            .domain([0,1])
            .range([height, 0]);
        chart.append("g")
            .call(d3.axisLeft(y));

        const graph = d3.selectAll("dot")
            .data(this.data)
            .enter()
            .append("circle")
                .attr("cx", (d,i) => (i+1))
                .attr("cy", (d,i) => d)
                .attr("r", 10)
                .attr("fill", "#000000");
    }
    

    render() {
        return (
            <div className="chart">
                <D3Components.Chart ref={r => (this.chartRef = r)} width={1280} 
                    height={1024} paddingLeft={64} paddingTop={16}>
                </D3Components.Chart>
            </div>
        );
    }
}
