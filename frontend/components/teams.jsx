import React from 'react';
import { Query } from "react-apollo";
import { ApolloConsumer } from 'react-apollo';
import { GET_ALL_TEAMS } from '../util/queries';
import { Link } from "react-router-dom";

const divisions = ["Atlantic", "Central", "Southeast", "Southwest", "Northwest", "Pacific"];
const conferences = ["Eastern Conference", "Western Conference"];

const Teams = () => {
    return(
        <div className="container">
            <h2 className="title has-text-centered">NBA Teams</h2>
            <Query query={GET_ALL_TEAMS} >
            {
                ({loading, error, data}) => {
                    if (loading) return 'Loading...';
                    if (error) return `Error! ${error.message}`;
                    
                    return(
                        <div className="columns is-multiline is-centered is-tablet">
                            {
                                data.allTeams.map((team, i) => (
                                    <>
                                    {
                                        i % 5 === 0 ? 
                                            <div key={"division-"+i}
                                            className="column is-full is-centered has-text-centered">
                                                <h2 className="title">{divisions[i/5]} Division</h2>
                                            </div> : null
                                    }
                                    <div className="column is-one-fifth" key={team.id}>
                                        <Link className="link is-flexed" to={`teams/${team.id}`}>
                                            <figure className="image">
                                                <img className="team-logo" 
                                                    src={`/static/images/logos/${team.abbreviation}_logo.svg`}/>
                                            </figure>
                                        </Link>
                                    </div>
                                    </>
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