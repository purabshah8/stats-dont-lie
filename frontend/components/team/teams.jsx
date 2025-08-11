import React from 'react';
import { useQuery } from "@apollo/client";
import { GET_ALL_TEAMS } from '../../util/queries';
import { Link } from "react-router-dom";
import Loading from '../elements/loading';

const divisions = ["Atlantic", "Central", "Southeast", "Southwest", "Northwest", "Pacific"];

const Teams = () => {
    const { loading, error, data } = useQuery(GET_ALL_TEAMS);
    
    if (loading) return <Loading />;
    if (error) return `Error! ${error.message}`;
    
    return(
        <div className="container">
            <div key="nba-teams" className="columns is-multiline is-centered is-mobile is-vcentered">
                {
                    data.allTeams.map((team, i) => (
                        <React.Fragment key={i}>
                            {
                                i % 5 === 0 ? 
                                    <div key={divisions[i/5]}
                                    className="column is-full is-centered has-text-centered">
                                        <h2 className="title">{divisions[i/5]} Division</h2>
                                    </div> : null
                            }
                            <div className="column is-one-fifth-desktop is-one-fifth-fullhd is-one-fifth-widescreen is-full-mobile is-one-fifth-tablet team-tile" key={team.id}>
                                <Link className="is-flexed" to={`/teams/${team.id}`}>
                                    <figure className="is-square">
                                        <img className="team-logo" 
                                            alt={`${team.city} ${team.name}`}
                                            src={`https://statsdontlie-media.s3.amazonaws.com/${team.abbreviation}.svg`}/>
                                    </figure>
                                </Link>
                            </div>
                        </React.Fragment>
                    ))
                }
            </div>
        </div>
    );
};

export default Teams;