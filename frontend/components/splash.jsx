import React, { useState } from 'react';
import { Link } from "react-router-dom";
import { useQuery } from "@apollo/client";
import { GET_SEASON_STATS } from '../util/queries';
import Loading from './elements/loading';
import Lollipop from "./d3/lollipop";
import { statNameMap } from "../util/util";


export default function Splash(props) {
    const [stat, setstat] = useState("ortg");
    // const [dateRange, setDateRange] = useState([0,0]);
    // const day = 86400000;
    
    const stats = ["ortg", "drtg", "fgPct", "tpPct", "ftPct", "ts", "ast", "trb", "stl", "blk", "tovPct"];
    
    const { loading, error, data } = useQuery(GET_SEASON_STATS, {
        variables: { year: 2019 }
    });
    
    const teamStats = data?.season?.teamStats || [];
    
    if (loading) return <Loading/>;
    if (error) return <div>Error! {error.message}</div>;
    
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

                <div className="glossary-link">
                    <Link to="/glossary">Glossary</Link>
                </div>

                <div className="stat-selector">
                    {statTags}
                </div>

                {/* <div className="date-selector-container">
                    <span className="date-selector">
                        <input type="range" name="" id="" value={dateRange[0]} onChange={(e) => setDateRange([e.target.value, dateRange[1]])} min={start} max={dateRange[1]-day} step={day} />
                        <input type="range" name="" id="" value={dateRange[1]} onChange={(e) => setDateRange([dateRange[0], e.target.value])} min={dateRange[0]+day} max={finish}/>
                    </span>
                </div> */}
                <Lollipop statName={stat} stats={teamStats} />

            </div>
        </div>
    );

}