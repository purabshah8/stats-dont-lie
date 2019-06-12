import React, { useEffect } from 'react';
import * as d3 from 'd3';
import { statNameMap } from '../../util/util';


export default function Lollipop({ stats, statName }) {
    let chartRef = null;
    let containerRef = null;
    const setContainerRef = el => { containerRef = el; };
    const setChartRef = el => { chartRef = el; };
    
    const baseHeight = 800;
    const baseWidth = 1280;
    const margin = { top: 100, bottom: 50, left: 75, right: 50 };
    const height = baseHeight + margin.top + margin.bottom;
    const width = baseWidth + margin.left + margin.right;
    let xLabel = `${statNameMap[statNameMap[statName]]} (per 100 poss)`;

    let teamStats = [];
    stats.forEach(team => teamStats.push(Object.assign({}, team)));

    const pctStats = ["fgPct", "tpPct", "ftPct", "ts"];
    teamStats.forEach(team => {
        pctStats.forEach(stat => { team[stat] *= 100; });
    });
    
    if (pctStats.includes(statName))
        xLabel = `${statNameMap[statNameMap[statName]]}`;

    const countingStats = ["ast", "trb", "stl", "blk", "tov"];
    if (countingStats.includes(statName)) {
        teamStats = teamStats.map(team => {
            let team_ = team;
            team_[statName] = team[statName]/team["poss"]*100;
            return team_;
        });
    }
        

    teamStats.sort((b,a) => b[statName] - a[statName]);
    if (statName === "drtg")
        teamStats.sort((a,b) => b[statName] - a[statName]);

    const teams = teamStats.map(team => team.abbr);
    let values = teamStats.map(team => team[statName]);
    const minVal = d3.min(values);
    const maxVal = d3.max(values);
    
    // Scales
    let xScale = d3.scaleLinear()
        .range([0, baseWidth])
        .domain([minVal-0.01*minVal, maxVal+0.01*maxVal]); // add stat

    if (statName === "ortg" || statName === "drtg") {
        xScale = d3.scaleLinear()
            .range([0, baseWidth])
            .domain([minVal-2, maxVal+2]);
    }
    
    const yScale = d3.scaleBand()
        .range([baseHeight, 0])
        .domain(teams)
        .padding(1.5);

    const xAxis = d3.axisBottom(xScale).tickSize(0).tickPadding(5);
    const yAxis = d3.axisLeft(yScale).tickSize(0);

    useEffect(() => {

        d3.select(chartRef).selectAll("g").remove();

        const chart = d3.select(chartRef)
            .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);
        
        // Title
        chart.append("text")
            .attr("x", `${width/2}`)
            .attr("y", "-20")
            .attr("class", "d3-title")
            .text(`Team ${statNameMap[statNameMap[statName]]}`);

        chart.append("g")
            .attr("transform", `translate(0,${baseHeight})`)
            .style("font-size", "1rem")
            .transition()
            .duration(1000)
            .call(xAxis);


        chart.append("g")
            .attr("class", "grid")
            .attr("transform", `translate(0,${baseHeight})`)
            .call(
                xAxis.ticks(5)
                    .tickSize(-(baseHeight-45))
                    .tickSizeOuter(0)
                    .tickFormat("")
            );

        chart.append("text")
            .attr("x", `${baseWidth/2}`)
            .attr("y", `${baseHeight+40}`)
            .attr("class","d3-text")
            .text(xLabel);
        
        // chart.append("g")
        //     .style("font-size", "1.2rem")
        //     .transition()
        //     .duration(1000)
        //     .call(yAxis);
        
        // chart.selectAll("myline")
        //     .append("line")
        //         .attr("x1", yScale((maxVal+minVal)/2))
        //         .attr("x2", yScale((maxVal+minVal)/2))
        //         .attr("y1", 0)
        //         .attr("y2", baseHeight)
        //         .attr("stroke", "grey");
        
        // chart.selectAll("myline")
        //     .data(teamStats)
        //     .enter()
        //     .append("line")
        //       .attr("x1", 0)
        //       .attr("x2", 0)
        //       .attr("y1", function(d) { return yScale(d.abbr); })
        //       .attr("y2", function(d) { return yScale(d.abbr); })
        //       .attr("stroke", "grey");

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

        const mouseMove = function(d) {
            tooltip
                .html(`${d.abbr}: ${d[statName]}`)
                .style("left", d3.mouse(this)[0] + "px")
                .style("top", d3.mouse(this)[1] + "px");
        };
        const mouseLeave = function(d) {
            tooltip.style("opacity", 0);
            d3.select(this)
                .transition()
                .duration(350)
                .style("stroke", "none")
                .style("opacity", 0.8);
        };
    
        chart.selectAll("myimage")
            .data(teamStats)
            .enter()
            
            .append("svg:image")
                .attr("x", 0)
                .attr("y", function(d) { return yScale(d.abbr); })
                .attr("width", "36")
                .attr("height", "36")
                .attr("xlink:href", function(d) { return `https://statsdontlie-media.s3.amazonaws.com/${d.abbr}.svg`; })
            .on("mousover", mouseOver)
            .on("mousemove", mouseMove)
            .on("mouseleave", mouseLeave);
            // .append("circle")
            //     .attr("cx", 0)
            //     .attr("cy", function(d) { return yScale(d.abbr); })
            //     .attr("r", "12")
            //     .style("fill", "#69b3a2");

        chart.selectAll("image")
            .transition()
            .duration(2000)
            .attr("x", function(d) { return xScale(d[statName]); });
              
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
