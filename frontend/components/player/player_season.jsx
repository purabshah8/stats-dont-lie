import React, { Component } from "react";
import { Query } from "react-apollo";
import { GET_PLAYER_SEASON } from "../../util/queries";
import PlayerDetails from "./player_details";
import SeasonPicker from "../elements/season_picker";
import LineChart from "../d3/line_chart";
import ChartPicker from "../d3/chart_picker";

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
                        let rawStats = [];
                        let totalStats = {};
                        playerSeasons.forEach(ps => {
                            rawStats.push(ps.rawStats);
                            Object.entries(ps.totalStats).forEach(([statName, val]) => {
                                if (totalStats.hasOwnProperty(statName))
                                    totalStats[statName] += val;
                                else
                                    totalStats[statName] = val;
                            });
                        });
                        totalStats["ts"] = totalStats["pts"]/(2*(totalStats["fga"]+0.44*totalStats["fta"]));
                        return(
                                <div className={`${abbreviation}-theme`}>
                                    <div className="primary-background">
                                    </div>
                                    <div className="secondary-background">
                                        <div className="primary-diagonal"></div>
                                        <div className="white-diagonal"></div>
                                    </div>
                                    <div className="white-background">
                                    <PlayerDetails 
                                        player={player}
                                        totalStats = {totalStats}
                                        team={currentTeamSeason.team} 
                                        year={ repeat ? 0 : year}/>
                                    </div>
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
                                            <div className={`${abbreviation}-theme main-container`}>
                                                <ChartPicker stats={rawStats} season={currentTeamSeason.season}/>
                                            </div>
                                    }
                                </div>
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
        return this.renderQuery(playerId, year);
    }
}
