import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Query } from "react-apollo";
import { GET_TEAM, GET_PLAYER } from "../util/queries";

export default class Breadcrumb extends Component {


    constructor(props) {
        super(props);
        this.state = {
            path: this.props.history.location.pathname
        };
        this.listItems = [];
        const teams = <li><Link to="/teams">Teams</Link></li>;
        const players = <li><Link to="/players">Players</Link></li>;
        this.allListItems = { teams, players };
    }

    createPlayerListItem(playerId) {
        return(
            <li>
                {
                    <Query query={GET_PLAYER} variables={{ playerId }}>
                        {
                            ({loading, data}) => {
                                if (loading)
                                    return <progress className="progress" max="100">50%</progress>;
                                const { preferredName, lastName } = data.player.person;
                                const playerName = preferredName + " " + lastName;
                                return(
                                    <Link to={`/players/${playerId}`}>
                                        {playerName}
                                    </Link>
                                );
                            }
                        }
                    </Query>
                }
            </li>
        );
    }

    createTeamListItem(teamId) {
        return(
            <li>
                {
                    <Query query={GET_TEAM} variables={ { teamId } }>
                        {
                            ({loading, data}) => {
                                if (loading)
                                    return <progress className="progress" max="100">50%</progress>;
                                const { city, name } = data.team;
                                const teamName = city + " " + name;
                                return(
                                    <Link to={`/teams/${teamId}`}>
                                        {teamName}
                                    </Link>
                                );
                            }
                        }
                    </Query>
                }
            </li>
        );
    }

    createListItem(property, id) {
        if (property === "teams")
            return this.createTeamListItem(id);
        if (property === "players")
            return this.createPlayerListItem(id);
    }

    populateListItems() {
        this.listItems = [];
        const pathItems = this.state.path.split("/");
        pathItems.forEach((item, idx) => {
            if (this.allListItems[item])
                this.listItems.push(this.allListItems[item]);
            if (item && !isNaN(item)){
                this.listItems.push(this.createListItem(pathItems[idx-1],parseInt(item)));}
        });
    }

    componentWillReceiveProps(nextProps) {
            this.setState({ path: nextProps.history.location.pathname });
    }

    render() {
        this.populateListItems();
        console.log(this.state);
        console.log(this.listItems);
        if (this.state.path === "/")
            return null;
        return (
            <div className="container">
                <nav className="breadcrumb" aria-label="breadcrumbs">
                    <ul>
                        <li><Link to="/">Home</Link></li>
                        {this.listItems}
                    </ul>
                </nav>
            </div>
        );
    }
}
