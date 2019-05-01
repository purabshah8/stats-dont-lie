import React from "react";
import { Link } from "react-router-dom";
import { range } from "lodash";
import { yearToSeason } from "../../util/util";

export default class SeasonPicker extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isActive: false
        };
        const pathArr = this.props.path.split("/");
        const seasonType = pathArr[1];
        this.basePath = pathArr.slice(0,3).join("/");
        this.baseLinkText = null;
        if (seasonType === "teams")
            this.baseLinkText = "Team Page";
        else if (seasonType === "players")
            this.baseLinkText = "Career";
    }

    toggleActive() {
        return e => {
            this.setState({ isActive: !this.state.isActive });
        };
    }

    renderSeasonOptions() {
        const seasons = range(this.props.start, this.props.end+1);
        const seasonOptions = seasons.map(season => (
                <Link key={season} className="dropdown-item" to={`${this.basePath}/seasons/${season}`}>
                    {yearToSeason(season)}
                </Link>
            )
        );
        return seasonOptions;
    }

    render() {
        let dropdownClasses = "dropdown ";
        dropdownClasses += this.state.isActive ? " is-active" : "";
        return (
            <div className="section">
                <div className={dropdownClasses} onClick={this.toggleActive()}>
                    <div className="dropdown-trigger">
                        <button className="button" aria-haspopup="true" aria-controls="dropdown-menu">
                            <span>Select Season</span>
                            <span className="icon is-small">
                                <i className="fas fa-angle-down" aria-hidden="true"></i>
                            </span>
                        </button>
                    </div>
                    <div className="dropdown-menu" role="menu">
                        <div className="dropdown-content">
                            {this.renderSeasonOptions()}
                            <hr className="dropdown-divider"></hr>
                            <Link className="dropdown-item" to={this.basePath}>{this.baseLinkText}</Link>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
