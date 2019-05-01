
export const yearToSeason = (year) => {
    const startYear = year - 1;
    let endYear = year - 2000;
    if (endYear < 0)
                endYear += 100; 
    return `${startYear}-${endYear}`;
};

export const statNameMap = {
    "mp": "Minutes",
    "fg": "FG",
    "fga": "FG Attempted",
    "fgPct": "FG%",
    "tp": "3P",
    "tpa": "3PA",
    "tpPct": "3P%",
    "ft": "FT",
    "fta": "FTA",
    "ftPct": "FT%",
    "orb": "OReb",
    "drb": "DReb",
    "treb": "Rebounds",
    "ast": "Assists",
    "stl": "Steals",
    "blk": "Blocks",
    "tov": "Turnovers",
    "pf": "Fouls",
    "pts": "Points",
    "ts": "True Shooting %",
    "efg": "Effective FG%",
    "tpar": "3PA Rate", 
    "ftr": "FT Rate", 
    "orbPct": "OReb%", 
    "drbPct": "DReb%",
    "trbPct": "Rebound %", 
    "astPct": "Assist %", 
    "stlPct": "Steal %", 
    "blkPct": "Block %", 
    "tovPct": "Turover %", 
    "usgRate": "Usage Rate", 
    "ortg": "Offensive Rating", 
    "drtg": "Defensive Rating",
};