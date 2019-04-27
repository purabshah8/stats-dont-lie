import React from 'react';
import { Query } from "react-apollo";
import { range } from "lodash";
import { GET_PLAYER, GET_PLAYER_SEASON } from "../../util/queries";
import PlayerDetails from "./player_details";
import LineChart from "../d3/line_chart";
export default class Player extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            year: 0
        };
    }

    toggleState(field) {
        return e => {
            this.setState({[field]: parseInt(e.target.value)});
        };
    }

    renderSeasonOptions(player) {
        const rookieSeason = player.rookieSeason.year;
        let finalSeason;
        if (player.finalSeason)
            {
                finalSeason = player.finalSeason.year;
                this.setState({year: player.finalSeason.year});
            }
        else
            finalSeason = 2019;
        let playerSeasons = range(rookieSeason, finalSeason+1);
        const seasonOptions = playerSeasons.map(season => {
            const startYear = season-1;
            let endYear = season - 2000;
            if (endYear < 0)
                endYear += 100;
            return(
                <option key={season} value={season}>
                    {startYear + "-" + endYear}
                </option>
            );
        }); 
        return(
            <select onChange={this.toggleState("year")} value={this.state.year}>
                <optgroup label="Season Stats">
                    {seasonOptions}
                </optgroup>
                <option value={0}>Career</option>
            </select>
        );
    }
    
    render() {
        console.log(this.state);
        const year = this.state.year ? this.state.year : 2019;
        return(
            <div className="section">
                <Query query={GET_PLAYER_SEASON} variables={ { playerId: this.props.match.params.id, year } }>
                    {
                        ({loading, error, data, client}) => {
                            if (loading) return <progress className="progress" max="100">50%</progress>;
                            if (error) return `Error! ${error.message}`;
                            const playerSeasons = data.playerSeason;
                            const { player } = playerSeasons[0];
                            const currentTeamSeason = playerSeasons[playerSeasons.length-1].teamSeason;
                            const { abbreviation } = currentTeamSeason.team;
                            client.writeData({ data : {theme: abbreviation} });
                            let stats = [];
                            playerSeasons.forEach(ps => stats.push(ps.rawStats));
                            return(
                                    <>
                                        <PlayerDetails player={player} team={currentTeamSeason.team}/>
                                        <div className="select">
                                            {this.renderSeasonOptions(player)}
                                        </div>
                                        <div className="container">
                                            <LineChart stats={stats} />
                                        </div>
                                    </>
                            );
                        }
                    }
                </Query>
            </div>
        );
    }
}