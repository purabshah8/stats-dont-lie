import React from 'react';
import { Query } from "react-apollo";
import { GET_ALL_TEAMS } from '../util/queries';
import { Link } from "react-router-dom";

const Teams = () => {
    return(
        <div className="page-container">
            <h2 className="title is-centered">NBA Teams</h2>
            <Query query={GET_ALL_TEAMS} >
            {
                ({loading, error, data}) => {
                    if (loading) return 'Loading...';
                    if (error) return `Error! ${error.message}`;
                    
                    return(
                        <div className="columns is-multiline is-mobile is-centered">
                            {
                                data.allTeams.map(team => (
                                    <div className="column is-one-fifth">
                                        <Link className="team-link" to={`teams/${team.id}`}>
                                            <img 
                                                className="team-logo" 
                                                src={`/static/images/logos/${team.abbreviation}_logo.svg`}/>
                                            <div className="team-name">{team.city + ' ' + team.name}</div>
                                        </Link>
                                    </div>
                                ))
                            }
                        </div>
                    );
                }
            }
            </Query>
        </div>
    );
};

export default Teams;