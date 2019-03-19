import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Query } from "react-apollo";
import { getTeam } from '../util/queries';

export default class Team extends Component {

    constructor(props) {
        super(props);

    }

    render() {
        return (
            <div>
                <Query query={getTeam('id', this.props.match.params.id)}>
                    {
                        ({loading, error, data}) => {
                            if (loading) return 'Loading...';
                            if (error) return `Error! ${error.message}`;
                            
                            return(
                                <div>
                                    <h2>{data.team.city + " " + data.team.name}</h2>
                                    <ul>
                                        <li>Division: {data.team.division.name}</li>
                                        <li>Conference: {data.team.division.conference.name}</li>
                                        <li>Arena: {data.team.arena.name}</li>
                                    </ul>
                                    <Link to="/teams">Back</Link>
                                </div>
                            ); 
                        }
                    }
                </Query>
            </div>
        )
    }
}
