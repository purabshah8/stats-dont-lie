import React from 'react';
import { Query } from "react-apollo";
import { GET_NAV_STATE } from '../util/queries';
import { Link } from "react-router-dom";


export default class Navbar extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <Query query={GET_NAV_STATE}>
                {
                    ({data, client}) => {
                        const { navMenuIsActive, theme } = data;
                        let activeStr = navMenuIsActive ? "is-active" : "";
                        const toggleNavMenu = () => {
                            client.writeData({ 
                                data: { 
                                    theme,
                                    navMenuIsActive: !navMenuIsActive,
                                }
                            });
                        };
                        return(
                            <div className={`${theme}-theme`}>
                                <nav className="navbar is-fixed-top">
                                    <div className="navbar-brand">
                                        <Link onClick={toggleNavMenu} className="navbar-item" to="/">Stats Don't Lie</Link>
                                        <a role="button" aria-label="menu" aria-expanded="false"
                                            className={`navbar-burger ${activeStr}`}
                                            onClick={toggleNavMenu}
                                            data-target="mainNavbar">
                                            
                                            <span aria-hidden="true"></span>
                                            <span aria-hidden="true"></span>
                                            <span aria-hidden="true"></span>
                                        </a>
                                    </div>
                                    <div id="mainNavbar" className={`navbar-menu ${activeStr}`}>
                                        <div className="navbar-start">
                                            <Link onClick={toggleNavMenu} className="navbar-item" to="/teams">Teams</Link>
                                            <Link onClick={toggleNavMenu} className="navbar-item" to="/players">Players</Link>
                                            <Link onClick={toggleNavMenu} className="navbar-item" to="#">Seasons</Link>
                                        </div>
                                        <div className="navbar-end">
                                            
                                        </div>
                                    </div>
                                </nav>
                            </div>
                        );
                    }
                }
            </Query>
        );
    }
}