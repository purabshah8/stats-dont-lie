import React from "react";
import { useQuery } from "@apollo/client";
import { useParams, useLocation } from "react-router-dom";
import Loading from "../elements/loading";
import { GET_PLAYER_SEASON } from "../../util/queries";
import PlayerDetails from "./player_details";
import SeasonPicker from "../elements/season_picker";
import LineChart from "../d3/line_chart";
import ChartPicker from "../d3/chart_picker";
import { themeVar } from "../../root";

function PlayerSeasonContent({ playerId, year, repeat = false }) {
    const location = useLocation();
    const { loading, error, data } = useQuery(GET_PLAYER_SEASON, {
        variables: { playerId: parseInt(playerId), year: parseInt(year) }
    });

    if (loading) return <Loading />;
    if (error) return <div>Error! {error.message}</div>;

    const playerSeasons = data.playerSeason;
    if (playerSeasons.length !== 0) {
        const { player } = playerSeasons[0];
        const currentTeamSeason = playerSeasons[playerSeasons.length-1].teamSeason;
        const { abbreviation } = currentTeamSeason.team;
        
        // Update theme using reactive variable
        themeVar(abbreviation);
        
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
                    year={ repeat ? 0 : year}/>
                <div className="secondary-diagonal"></div>
                <div className="secondary-background"></div>
                <SeasonPicker 
                    path={location.pathname} 
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
        return <PlayerSeasonContent playerId={playerId} year="2019" repeat={true} />;
    }
}

export default function PlayerSeason() {
    const { playerId, year } = useParams();
    return <PlayerSeasonContent playerId={playerId} year={year} />;
}
