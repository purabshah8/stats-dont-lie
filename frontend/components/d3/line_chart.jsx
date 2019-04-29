import React from 'react';
import * as d3 from 'd3';
import D3Components from "./d3_components";

export default class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this.data = this.props.stats[0]["fgPct"];
        this.chartRef = null;
        this.setChartRef = el => { this.chartRef = el; };
        this.circles = this.createCircles();
        this.margin = { top: 50, bottom: 50, left: 50, right: 50 };
        // this.width = 1280 + this.margin.left + this.margin.right;
        // this.height = 800 + this.margin.top + this.margin.bottom;
    }


    createCircles() {
        const circles = this.data.map((y,i) => ({
         x: i+1,
         y,
         radius: 5,
        }));
        return circles;
    }

    
    componentDidMount() {

        const chart = d3.select(this.chartRef)
            .append("g")
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
        // const { height, width } = this.chartRef.getBoundingClientRect();
        
        const xScale = d3.scaleLinear()
            .domain([1, this.data.length])
            .range([0, 1280]);
        
        const yScale = d3.scaleLinear()
            .domain([0,100])
            .range([800, 0]);
        
        const xAxis = d3.axisBottom().scale(xScale);
        const yAxis = d3.axisLeft().scale(yScale);
        
        const line = d3.line()
            .x(function(d,i) {return xScale(i+1);})
            .y(function(d) { return yScale(d);})
            .curve(d3.curveMonotoneX);
        
        
        chart.append("g")
            .call(yAxis);
        
        chart.append("g")
            .attr("transform", "translate(0,800)")
            .call(xAxis);
        
        chart.selectAll("circle")
            .data(this.circles)
            .enter()
            .append("circle")
            .attr("cx",  function (d) { return xScale(d.x); })
            .attr("cy",  function (d) { return yScale(d.y*100); })
            .attr("r",  function (d) { return d.radius; })
            .style("fill", "black");

        chart.append("path")
            .datum(this.data.map(el => (el*100)))
            .attr("fill", "none")
            .attr("stroke", "black")
            .attr("stroke-width", 2)
            .attr("d", line);

    }
    
    render() {
        return (
            <div className="chart-container">
                <svg ref={this.setChartRef} className="chart-svg" 
                    viewBox="0 0 1380 900" preserveAspectRatio="xMinYMin meet">
                </svg>
            </div>
        );
    }
}
