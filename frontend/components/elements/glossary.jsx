import React from 'react';

export default function Glossary() {
    return (
        <div className="container">
            <div className="title">Glossary</div>
            <ul className="terms">
                <li className="term">2P: 2-Point Field Goals</li>  
                <li className="term">2P%: 2-Point Field Goal Percentage; the formula is 2P / 2PA.</li>  
                <li className="term">2PA: 2-Point Field Goal Attempts</li>  
                <li className="term">3P: 3-Point Field Goals (available since the 1979-80 season in the NBA)</li>  
                <li className="term">3P%: 3-Point Field Goal Percentage (available since the 1979-80 season in the NBA); the formula is 3P / 3PA.</li>  
                <li className="term">3PA: 3-Point Field Goal Attempts (available since the 1979-80 season in the NBA)</li>  
                <li className="term">Age: Age; player age on February 1 of the given season.</li>  
                <li className="term">AST: Assists</li>  
                <li className="term">AST%: Assist Percentage (available since the 1964-65 season in the NBA); the formula is 100 * AST / (((MP / (Tm MP / 5)) * Tm FG) - FG). Assist percentage is an estimate of the percentage of teammate field goals a player assisted while he was on the floor.</li>  
                <li className="term">BLK: Blocks (available since the 1973-74 season in the NBA)</li>  
                <li className="term">BLK%: Block Percentage (available since the 1973-74 season in the NBA); the formula is 100 * (BLK * (Tm MP / 5)) / (MP * (Opp FGA - Opp 3PA)). Block percentage is an estimate of the percentage of opponent two-point field goal attempts blocked by the player while he was on the floor.</li>  
                <li className="term">DPOY: Defensive Player of the Year</li>  
                <li className="term">DRB: Defensive Rebounds (available since the 1973-74 season in the NBA)</li>  
                <li className="term">DRB%: Defensive Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (DRB * (Tm MP / 5)) / (MP * (Tm DRB + Opp ORB)). Defensive rebound percentage is an estimate of the percentage of available defensive rebounds a player grabbed while he was on the floor.</li>  
                <li className="term">DRtg: Defensive Rating (available since the 1973-74 season in the NBA); for players and teams it is points allowed per 100 posessions. This rating was developed by Dean Oliver, author of Basketball on Paper. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.</li>  
                <li className="term">eFG%: Effective Field Goal Percentage; the formula is (FG + 0.5 * 3P) / FGA. This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal. For example, suppose Player A goes 4 for 10 with 2 threes, while Player B goes 5 for 10 with 0 threes. Each player would have 10 points from field goals, and thus would have the same effective field goal percentage (50%).</li>  
                <li className="term">FG: Field Goals (includes both 2-point field goals and 3-point field goals)</li>  
                <li className="term">FG%: Field Goal Percentage; the formula is FG / FGA.</li>  
                <li className="term">FGA: Field Goal Attempts (includes both 2-point field goal attempts and 3-point field goal attempts)</li>  
                <li className="term">FT: Free Throws</li>  
                <li className="term">FT%: Free Throw Percentage; the formula is FT / FTA.</li>  
                <li className="term">FTA: Free Throw Attempts</li>  
                <li className="term">G: Games</li>  
                <li className="term">GB: Games Behind; the formula is ((first W - W) + (L - first L)) / 2, where first W and first L stand for wins and losses by the first place team, respectively.</li>  
                <li className="term">GmSc: Game Score; the formula is PTS + 0.4 * FG - 0.7 * FGA - 0.4*(FTA - FT) + 0.7 * ORB + 0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV. Game Score was created by John Hollinger to give a rough measure of a player's productivity for a single game. The scale is similar to that of points scored, (40 is an outstanding performance, 10 is an average performance, etc.).</li>  
                <li className="term">GS: Games Started (available since the 1982 season)</li>  
                <li className="term">L: Losses</li>  
                <li className="term">MVP: Most Valuable Player</li>  
                <li className="term">MP: Minutes Played (available since the 1951-52 season)</li>  
                <li className="term">MOV: Margin of Victory; the formula is PTS - Opp PTS.</li>  
                <li className="term">ORtg: Offensive Rating (available since the 1977-78 season in the NBA); for players it is points produced per 100 posessions, while for teams it is points scored per 100 possessions. This rating was developed by Dean Oliver, author of Basketball on Paper. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.</li>  
                <li className="term">Opp: Opponent</li>  
                <li className="term">ORB: Offensive Rebounds (available since the 1973-74 season in the NBA)</li>  
                <li className="term">ORB%: Offensive Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (ORB * (Tm MP / 5)) / (MP * (Tm ORB + Opp DRB)). Offensive rebound percentage is an estimate of the percentage of available offensive rebounds a player grabbed while he was on the floor.</li>  
                <li className="term">Pace: Pace Factor (available since the 1973-74 season in the NBA); the formula is 48 * ((Tm Poss + Opp Poss) / (2 * (Tm MP / 5))). Pace factor is an estimate of the number of possessions per 48 minutes by a team. (Note: 40 minutes is used in the calculation for the WNBA.)</li>  
                <li className="term">Per : Minutes - A statistic (e.g., assists) divided by minutes played, multiplied by 36.</li>  
                <li className="term">Per Ga: - A statistic (e.g., assists) divided by games.</li>  
                <li className="term">PF: Personal Fouls</li>  
                <li className="term">Poss: Possessions (available since the 1973-74 season in the NBA); the formula for teams is 0.5 * ((Tm FGA + 0.4 * Tm FTA - 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA - Tm FG) + Tm TOV) + (Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA - Opp FG) + Opp TOV)). This formula estimates possessions based on both the team's statistics and their opponent's statistics, then averages them to provide a more stable estimate. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.</li>  
                <li className="term">PProd: Points Produced; Dean Oliver's measure of offensive points produced. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.</li>  
                <li className="term">PTS: Points</li>  
                <li className="term">ROY: Rookie of the Year</li>  
                <li className="term">SMOY: Sixth Man of the Year</li>  
                <li className="term">SOS: Strength of Schedule; a rating of strength of schedule. The rating is denominated in points above/below average, where zero is average. My colleague Doug Drinen of Pro-Football-Reference.com has written a great explanation of this method.</li>  
                <li className="term">SRS: Simple Rating System; a rating that takes into account average point differential and strength of schedule. The rating is denominated in points above/below average, where zero is average. My colleague Doug Drinen of Pro-Football-Reference.com has written a great explanation of this method.</li>  
                <li className="term">STL: Steals (available since the 1973-74 season in the NBA)</li>  
                <li className="term">STL%: Steal Percentage (available since the 1973-74 season in the NBA); the formula is 100 * (STL * (Tm MP / 5)) / (MP * Opp Poss). Steal Percentage is an estimate of the percentage of opponent possessions that end with a steal by the player while he was on the floor.</li>  
                <li className="term">Stops: Stops; Dean Oliver's measure of individual defensive stops. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.</li>  
                <li className="term">Tm: Team</li>  
                <li className="term">TOV: Turnovers (available since the 1977-78 season in the NBA)</li>  
                <li className="term">TOV%: Turnover Percentage (available since the 1977-78 season in the NBA); the formula is 100 * TOV / (FGA + 0.44 * FTA + TOV). Turnover percentage is an estimate of turnovers per 100 plays.</li>  
                <li className="term">TRB: Total Rebounds (available since the 1950-51 season)</li>  
                <li className="term">TRB%: Total Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (TRB * (Tm MP / 5)) / (MP * (Tm TRB + Opp TRB)). Total rebound percentage is an estimate of the percentage of available rebounds a player grabbed while he was on the floor.</li>  
                <li className="term">TS%: True Shooting Percentage; the formula is PTS / (2 * TSA). True shooting percentage is a measure of shooting efficiency that takes into account field goals, 3-point field goals, and free throws.</li>  
                <li className="term">TSA: True Shooting Attempts; the formula is FGA + 0.44 * FTA.</li>  
                <li className="term">Usg%: Usage Percentage (available since the 1977-78 season in the NBA); the formula is 100 * ((FGA + 0.44 * FTA + TOV) * (Tm MP / 5)) / (MP * (Tm FGA + 0.44 * Tm FTA + Tm TOV)). Usage percentage is an estimate of the percentage of team plays used by a player while he was on the floor.</li>  
                <li className="term">VORP: Value Over Replacement Player (available since the 1973-74 season in the NBA); a box score estimate of the points per 100 TEAM possessions that a player contributed above a replacement-level (-2.0) player, translated to an average team and prorated to an 82-game season. Multiply by 2.70 to convert to wins over replacement. Please see the article About Box Plus/Minus (BPM) for more information.</li>  
                <li className="term">W: Wins</li>  
                <li className="term">W:% Won-Lost Percentage; the formula is W / (W + L).</li>  
                <li className="term">WS: Win Shares; an estimate of the number of wins contributed by a player. Please see the article Calculating Win Shares for more information.</li>  
                <li className="term">WS/: Win Shares Per 48 Minutes (available since the 1951-52 season in the NBA); an estimate of the number of wins contributed by the player per 48 minutes (league average is approximately 0.100). Please see the article Calculating Win Shares for more information.</li>  
                <li className="term">Win Probability: The estimated probability that Team A will defeat Team B in a given matchup.</li>  
                <li className="term">Year: Year that the season occurred. Since the NBA season is split over two calendar years, the year given is the last year for that season. For example, the year for the 1999-00 season would be 2000.</li>  
            </ul>      
        </div>
    );
}
