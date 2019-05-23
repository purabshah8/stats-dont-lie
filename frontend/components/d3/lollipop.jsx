import React, { useEffect } from 'react';
import * as d3 from 'd3';
import { statNameMap } from '../../util/util';


export default function Lollipop({ teamStats, statName }) {
    let chartRef = null;
    let containerRef = null;
    const setContainerRef = el => { containerRef = el; };
    const setChartRef = el => { chartRef = el; };

    const baseHeight = 800;
    const baseWidth = 1280;
    const margin = { top: 100, bottom: 50, left: 75, right: 50 };
    const height = baseHeight + margin.top + margin.bottom;
    const width = baseWidth + margin.left + margin.right;
    teamStats.sort((b,a) => b[statName] - a[statName]);
    const teams = teamStats.map(team => team.abbr);
    const values = teamStats.map(team => team[statName]);
    const minVal = d3.min(values);
    const maxVal = d3.max(values);
    
    // Scales
    const xScale = d3.scaleLinear()
        .range([0, baseWidth])
        .domain([minVal-0.1*minVal, maxVal+0.01*maxVal]); // add stat
    
        const yScale = d3.scaleBand()
        .range([baseHeight, 0])
        .domain(teams)
        .padding(1);

    const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale).tickSize(0);

    useEffect(() => {
        
        const chart = d3.select(chartRef)
            .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);
        
        chart.selectAll("*").remove();
        
        // Title
        chart.append("text")
            .attr("x", `${width/2-250}`)
            .attr("y", "-20")
            .attr("class", "d3-title")
            .text(`Team ${statNameMap[statName]}`);

        chart.append("g")
            .attr("transform", `translate(0,${baseHeight})`)
            .transition()
            .duration(1000)
            .call(xAxis);
        
        chart.append("g")
            .style("font-size", "0.8rem")
            .transition()
            .duration(1000)
            .call(yAxis);
        
        
        // chart.selectAll("myline")
        //     .data(teamStats)
        //     .enter()
        //     .append("line")
        //       .attr("x1", 0)
        //       .attr("x2", 0)
        //       .attr("y1", function(d) { return yScale(d.abbr); })
        //       .attr("y2", function(d) { return yScale(d.abbr); })
        //       .attr("stroke", "grey");
    
        chart.selectAll("mycircle")
            .data(teamStats)
            .enter()
            .append("circle")
                .attr("cx", 0)
                .attr("cy", function(d) { return yScale(d.abbr); })
                .attr("r", "10")
                .style("fill", "#69b3a2");

        chart.selectAll("circle")
            .transition()
            .duration(2000)
            .attr("cx", function(d) { return xScale(d[statName]); });
              
        // chart.selectAll("line")
        //     .transition()
        //     .duration(2000)
        //     .attr("x1", function(d) { return xScale(d[statName]); });
    });

    return (
        <div ref={setContainerRef} className="d3-container">
            <svg ref={setChartRef} 
                className="d3-svg" 
                viewBox={`0 0 ${width} ${height}`} 
                preserveAspectRatio="xMinYMin meet">
            </svg>
        </div>
    );
}
