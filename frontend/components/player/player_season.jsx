import React, { Component } from "react";
import { Query } from "react-apollo";
import { GET_PLAYER_SEASON } from "../../util/queries";
import PlayerDetails from "./player_details";
import SeasonPicker from "../elements/season_picker";
import LineChart from "../d3/line_chart";

export default class PlayerSeason extends Component {
    constructor(props) {
        super(props);
    }

    renderQuery(playerId, year, repeat=false) {
        return <Query query={GET_PLAYER_SEASON} variables={ { playerId, year } }>
            {
                ({loading, error, data, client}) => {
                    if (loading) return <div className="lds-ring is-centered"><div></div><div></div><div></div><div></div></div>;
                    if (error) return `Error! ${error.message}`;
                    
                    const playerSeasons = data.playerSeason;
                    if (playerSeasons.length !== 0) {
                        const { player } = playerSeasons[0];
                        const currentTeamSeason = playerSeasons[playerSeasons.length-1].teamSeason;
                        const { abbreviation } = currentTeamSeason.team;
                        client.writeData({ data : {theme: abbreviation} });
                        let stats = [];
                        playerSeasons.forEach(ps => stats.push(ps.rawStats));
                        return(
                                <>
                                    <PlayerDetails player={player} team={currentTeamSeason.team} year={ repeat ? 0 : year}/>
                                    <SeasonPicker 
                                        path={this.props.history.location.pathname} 
                                        start={player.rookieSeason.year} 
                                        end={player.finalSeason ? player.finalSeason.year : 2019 } />
                                    {
                                        repeat ?
                                            <div className="container">
                                                <div className="notification">Coming Soon!</div>
                                            </div>
                                        :
                                            <div className={`${abbreviation}-theme`}>
                                                <LineChart stats={stats} />
                                            </div>
                                    }
                                </>
                        );
                    } else {
                        return this.renderQuery(playerId, 2019, true);
                    }
                }
            }
        </Query>;
    }

    render() {
        const { playerId, year } = this.props.match.params;
        return (
        <div className="section">
            {this.renderQuery(playerId, year)}
        </div>
        );
    }
}
