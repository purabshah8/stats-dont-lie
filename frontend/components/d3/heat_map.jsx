import React from 'react';
import * as d3 from 'd3';


export default class HeatMap extends React.Component {
    constructor(props) {
        super(props);
        this.chartRef = null;
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
    }
    
    render() {
        return (
            <div className="heatmap-container">
            <svg ref={this.setChartRef} className="chart-svg" 
                viewBox="0 0 1380 900" preserveAspectRatio="xMinYMin meet">
            </svg>
        </div>
        );
    }
}
