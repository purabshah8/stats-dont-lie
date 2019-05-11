import React from 'react';
import { Query } from "react-apollo";
import Loading from "../elements/loading";
import { GET_PLAYER_SEASON } from "../../util/queries";
import PlayerDetails from "./player_details";
import SeasonPicker from "../elements/season_picker";
import ChartPicker from '../d3/chart_picker';

export default class Player extends React.Component {
    constructor(props) {
        super(props);
    }

    renderQuery() {
        const year = 2019;
        return(
            <Query query={GET_PLAYER_SEASON} variables={ { playerId: this.props.match.params.id, year } }>
                {
                    ({loading, error, data, client}) => {
                        if (loading) return <Loading/>;
                        if (error) return `Error! ${error.message}`;
                        
                        const playerSeasons = data.playerSeason;
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
                                <PlayerDetails 
                                    player={player}
                                    totalStats = {totalStats} 
                                    team={currentTeamSeason.team} 
                                    year={0}/>
                                <div className="secondary-diagonal"></div>
                                <div className="secondary-background"></div>
                                <SeasonPicker 
                                    path={this.props.history.location.pathname} 
                                    start={player.rookieSeason.year} 
                                    end={player.finalSeason ? player.finalSeason.year : 2019 } />
                                <div className={`${abbreviation}-theme main-container`}>
                                    <ChartPicker 
                                        stats={rawStats} 
                                        season={currentTeamSeason.season}/>
                                </div>
                            </div>
                        );
                    }
                }
            </Query>
        );
    }
    
    render() {
        return this.renderQuery();
    }
}