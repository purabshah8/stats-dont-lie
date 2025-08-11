import React from 'react';
import { useQuery, useApolloClient } from "@apollo/client";
import { GET_NAV_STATE } from '../../util/queries';
import { Link } from "react-router-dom";
import { navMenuIsActiveVar } from '../../root';


const Navbar = () => {
    const { data } = useQuery(GET_NAV_STATE);
    const { navMenuIsActive, theme } = data || { navMenuIsActive: false, theme: 'default' };
    let activeStr = navMenuIsActive ? "is-active" : "";
    
    const toggleNavMenu = () => {
        navMenuIsActiveVar(!navMenuIsActive);
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
                        {/* <Link onClick={toggleNavMenu} className="navbar-item" to="/games">Games</Link> */}
                    </div>
                    <div className="navbar-end">
                        
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Navbar;