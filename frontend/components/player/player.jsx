import React from 'react';
import { Query } from "react-apollo";
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
                        if (loading) return <div className="lds-ring is-centered"><div></div><div></div><div></div><div></div></div>;
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
                                <PlayerDetails 
                                    player={player} 
                                    team={currentTeamSeason.team} 
                                    year={0}/>
                                <SeasonPicker 
                                    path={this.props.history.location.pathname} 
                                    start={player.rookieSeason.year} 
                                    end={player.finalSeason ? player.finalSeason.year : 2019 } />
                                <div className={`${abbreviation}-theme main-container`}>
                                    <ChartPicker 
                                        stats={stats} 
                                        season={currentTeamSeason.season}/>
                                </div>
                            </>
                        );
                    }
                }
            </Query>
        );
    }
    
    render() {
        return(
            <div className="section">
                {this.renderQuery()}
            </div>
        );
    }
}