import React from 'react';

//  <li className="entry"><div className="term"></div> <div></div></li>

export default function Glossary() {
    return (
        <div className="container is-flexed">
            <div className="title">Glossary</div>
            <ul className="terms">
                <li className="entry"><div className="term">2P</div> <div>2-Point Field Goals</div></li>
                <li className="entry"><div className="term">2P%</div> <div>2-Point Field Goal Percentage<br/><span>Formula:</span> 2P / 2PA.</div></li>
                <li className="entry"><div className="term">2PA</div> <div>2-Point Field Goal Attempts</div></li>
                <li className="entry"><div className="term">3P</div> <div>3-Point Field Goals</div></li>
                <li className="entry"><div className="term">3P%</div> <div>3-Point Field Goal Percentage<br/><span>Formula:</span> 3P / 3PA.</div></li>
                <li className="entry"><div className="term">3PA</div> <div>3-Point Field Goal Attempts</div></li>
                <li className="entry"><div className="term">Age</div> <div>Player age on February 1 of the given season.</div></li>
                <li className="entry"><div className="term">AST</div> <div>Assists</div></li>
                <li className="entry"><div className="term">AST%</div> <div>Assist Percentage; Assist percentage is an estimate of the percentage of teammate field goals a player assisted while he was on the floor. <br/><span>Formula:</span> 100 * AST / (((MP / (Team MP / 5)) * Team FG) - FG)</div></li>
                <li className="entry"><div className="term">BLK</div> <div>Blocks</div></li>
                <li className="entry"><div className="term">BLK%</div> <div>Block Percentage; Block percentage is an estimate of the percentage of opponent two-point field goal attempts blocked by the player while he was on the floor. <br/><span>Formula:</span> 100 * (BLK * (Team MP / 5)) / (MP * (Opp FGA - Opp 3PA))</div></li>
                <li className="entry"><div className="term">DRB</div> <div>Defensive Rebounds</div></li>
                <li className="entry"><div className="term">DRB%</div> <div>Defensive Rebound Percentage; Defensive rebound percentage is an estimate of the percentage of available defensive rebounds a player grabbed while he was on the floor. <br/><span>Formula:</span> 100 * (DRB * (Team MP / 5)) / (MP * (Team DRB + Opp ORB))</div></li>
                <li className="entry"><div className="term">DRtg</div> <div>Defensive Rating; For players and teams it is an estimation of points allowed per 100 posessions.</div></li>
                <li className="entry"><div className="term">eFG%</div> <div>Effective Field Goal Percentage; This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal.<br/><span>Formula:</span> (FG + 0.5 * 3P) / FGA</div></li>
                <li className="entry"><div className="term">FG</div> <div>Field Goals (includes both 2-point field goals and 3-point field goals)</div></li>
                <li className="entry"><div className="term">FG%</div> <div>Field Goal Percentage; <br/><span>Formula:</span> FG / FGA</div></li>
                <li className="entry"><div className="term">FGA</div> <div>Field Goal Attempts (includes both 2-point field goal attempts and 3-point field goal attempts)</div></li>
                <li className="entry"><div className="term">FT</div> <div>Free Throws</div></li>
                <li className="entry"><div className="term">FT%</div> <div>Free Throw Percentage; <br/><span>Formula:</span> FT / FTA.</div></li>
                <li className="entry"><div className="term">FTA</div> <div>Free Throw Attempts</div></li>
                <li className="entry"><div className="term">G</div> <div>Games</div></li>
                <li className="entry"><div className="term">GS</div> <div>Games Started</div></li>
                <li className="entry"><div className="term">L</div> <div>Losses</div></li>
                <li className="entry"><div className="term">MP</div> <div>Minutes Played</div></li>
                <li className="entry"><div className="term">MOV</div> <div>Margin of Victory; <br/><span>Formula:</span> PTS - Opp PTS.</div></li>
                <li className="entry"><div className="term">ORtg</div> <div>Offensive Rating; for players it is points produced per 100 posessions, while for teams it is points scored per 100 possessions.</div></li>
                <li className="entry"><div className="term">Opp</div> <div>Opponent</div></li>
                <li className="entry"><div className="term">ORB</div> <div>Offensive Rebounds</div></li>
                <li className="entry"><div className="term">ORB%</div> <div>Offensive Rebound Percentage; Offensive rebound percentage is an estimate of the percentage of available offensive rebounds a player grabbed while he was on the floor. <br/><span>Formula:</span> 100 * (ORB * (Team MP / 5)) / (MP * (Team ORB + Opp DRB))</div></li>
                <li className="entry"><div className="term">Pace</div> <div>Pace is an estimate of the number of possessions per 48 minutes by a team. <br/><span>Formula:</span> 48 * ((Team Poss + Opp Poss) / (2 * (Team MP / 5)))</div></li>
                <li className="entry"><div className="term">PF</div> <div>Personal Fouls</div></li>
                <li className="entry"><div className="term">Poss</div> <div>Possessions; An estimation of how many times a team or player controlled the ball. The following formula estimates possessions based on both the team's statistics and their opponent's statistics, then averages them to provide a more stable estimate. <br/><span>Formula:</span> 0.5 * ((Team FGA + 0.4 * Team FTA - 1.07 * (Team ORB / (Team ORB + Opp DRB)) * (Team FGA - Team FG) + Team TOV) + (Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Team DRB)) * (Opp FGA - Opp FG) + Opp TOV))</div></li>
                <li className="entry"><div className="term">PTS</div> <div>Points</div></li>
                <li className="entry"><div className="term">STL</div> <div>Steals</div></li>
                <li className="entry"><div className="term">STL%</div> <div>Steal Percentage; Steal Percentage is an estimate of the percentage of opponent possessions that end with a steal by the player while he was on the floor.  <br/><span>Formula:</span> 100 * (STL * (Team MP / 5)) / (MP * Opp Poss)</div></li>
                <li className="entry"><div className="term">TOV</div> <div>Turnovers</div></li>
                <li className="entry"><div className="term">TOV%</div> <div>Turnover Percentage; Turnover percentage is an estimate of turnovers per 100 plays. <br/><span>Formula:</span> 100 * TOV / (FGA + 0.44 * FTA + TOV)</div></li>
                <li className="entry"><div className="term">TRB</div> <div>Total Rebounds </div></li>
                <li className="entry"><div className="term">TRB%</div> <div>Total Rebound Percentage; Total rebound percentage is an estimate of the percentage of available rebounds a player grabbed while he was on the floor. <br/><span>Formula:</span> 100 * (TRB * (Team MP / 5)) / (MP * (Team TRB + Opp TRB))</div></li>
                <li className="entry"><div className="term">TS%</div> <div>True Shooting Percentage; True shooting percentage is a measure of shooting efficiency that takes into account field goals, 3-point field goals, and free throws. <br/><span>Formula:</span> PTS / (2 * TSA)</div></li>
                <li className="entry"><div className="term">TSA</div> <div>True Shooting Attempts; <br/><span>Formula:</span> FGA + 0.44 * FTA.</div></li>
                <li className="entry"><div className="term">Usg Rate</div> <div>Usage Rate; Usage rate is an estimate of the percentage of team plays used by a player while he was on the floor. <br/><span>Formula:</span> 100 * ((FGA + 0.44 * FTA + TOV) * (Team MP / 5)) / (MP * (Team FGA + 0.44 * Team FTA + Team TOV))</div></li>
                <li className="entry"><div className="term">W</div> <div>Wins</div></li>
                <li className="entry"><div className="term">W-L%</div> <div>Won-Lost Percentage; <br/><span>Formula:</span> W / (W + L).</div></li>
                <li className="entry"><div className="term">Year</div> <div>Year that the season occurred. Since the NBA season is split over two calendar years, the year given is the last year for that season.</div></li>
            </ul>      
        </div>
    );
}


