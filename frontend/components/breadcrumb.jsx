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
        
    }

    liClassCreator(link, className="") {
        if (this.state.path === link)
            return className + " is-active";
        return className;
    }

    createPlayerListItem(playerId) {
        return(
            <li className={this.liClassCreator(`/players/${playerId}`)} key={`player-${playerId}`}>
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
            <li className={this.liClassCreator(`/teams/${teamId}`)} key={`team-${teamId}`}>
                {
                    <Query query={GET_TEAM} variables={ { teamId } }>
                        {
                            ({loading, data}) => {
                                if (loading)
                                    return <progress className="progress" max="100">50%</progress>;
                                const { city, name, abbreviation } = data.team;
                                const teamName = city + " " + name;
                                return(
                                    <Link to={`/teams/${teamId}`}>
                                        <span className="icon is-small">
                                            <img src={`/static/images/logos/${abbreviation}_logo.svg`}/>
                                        </span>
                                        <span>{teamName}</span>
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
        const teams = 
            <li className={this.liClassCreator("/teams")} key="teams">
                <Link to="/teams">
                    <span className="icon is-small">
                        <img src="/static/images/logos/NBA_logo.svg"/>
                    </span>
                    <span>Teams</span>
                </Link>
            </li>;
        const players = 
            <li className={this.liClassCreator("/players")} key="players">
                <Link to="/players">
                    <span className="icon is-small">
                        <i className="fas fa-user"></i>
                    </span>
                    <span>Players</span>
                </Link>
            </li>;
        this.allListItems = { teams, players };
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

        if (this.state.path === "/")
            return null;
        return (
            <div id="bc-container" className="container is-hidden-mobile">
                <nav className="breadcrumb is-medium has-succeeds-separator" aria-label="breadcrumbs">
                    <ul>
                        <li>
                            <Link to="/">
                            <span className="icon is-small">
                                <i className="fas fa-basketball-ball"></i>
                            </span>
                            <span>Stats Don't Lie</span>
                            </Link>
                        </li>
                        {this.listItems}
                    </ul>
                </nav>
            </div>
        );
    }
}
