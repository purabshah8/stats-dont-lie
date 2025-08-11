import React, { useEffect } from 'react';
import * as d3 from 'd3';
import zTable from 'ztable';
import { statNameMap } from "../../util/util";

function calcZScore(val, mean, stdDev) {
    return (val - mean)/stdDev;
}

export default function HeatMap({stats, season}) {
    let chartRef = null;
    let containerRef = null;
    const setContainerRef = el => { containerRef = el; };
    const setChartRef = el => { chartRef = el; };
    
    const baseHeight = 800;
    const baseWidth = 1280;
    const margin = { top: 100, bottom: 50, left: 75, right: 50 };
    const height = baseHeight + margin.top + margin.bottom;
    const width = baseWidth + margin.left + margin.right;
    
    const statLabels = Object.keys(stats[0]).reverse();
    const extraLabels = ["gameDates", "__typename"];
    extraLabels.forEach(label => {
        const idx = statLabels.indexOf(label);
        statLabels.splice(idx, 1);
    });
    const { averages, standardDeviations } = season.aggregateStats;
    const dates = [];
    const data = [];
    stats.forEach(team => {
        statLabels.forEach(statName => {
            team[statName].forEach((val, i) => {
                if (statName === "started")
                    val += 0;
                const gameDate = new Date(team["gameDates"][i]);
                dates.push(gameDate);
                data.push({ 
                    date: gameDate, 
                    stat: statNameMap[statName],
                    val,
                    normVal: calcZScore(val, averages[statName], standardDeviations[statName]) || -Infinity
                });
            });
        });
    });

    // Scales
    const xScale = d3.scaleBand()
            .range([0, baseWidth])
            .domain(dates)
            .padding(0.05);
    const yScale = d3.scaleBand()
        .range([baseHeight, 0])
        .domain(statLabels.map(label => statNameMap[label]));
    const colorScale = d3.scaleSequential()
        .domain([0, 1])
        .interpolator(d3.interpolateRdYlBu);

    // Axes
    const xAxis = d3.axisBottom(xScale)
        .tickSize(0)
        .tickFormat(d3.timeFormat("%m/%d"));
    const yAxis = d3.axisLeft(yScale).tickSize(0);

    useEffect(() => {
        // create top level group
        const chart = d3.select(chartRef)
            .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);
        
        // x axis tick labels
        chart.append("g")
            .attr("transform", `translate(0,${baseHeight})`)
            .call(xAxis)
            .selectAll("text")
                .attr("y", 0)
                .attr("x", 9)
                .attr("dy", ".35em")
                .attr("transform", "rotate(90)")
                .style("text-anchor", "start")
            .select(".domain").remove();
       
        // y axis tick labels
        chart.append("g")
            .call(yAxis)
            .selectAll("text")
                .attr("font-size", "1rem")
                .attr("y", -10)
                .attr("x", -60)
                // .attr("dy", ".35em")
                .style("text-anchor", "start")
            .select(".domain").remove();


        
        // tooltip and accompanying event handlers
        const tooltip = d3.select(containerRef)
            .append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        const mouseOver = function(d) {
            tooltip
                .transition()
                .duration(200)
                .style("opacity", 1);
            d3.select(this)
                .transition()
                .duration(200)
                .style("stroke", "black")
                .style("opacity", 1);
        };
    
        const mouseMove = function(event, d) {
            tooltip
                .html(`Date: ${d.date.toLocaleDateString()} <br/> Stat: ${d.stat} <br/> Value: ${d.val} <br/> zScore: ${d.normVal.toFixed(2)}`)
                .style("left", d3.pointer(event)[0] + "px")
                .style("top", d3.pointer(event)[1] + "px");
        };
        const mouseLeave = function(d) {
            tooltip.style("opacity", 0);
            d3.select(this)
                .transition()
                .duration(350)
                .style("stroke", "none")
                .style("opacity", 0.8);
        };
        
        // add rectangles
        chart.selectAll()
            .data(data, function(d) {return d.date+':'+d.stat;})
            .enter()
            .append("rect")
                .attr("class", "heat-map-rect")
                .attr("x", d => xScale(d.date))
                .attr("y", d => yScale(d.stat))
                .attr("width", xScale.bandwidth() )
                .attr("height", yScale.bandwidth()/2 )
                .style("fill", d => colorScale( zTable(0-d.normVal) ))
            .on("mouseover", mouseOver)
            .on("mousemove", mouseMove)
            .on("mouseleave", mouseLeave);

        // Title
        chart.append("text")
            .attr("x", `${width/2-250}`)
            .attr("y", "-20")
            .attr("text-anchor", "left")
            .style("font-size", "2.5em")
            .text("Performance Heatmap");
        
        // x axis label
        chart.append("text")
            .attr("x", `${width/2-80}`)
            .attr("y", `${baseHeight+50}`)
            .attr("text-anchor", "left")
            .style("font-size", "1em")
            .text("Game");

        // y axis label
        chart.append("text")
            .attr("x", "-50")
            .attr("y", `${baseHeight/2}`)
            .attr("transform", "rotate(90)")
            .attr("text-anchor", "left")
            .style("font-size", "1em")
            .text("Stat");

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