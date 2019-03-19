import React from 'react';
import { Query } from "react-apollo";
import { GET_ALL_TEAMS } from '../util/queries';
import { Link } from "react-router-dom";

const Teams = () => {
    return(
        <div>
            <h2>NBA Teams</h2>
            <Query query={GET_ALL_TEAMS} >
            {
                ({loading, error, data}) => {
                    if (loading) return 'Loading...';
                    if (error) return `Error! ${error.message}`;
                    
                    return(
                        <ul>
                            {
                                data.allTeams.map(team => (
                                    <li>
                                        <Link to={`teams/${team.id}`}>
                                            {team.city + ' ' + team.name}
                                        </Link>
                                    </li>
                                ))
                            }
                        </ul>
                    );
                }
            }
            </Query>
        </div>
    );
};

export default Teams;