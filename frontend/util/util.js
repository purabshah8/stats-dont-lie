
export const yearToSeason = (year) => {
    const startYear = year - 1;
    let endYear = year - 2000;
    if (endYear < 0)
                endYear += 100; 
    return `${startYear}-${endYear.toString().padStart(2,'0')}`;
};

export const statNameMap = {
    "mp": "Min",
    "fg": "FG",
    "fga": "FGA",
    "fgPct": "FG%",
    "tp": "3P",
    "tpa": "3PA",
    "tpPct": "3P%",
    "ft": "FT",
    "fta": "FTA",
    "ftPct": "FT%",
    "orb": "ORBs",
    "drb": "DRBs",
    "trb": "REBs",
    "ast": "Assists",
    "stl": "Steals",
    "blk": "Blocks",
    "tov": "TOs",
    "pf": "Fouls",
    "pts": "Points",
    "plusMinus": "+/-",
    "starts": "Starts",
    "started": "Started",
    "ts": "TS%",
    "efg": "eFG%",
    "tpar": "3PA Rate", 
    "ftr": "FT Rate", 
    "orbPct": "OReb%", 
    "drbPct": "DReb%",
    "trbPct": "Rebound %", 
    "astPct": "Assist %", 
    "stlPct": "Steal %", 
    "blkPct": "Block %", 
    "tovPct": "TO%", 
    "usgRate": "Usage Rate", 
    "ortg": "Offensive Rating", 
    "drtg": "Defensive Rating",
};