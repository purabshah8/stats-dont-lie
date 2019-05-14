import React from 'react';
import * as d3 from 'd3';


export default function Lollipop({  }) {
    let chartRef = null;
    let containerRef = null;
    const setContainerRef = el => { containerRef = el; };
    const setChartRef = el => { chartRef = el; };

    const baseHeight = 800;
    const baseWidth = 1280;
    const margin = { top: 100, bottom: 50, left: 75, right: 50 };
    const height = baseHeight + margin.top + margin.bottom;
    const width = baseWidth + margin.left + margin.right;

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
