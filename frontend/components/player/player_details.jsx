import React from 'react';
import { Link } from "react-router-dom";
import { yearToSeason } from "../../util/util";
import StatBox from "../elements/stat_box";

export default class PlayerDetails extends React.Component {
    constructor(props) {
        super(props);
    }

    renderBasicInfo() {
        let { person, height , weight } = this.props.player;
        
        height /= 2.54; // convert cm to in
        weight = parseInt(weight * 2.2); // convert kg to lbs
        const feet = Math.floor(height/12);
        const inches = parseInt(height) % 12;
        
        let { dob, college } = person;
        const dobDate = new Date(dob);
        const age = Math.floor((new Date()-dobDate)/31536000000); // convert ms to years
        const birthDate = `${dobDate.getUTCMonth()+1}/${dobDate.getUTCDate()}/${dobDate.getUTCFullYear()}`;
        const collegeLi = college ?  
            <li className="info-item">
                <strong>College: </strong>{college}
            </li> :
            null;
        return(
            <div className="player-info-right">
                <ul>
                    <li className="info-item">
                        <strong>Height: </strong>{feet}'{inches}"
                    </li>
                    <li className="info-item">
                        <strong>Weight: </strong>{weight} lbs
                    </li>
                    <li className="info-item">
                        <strong>Age: </strong>{age} (Born {birthDate}) 
                    </li>
                    {collegeLi}
                </ul>
            </div>
        );
    }

    render() {
        const { team, player, totalStats, year } = this.props;
        const { person, positions, imageUrl } = player;
        const { preferredName, lastName } = person;
        let uniquePositions = positions;
        const isLongerThanOne = el => el.length > 1;
        if (positions.some(isLongerThanOne));
            uniquePositions = positions.filter(isLongerThanOne).join(", ");
        const { id, city, name, abbreviation } = team;
        const boxHeader = year === 0 ? "Career" : `${yearToSeason(year)} Season`;
        return (
            <div className={`${abbreviation}-theme container`}>
                <div className="level">
                    <div className="level-left">
                        <div className="level-item">
                            <figure>
                                <img className="player-image" src={imageUrl} />
                            </figure>
                            <figure className="current-team-logo">
                                <img src={`/static/images/logos/${abbreviation}.svg`} />
                            </figure>
                        </div>
                        <div className="level-item">
                            <div className="player-info-left">
                                <p className="preferred-name">{preferredName}</p>
                                <p className="last-name">{lastName}</p>
                                <p className="positions">{uniquePositions}</p>
                                <Link to={`/teams/${id}`} className="current-team">{city} {name}</Link>
                            </div>
                        </div>
                        <div className="level-item">
                            {this.renderBasicInfo()}
                        </div>
                    </div>
                    <div className="level-right">
                        <StatBox
                            boxHeader = {boxHeader}
                            stats={totalStats} 
                            positions={positions} />
                    </div>
                </div>
            </div>
        );
    }
}