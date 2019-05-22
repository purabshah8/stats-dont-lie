import React, { useState } from 'react';
import { Query } from "react-apollo";
import { GET_SEASON_STATS } from '../util/queries';
import Loading from './elements/loading';
import Lollipop from "./d3/lollipop";
import { statNameMap } from "../util/util";


export default function Splash(props) {
    const [stat, setstat] = useState("ortg");
    const stats = ["ortg", "drtg", "fgPct", "tpPct", "ftPct", "ts", "ast", "trb", "stl", "blk", "tov"];
    const statTags = stats.map(statName => {
        let statClasses = "tag stat-tag";
        if (statName === stat)
            statClasses += " is-dark";
        return (
            <div onClick={() => setstat(statName)}
            key={statName} className={statClasses}>
                {statNameMap[statName]}
            </div>
        );
    });
    return(
        <div className="section">
            <div className="title has-text-centered">Stats Don't Lie</div>
            <div className="subtitle has-text-centered is-6">Explore NBA stats using D3</div>
            
            <div className="container splash-container">
                <div className="title is-4">2018-19 Team Stats</div>

                <div className="stat-selector">
                    {statTags}
                </div>

                <Query query={GET_SEASON_STATS} variables={{ year: 2019 }}>
                    {
                        ({loading, error, data}) => {
                            if (loading) return <Loading/>;
                            if (error) return <div>Error! ${error.message}</div>;

                            const { season } = data;


                            return <Lollipop statName={stat} teamStats={season.teamStats} />;
                        }
                    }
                </Query>

            </div>
        </div>
    );

}