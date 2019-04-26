import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Query } from "react-apollo";
import { ApolloConsumer } from 'react-apollo';
import { GET_TEAM, GET_ROSTER, GET_THEME } from '../util/queries';

export default class Team extends Component {

    constructor(props) {
        super(props);
        this.state = {
            year: 2019
        };
    }

    updateTheme(theme) {
        return(
            <ApolloConsumer>
                {
                    client => {
                        client.writeData({data: {theme} });
                    }
                }
            </ApolloConsumer>
        );
    }

    renderTeam() {
        return(
        <Query query={GET_TEAM} variables={{ teamId: this.props.match.params.id }}>
            {
                ({loading, error, data}) => {
                    if (loading) return <div className="button large is-loading"></div>;
                    if (error) return <div>Error! ${error.message}</div>;
                    if (data) {
                        debugger;
                        this.updateTheme(data.team.abbreviation);
                        debugger;
                        return(
                            <div className="container">
                                <div className="media">
                                    <figure className="media-left">
                                        <img src={`/static/images/logos/${data.team.abbreviation}_logo.svg`} className="team-logo" />
                                    </figure>
                                    <div className="media-content">
                                        <span>{data.team.city} {data.team.name}</span>
                                        <br/>
                                        <span>{data.team.division.name}</span>
                                        <br/>
                                        <span>Home: {data.team.arena.name}</span>
                                    </div>
                                </div>
                            </div>
                        );
                    }
                }
            }
        </Query>);
    }

    renderRoster() {
        return(
            <Query query={GET_ROSTER} 
                variables={ { teamId: this.props.match.params.id, year: 2019 } }>
                {
                    ({loading, error, data}) => {
                        if (loading) return <div className="button is-loading"></div>;
                        if (error) return <div>Error! ${error.message}</div>;
                        let players;
                        if (data) {
                            players = data.teamSeason.roster.map(datum => {
                                if (!datum.player.imageUrl)
                                    datum.player.imageUrl = "https://www.maxwell.syr.edu/uploadedImages/exed/people/students/IFS_Phase_V/August_2010/unknown-person.png";
                                return(
                                    <div className="column is-one-fifth is-flexed">
                                        <Link key={datum.player.person.id}
                                            to={`/players/${datum.player.person.id}`}
                                            className="link">
                                            <figure className="">
                                                <img src={datum.player.imageUrl} />
                                            </figure>
                                            <div className="is-flexed">
                                                <p className="">{datum.player.person.preferredName}</p>
                                                <p className="">{datum.player.person.lastName}</p>
                                            </div>
                                        </Link>
                                    </div>
                                );
                            });
                        }
                        return(
                            <div className="container">
                                <h2>Roster</h2>
                                <div className="columns is-centered is-mobile is-multiline is-3">
                                    {players}
                                </div>
                            </div>
                        ); 
                    }
                }
            </Query>
        );
    }

    render() {
        return (
            <div className="section">
                {this.renderTeam()}
                {this.renderRoster()}
                <Link to="/teams">Back</Link>
            </div>
        );
    }
}