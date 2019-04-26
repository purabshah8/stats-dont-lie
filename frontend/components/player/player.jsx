import React from 'react';
import { Query } from "react-apollo";
import { range } from "lodash";
import { GET_PLAYER, GET_PLAYER_SEASON } from "../../util/queries";
import PlayerDetails from "./player_details";
import LineChart from "../charts/line_chart";
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
        return(
            <Query query={GET_PLAYER} variables={ { playerId: this.props.match.params.id } }>
                {
                    ({loading, error, data}) => {
                        if (loading) return 'Loading...';
                        if (error) return `Error! ${error.message}`;

                        const player = data.player;
                        return(
                            <div className="section">
                                <PlayerDetails data={data} />
                                <div className="select">
                                    {this.renderSeasonOptions(player)}
                                </div>
                                <LineChart playerid={this.props.match.params.id} year={this.state.year} />
                            </div>
                        );
                    }
                }
            </Query>
        );
    }

    // render() {
    //     return (
    //         <>
    //         <div className="section">
    //             <PlayerDetails playerId={this.props.match.params.id} />
    //         </div>
    //         <LineChart playerId={this.props.match.params.id} />
    //         </>
    //     );
    // }
}