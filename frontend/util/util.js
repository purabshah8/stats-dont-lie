
export const yearToSeason = (year) => {
    const startYear = year - 1;
    let endYear = year - 2000;
    if (endYear < 0)
                endYear += 100; 
    return `${startYear}-${endYear}`;
};