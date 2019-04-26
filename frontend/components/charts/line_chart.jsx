import React from 'react';
import * as d3 from 'd3';

export default class LineChart extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        const width = 500;
        const height = 750;

        const chart = d3.select(this.chartRef)
            .attr("width", width+100)
            .attr("height", height+100)
            .append("g")
            .attr("transform", "translate(100,0)");

        const x = d3.scaleLinear()
            .domain([1,82])
            .range([0, width]);
        chart.append("g")
            .call(d3.axisBottom(x));

        const y = d3.scaleLinear()
            .domain([0,100])
            .range([height, 0]);
        chart.append("g")
            .call(d3.axisLeft(y));

        // const graph = d3.selectAll(".graph")
        //     .data()
    }
    

    render() {
        return (
            <div className="chart">
                <svg ref={r => (this.chartRef = r)}/>
            </div>
        );
    }
}
