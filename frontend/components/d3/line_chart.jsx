import React from 'react';
import * as d3 from 'd3';
import D3Components from "./d3_components";
// import { stat } from 'fs';

export default class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this.chartRef = null;
        this.setChartRef = el => { this.chartRef = el; };
        
        let yMin, yMax;
        this.data = this.props.stats.map(team => { 
            const data = [];
            team["gameDates"].forEach((date,i) => {
                const y = team[this.props.statName][i];
                if (typeof yMin === "undefined" || yMin > y)
                    yMin = y;
                if (typeof yMax === "undefined" || yMax < y)
                    yMax = y;
                data.push({ x: new Date(date), y });
            });
            return data;
        });
        this.yMin = yMin;
        this.yMax = yMax;
        // this.circles = this.createCircles();
        this.margin = { top: 50, bottom: 50, left: 50, right: 50 };
        // this.width = 1280 + this.margin.left + this.margin.right;
        // this.height = 800 + this.margin.top + this.margin.bottom;
    }


    // createCircles() {
    //     const circles = this.data.map((y,i) => ({
    //      x: i+1,
    //      y,
    //      radius: this.props.stats[0]["fga"][i]*0.5,
    //     }));
    //     return circles;
    // }

    movingAverage(data, n) {
        const averagedData = [];
        for (let i = 0; i < data.length; i++) {
            if (i >= n) {
                const nPoints = data.slice(i-n, i);
                const sum = nPoints.reduce((total, datum) => total+datum);
                averagedData.push(sum/n);
            }
        }
        return averagedData;
    }

    componentDidMount() {
        const chart = d3.select(this.chartRef)
            .append("g")
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);
        
        const xScale = d3.scaleTime()
        .domain([this.props.xMin, this.props.xMax])
        .range([0, 1280]);
        
        // let yMin, yMax;
        // this.data.forEach(statGroup => {
        //     const currYMin = d3.min(statGroup.y)
        //     if (!yMin || yMin > currYMin) {
        //         yMin = currYMin;
        //     }
        //     const currYMax = d3.max(statGroup.y)
        //     if (!yMax || yMax > currYMax) {
        //         yMax = currYMax;
        //     }
        // });

        const yScale = d3.scaleLinear()
        .domain([this.yMin, this.yMax])
        .range([800, 0]);
        
        const xAxis = d3.axisBottom().scale(xScale);
        const yAxis = d3.axisLeft().scale(yScale);
        
        const line = d3.line()
        .x(function(d) { return xScale(d.x);})
        .y(function(d) { return yScale(d.y);})
        .curve(d3.curveMonotoneX);
        
        
        chart.append("g")
        .call(yAxis);
        
        chart.append("g")
        .attr("transform", "translate(0,800)")
        .call(xAxis);
        
        // chart.selectAll("circle")
        //     .data(this.circles)
        //     .enter()
        //     .append("circle")
        //     .attr("cx",  function (d) { return xScale(d.x); })
        //     .attr("cy",  function (d) { return yScale(d.y*100); })
        //     .attr("r",  function (d) { return d.radius; });
        // .attr("class", "black");
        this.data.forEach(statGroup => {
            
            // const stats = this.movingAverage(statGroup, 5);
            chart.append("path")
                .datum(statGroup)
                .attr("class", "curve")
                .attr("d", line);
        });

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
