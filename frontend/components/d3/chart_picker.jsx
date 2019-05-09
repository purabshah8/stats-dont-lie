import React, { Component } from "react";
import LineChart from "./line_chart";
import HeatMap from "./heat_map";
import { statNameMap } from "../../util/util";

export default class ChartPicker extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chartStat: "pts"
    };
    this.changeChartType = this.changeChartType.bind(this);
  }

  changeChartType(e) {
      this.setState({
          chartStat: e.target.getAttribute("data-stat")
      });
  }

  renderMenuOptions() {
    const menuLabels = ["Stats", "Shooting", "Hustle", "Advanced"];
    const menuOptions = {
      Stats: ["pts", "ast", "fg", "fga", "orb", "trb", "tp", "ft", "tpar", "ftr"],
      Hustle: ["stl", "blk", "tov", "pf"],
      Shooting: ["fgPct", "ftPct", "tpPct", "ts", "efg"],
      Advanced: [
        "orbPct",
        "drbPct",
        "trbPct",
        "astPct",
        "stlPct",
        "blkPct",
        "tovPct",
        "usgRate",
        "ortg",
        "drtg"
      ]
    };
    const menu = menuLabels.map(label => {
        let menuListItems = menuOptions[label].map(stat => {
        let liClassNames = "";
        if (this.state.chartStat === stat)
            liClassNames += "is-active";
            return <li onClick={this.changeChartType} data-stat={stat} key={stat} className={liClassNames}>{statNameMap[stat]}</li>;
            });
            return (
            <React.Fragment key={label}>
                <p className="menu-label">{label}</p>
                <ul className="menu-list">{menuListItems}</ul>
            </React.Fragment>
            );
        });
        return menu;
  }

  render() {
    const { stats, season } = this.props;
    return (
        <div className="container">
          <HeatMap stats={stats} season={season} />
        </div>
    );
  }
}
// <div className="menu">{this.renderMenuOptions()}</div>
/* <LineChart
  stats={stats}
  statName={this.state.chartStat}
  xMin={new Date(season.startDate)}
  xMax={new Date(season.playoffsStartDate)}
/> */