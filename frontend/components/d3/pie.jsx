import React, { useEffect } from 'react';
import * as d3 from 'd3';

export default function Pie({value}) {
    let chartRef = null;
    let containerRef = null;
    const setContainerRef = el => { containerRef = el; };
    const setChartRef = el => { chartRef = el; };

    const width = 500;
    const height = 500;
    const margin = 50;

    const radius = Math.min(width, height) / 2 - margin;
    
    useEffect(() => {
        d3.select(chartRef)
            .append("g")
            .attr("transform", `translate(${width/2}, + ${height/2})`);
        
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
