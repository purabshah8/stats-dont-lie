import React, { Component } from "react";
import LineChart from "./line_chart";
import HeatMap from "./heat_map";

export default class ChartPicker extends Component {
    constructor(props) {
        super(props);
        this.state = {
            lineChartType: "fg"
        };
    }

    render() {
        return (
            <div className="container">
                <HeatMap stats={this.props.stats} />
                <LineChart 
                    stats={this.props.stats} 
                    statName={this.state.lineChartType} 
                    xMin={new Date(this.props.season.seasonStart)}
                    xMax={new Date(this.props.season.playoffStart)}/>
            </div>
        );
    }
}
