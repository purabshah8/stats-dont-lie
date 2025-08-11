import React, { useEffect, useState } from 'react';
import { Link, useLocation } from "react-router-dom";
import { useQuery } from "@apollo/client";
import { GET_TEAM, GET_PLAYER } from "../../util/queries";

function PlayerBreadcrumbItem({ playerId, path, isActive }) {
    const { loading, data } = useQuery(GET_PLAYER, {
        variables: { playerId: parseInt(playerId) }
    });

    if (loading) return null;

    const { preferredName, lastName } = data.player.person;
    const playerName = preferredName + " " + lastName;

    return (
        <li className={isActive ? "is-active" : ""}>
            <Link to={`/players/${playerId}`}>
                {playerName}
            </Link>
        </li>
    );
}

function TeamBreadcrumbItem({ teamId, path, isActive }) {
    const { loading, data } = useQuery(GET_TEAM, {
        variables: { teamId: parseInt(teamId) }
    });

    if (loading) return null;

    const { city, name, abbreviation } = data.team;
    const teamName = city + " " + name;

    return (
        <li className={isActive ? "is-active" : ""}>
            <Link to={`/teams/${teamId}`}>
                <span className="icon is-small">
                    <img src={`/static/images/logos/${abbreviation}.svg`}/>
                </span>
                <span>{teamName}</span>
            </Link>
        </li>
    );
}

export default function Breadcrumb() {
    const location = useLocation();
    const [listItems, setListItems] = useState([]);
    
    const isActiveLink = (link) => location.pathname === link;

    useEffect(() => {
        const pathItems = location.pathname.split("/");
        const newListItems = [];

        const allListItems = {
            teams: (
                <li className={isActiveLink("/teams") ? "is-active" : ""} key="teams">
                    <Link to="/teams">
                        <span className="icon is-small">
                            <img src="/static/images/logos/NBA.svg"/>
                        </span>
                        <span>Teams</span>
                    </Link>
                </li>
            ),
            players: (
                <li className={isActiveLink("/players") ? "is-active" : ""} key="players">
                    <Link to="/players">
                        <span className="icon is-small">
                            <i className="fas fa-user"></i>
                        </span>
                        <span>Players</span>
                    </Link>
                </li>
            )
        };

        pathItems.forEach((item, idx) => {
            if (allListItems[item]) {
                newListItems.push(allListItems[item]);
            }
            if (item && !isNaN(item)) {
                const id = parseInt(item);
                const property = pathItems[idx - 1];
                const isActive = isActiveLink(location.pathname);

                if (property === "teams") {
                    newListItems.push(
                        <TeamBreadcrumbItem 
                            key={`team-${id}`}
                            teamId={id} 
                            path={location.pathname}
                            isActive={isActive} 
                        />
                    );
                } else if (property === "players") {
                    newListItems.push(
                        <PlayerBreadcrumbItem 
                            key={`player-${id}`}
                            playerId={id} 
                            path={location.pathname}
                            isActive={isActive} 
                        />
                    );
                }
            }
        });

        setListItems(newListItems);
    }, [location.pathname]);

    if (location.pathname === "/") {
        return null;
    }

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
                    {listItems}
                </ul>
            </nav>
        </div>
    );
}
