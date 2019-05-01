import React from 'react';
import * as d3 from 'd3';


export default class HeatMap extends React.Component {
    constructor(props) {
        super(props);
        this.chartRef = null;
        this.containerRef = null;
        this.setContainerRef = el => { this.chartRef = el; };
        this.setChartRef = el => { this.chartRef = el; };
        this.margin = { top: 50, bottom: 50, left: 50, right: 50 };
        
        const stats = this.props.stats[0];
        this.statLabels = Object.keys(stats);
        const extraLabels = ["gameDates", "__typename"];
        extraLabels.forEach(label => {
            const idx = this.statLabels.indexOf(label);
            this.statLabels.splice(idx, 1);
        });
        this.gameDates = stats["gameDates"].map(date => {
            const d = new Date(date);
            return d.toDateString();
        });
        this.data = this.props.stats.map(team => {
            const data = [];
            this.statLabels.forEach(statName => {
                team[statName].forEach((val, i) => {
                    data.push({ 
                        date: new Date(team["gameDates"][i]), 
                        stat: statName, 
                        val
                    });
                });
            });
            return data;
        });
        // debugger;
    }


    componentDidMount() {
        const chart = d3.select(this.chartRef)
            .append("g")
            .attr("transform", `translate(${this.margin.left}, ${this.margin.top})`);

        const x = d3.scaleBand()
            .range([0,1280])
            .domain(this.gameDates)
            .padding(0.05);

        const y = d3.scaleBand()
            .range([800,0])
            .domain(this.statLabels);

        const colorScale = d3.scaleSequential()
            .domain([0, 100])
            .interpolator(d3.interpolateYlOrRd);

        const tooltip = d3.select(this.containerRef)
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px");
        
        const mouseover = function(d) {
            tooltip.style("opacity", 1);
            d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1);
        };
        const mousemove = function(d) {
            tooltip
                .html("The exact value of<br>this cell is: " + d.value)
                .style("left", (d3.mouse(this)[0]+70) + "px")
                .style("top", (d3.mouse(this)[1]) + "px");
        };
        const mouseleave = function(d) {
        tooltip
            .style("opacity", 0);
        d3.select(this)
            .style("stroke", "none")
            .style("opacity", 0.8);
        };

        chart.selectAll()
            .data(this.data, function(d) {return d.date+':'+d.stat;})
            .enter()
            .append("rect")
            .attr("x", function(d) { return x(d.date); })
            .attr("y", function(d) { return y(d.stat); })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            .style("fill", function(d) { return colorScale(d.value);} )
            .style("stroke-width", 4)
            .style("stroke", "none")
            .style("opacity", 0.8)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave);
    }
    
    render() {
        return (
            <div ref={this.setContainerRef} className="heatmap-container">
                <svg ref={this.setChartRef} 
                    className="chart-svg" 
                    viewBox="0 0 1380 900" 
                    preserveAspectRatio="xMinYMin meet">
                </svg>
            </div>
        );
    }
}
