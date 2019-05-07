import React from 'react';
import * as d3 from 'd3';
import D3Components from "./d3_components";
import { statNameMap } from "../../util/util";
// import { stat } from 'fs';

export default class LineChart extends React.Component {
    constructor(props) {
        super(props);
        this.margin = { top: 50, bottom: 100, left: 100, right: 50 };
        this.chartRef = null;
        this.setChartRef = el => { this.chartRef = el; };
        
        // this.circles = this.createCircles();
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
            if (i >= n-1) {
                const nPoints = data.slice(i+1-n, i+1);
                const sum = nPoints.reduce((total, datum) => total+datum);
                averagedData.push(sum/n);
            }
        }
        return averagedData;
    }

    generateData() {
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
    }

    createChart() {
        const chart = d3.select(this.chartRef);
        chart.selectAll("*").remove();
        
        const xScale = d3.scaleTime()
        .domain([this.props.xMin, this.props.xMax])
        .range([0, 1280]);

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
            const y = statGroup.map(datum => datum.y);
            const stats = this.movingAverage(y, 5);
            let lineData =[];
            statGroup.forEach((datum,i) => {
                if (i >= 4)
                lineData.push({x: datum.x, y: stats[i-4]});
            });
            chart.append("path")
                .datum(lineData)
                .attr("class", "curve")
                .attr("d", line);
        });

        const statFullName = statNameMap[this.props.statName]
        chart.append("text")
            .attr("transform", "translate(440, 20)")
            .attr("font-size", "2rem")
            .text(`Player ${statFullName} (5 Game Rolling Avg)`);

        chart.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - this.margin.left)
            .attr("x",0 - (800 / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text(`${statFullName}`);   

        chart.append("text")             
            .attr("transform",`translate(640,${(800 + this.margin.top + 20)})`)
            .style("text-anchor", "middle")
            .text("Date");
    }

    componentDidMount() {
        this.generateData();
        this.createChart();
    }

    componentDidUpdate() {
        this.generateData();
        this.createChart();
    }
    
    render() {
        console.log(this.props.statName);
        return (
            <div className="d3-container">
                <svg 
                    className="d3-svg" 
                    viewBox="0 0 1380 900" 
                    preserveAspectRatio="xMinYMin meet">
                    <g 
                    ref={this.setChartRef}
                    transform={`translate(${this.margin.left}, ${this.margin.top})`}>
                    </g>
                </svg>
            </div>
        );
    }
}
