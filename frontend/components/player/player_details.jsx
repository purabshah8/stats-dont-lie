import React from 'react';
import { Query } from "react-apollo";
import { Link } from "react-router-dom";
import { GET_PLAYER } from '../../util/queries';
import { range } from "lodash";

export default class PlayerDetails extends React.Component {
    constructor(props) {
        super(props);
    }

    renderBasicInfo() {
        const { player } = this.props.data;
        const person = player.person;
        const height = player.height / 2.54; // convert cm to in
        const feet = Math.floor(height/12);
        const inches = parseInt(height) % 12;
        const weight = parseInt(player.weight * 2.2); // convert kg to lbs
        const dob = new Date(person.dob);
        const age = Math.floor((new Date()-dob)/31536000000); // convert ms to years
        const birthDate = `${dob.getUTCMonth()+1}/${dob.getUTCDate()}/${dob.getUTCFullYear()}`;
        const collegeLi = person.college ?  
            <li className="info-item">
                <strong>College: </strong>{person.college}
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
        const { player } = this.props.data;
        const person = player.person;
        const currentTeam = player.currentTeam;
        let positions = player.positions;
        const isLongerThanOne = el => el.length > 1;
        if (positions.some(isLongerThanOne));
            positions = positions.filter(isLongerThanOne).join(", ");
        return (
            <div className="container">
                <div className="level">
                    <div className="level-left">
                        <div className="level-item">
                            <figure>
                                <img src={player.imageUrl} />
                            </figure>
                            <figure className="current-team-logo">
                                <img src={`/static/images/logos/${currentTeam.abbreviation}_logo.svg`} />
                            </figure>
                        </div>
                        <div className="level-item">
                            <div className="player-info-left">
                                <p className="preferred-name">{person.preferredName}</p>
                                <p className="last-name">{person.lastName}</p>
                                <p className="positions">{positions}</p>
                                <p className="current-team">{currentTeam.city} {currentTeam.name}</p>
                            </div>
                        </div>
                        <div className="level-item">
                            {this.renderBasicInfo()}
                        </div>
                    </div>
                    <div className="level-right">
                    </div>
                </div>
            </div>
        );
    }

    // render() {
    //     return (
    //         <div className="container">
    //             <Query query={GET_PLAYER} variables={ { playerId: this.props.playerId } }>
    //                 {
    //                     ({loading, error, data}) => {
    //                         if (loading) return 'Loading...';
    //                         if (error) return `Error! ${error.message}`;                            
    //                         let player = data.player;
    //                         let person = data.player.person;
    //                         const currentTeam = player.currentTeam;
    //                         let rookieSeason = player.rookieSeason.year;
    //                         let finalSeason;
    //                         if (data.player.finalSeason)
    //                             finalSeason = player.finalSeason.year;
    //                         else
    //                             finalSeason = 2019;
    //                         let seasons = range(rookieSeason, finalSeason+1);
    //                         seasons = seasons.map(season => {
    //                             let startYear = season-1;
    //                             let endYear = season - 2000;
    //                             if (endYear < 0)
    //                                 endYear += 100;
    //                             return(
    //                                 <option key={season}>
    //                                     {startYear + "-" + endYear}
    //                                 </option>
    //                             );
    //                         });
    //                         const height = player.height / 2.54; // convert cm to inches
    //                         const feet = Math.floor(height/12);
    //                         const inches = parseInt(height) % 12;
    //                         const weight = parseInt(player.weight * 2.2); // convert kg to lbs
    //                         const today = new Date();
    //                         const dob = new Date(person.dob);
    //                         const age = Math.floor((today-dob)/31536000000); // convert ms to years
    //                         const collegeLi = person.college ?  <li className="info-item">
    //                                                                 <strong>College: </strong>{person.college}
    //                                                             </li> : null;
    //                         let positions = player.positions;
    //                         const isLongerThanOne = el => el.length > 1;
    //                         if (positions.some(isLongerThanOne));
    //                             positions = positions.filter(isLongerThanOne).join(", ");
    //                         return(
    //                             <> 
    //                                 <div className="level">
    //                                     <div className="level-left">
    //                                         <div className="level-item">
    //                                             <figure>
    //                                                 <img src={player.imageUrl} />
    //                                             </figure>
    //                                             <figure className="current-team-logo">
    //                                                 <img src={`/static/images/logos/${currentTeam.abbreviation}_logo.svg`} />
    //                                             </figure>
    //                                         </div>
    //                                         <div className="level-item">
    //                                             <div className="player-info-left">
    //                                                 <p className="preferred-name">{person.preferredName}</p>
    //                                                 <p className="last-name">{person.lastName}</p>
    //                                                 <p className="positions">{positions}</p>
    //                                                 <p className="current-team">{currentTeam.city} {currentTeam.name}</p>
    //                                             </div>
    //                                         </div>
    //                                         <div className="level-item">
    //                                             <div className="player-info-right">
    //                                                 <ul>
    //                                                     <li className="info-item">
    //                                                        <strong>Height: </strong>{feet}'{inches}"
    //                                                     </li>
    //                                                     <li className="info-item">
    //                                                        <strong>Weight: </strong>{weight} lbs
    //                                                     </li>
    //                                                     <li className="info-item">
    //                                                        <strong>Age: </strong>{age} (Born {dob.getUTCMonth()+1}/{dob.getUTCDate()}/{dob.getUTCFullYear()}) 
    //                                                     </li>
    //                                                     {collegeLi}
    //                                                 </ul>
    //                                             </div>
    //                                         </div>
    //                                     </div>
    //                                     <hr></hr>
    //                                     <div className="level-right">
    //                                     </div>
    //                                 </div>
    //                                 <div className="select">
    //                                     <select className="">
    //                                         <option disabled selected>Select Season</option>
    //                                         {seasons}
    //                                     </select>
    //                                 </div>
    //                             </>
    //                         );
    //                     }
    //                 }
    //             </Query>
    //         </div>
    //     );
    // }
}