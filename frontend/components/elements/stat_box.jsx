import React from 'react';
import { statNameMap } from "../../util/util";

export default function StatBox(props) {
    const { positions, stats, boxHeader } = props;
    const isLengthOne = el => el.length === 1;
    const basePositions = positions.filter(isLengthOne);
    const statNames = new Set(["pts", "ts"]);
    basePositions.forEach(pos => {
        if (pos === "G")
            statNames.add("ast").add("tov");
        if (pos === "F")
            statNames.add("trb").add("ast");
        if (pos === "C")
            statNames.add("trb").add("blk");
    });
    let statDivs = [];
    statNames.forEach(name => {
        let val = stats[name];
        if (name !== "ts")
            val /= stats["gp"];
        else
            val *= 100;
        statDivs.push(
            <div className="column">
                <div className="box-stat-val">{val.toFixed(1)}</div>
                <div className="box-stat-name">{statNameMap[name]}</div>
            </div>
        );
    });
    return (
        <div className="box level-item box-container">
            <div className="box-header">
                <span>{boxHeader}</span>
            </div>
            <div className="box-content">
                <div className="box-body columns">
                    {statDivs}
                </div>
            </div>
        </div>
    );
}
