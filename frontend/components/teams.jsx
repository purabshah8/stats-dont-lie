import React from 'react';
import gql from "graphql-tag";
import { Query } from "react-apollo";

const GET_ALL_TEAMS = gql `
    query {
        allTeams {
            city
            name
        }
    }
`;

const Teams = () => {
    return(
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
                                    {team.city + ' ' + team.name}
                                </li>
                            ))
                        }
                    </ul>
                );
            }
        }
        </Query>
    );
};

export default Teams;