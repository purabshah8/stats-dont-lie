import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Query } from "react-apollo";
import { GET_TEAM, GET_ROSTER } from '../../util/queries';
export default class Team extends Component {

    constructor(props) {
        super(props);
        this.state = {
            year: 2019
        };
    }

    renderTeam() {
        return(
        <Query query={GET_TEAM} variables={{ teamId: this.props.match.params.id }}>
            {
                ({loading, error, data, client}) => {
                    if (loading) return <progress className="progress" max="100">50%</progress>;
                    if (error) return <div>Error! ${error.message}</div>;

                    const { team } = data;
                    const { abbreviation, city, name, arena, division } = team;
                    client.writeData({ data: { theme: abbreviation } });
                    return(
                        <div className="container">
                            <div className="level">
                                <div className="level-left">
                                    <div className="level-item">
                                        <figure className="is-square">
                                            <img src={`/static/images/logos/${abbreviation}_logo.svg`} className="team-logo logo-large" />
                                        </figure>
                                    </div>
                                    <div className="level-item is-flexed">
                                        <p className="is-size-2">{city}</p>
                                        <p className="is-size-1">{name}</p>
                                    </div>
                                    <div className="level-item is-flexed">
                                        <p className="is-size-4">{division.name}</p>
                                        <p className="is-size-4">
                                            {division.conference.name}
                                        </p>
                                        <p className="is-size-4">
                                            Home: {arena.name}
                                        </p>
                                    </div>
                                </div>
                                <div className="level-right">

                                </div>
                            </div>
                        </div>
                    );
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
                        if (loading) return <progress className="progress" max="100">50%</progress>;
                        if (error) return <div>Error! ${error.message}</div>;
                        
                        const { teamSeason, theme } = data;
                        const comparePlayers = (a,b) => {
                            const aLast = a.player.person.lastName;
                            const bLast = b.player.person.lastName;
                            if (aLast.toUpperCase() < bLast.toUpperCase())
                                return -1;
                            if (aLast.toUpperCase() > bLast.toUpperCase())
                                return 1;
                            return 0;
                        };
                        teamSeason.roster.sort(comparePlayers);
                        const players = teamSeason.roster.map(datum => {
                                const { player } = datum;
                                let { person, positions, imageUrl } = player;
                                const fullName = person.preferredName + " " + person.lastName;
                                const isLongerThanOne = el => el.length > 1;
                                if (positions.some(isLongerThanOne))
                                    positions = positions.filter(isLongerThanOne);
                                positions = positions.join(", ");
                                if (!imageUrl)
                                    imageUrl = "https://www.maxwell.syr.edu/uploadedImages/exed/people/students/IFS_Phase_V/August_2010/unknown-person.png";
                                return(
                                    <div key={person.id}
                                        className="column is-one-fifth is-flexed zoom-in">
                                        <Link className="link"
                                            to={`/players/${person.id}`}>
                                            <figure className="is-flexed">
                                                <img src={imageUrl} />
                                            </figure>
                                            <div className="is-flexed">
                                                <p className="">{fullName}</p>
                                                <p className="">{positions}</p>
                                            </div>
                                        </Link>
                                    </div>
                                );
                            });
                        return(
                            <div className="container">
                                <h2>Roster</h2>
                                <div className={`columns is-centered is-mobile is-multiline is-3 ${theme}-theme`}>
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