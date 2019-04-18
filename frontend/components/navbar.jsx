import React from 'react';
import { Link } from "react-router-dom";

export default class Navbar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isActive: false
        };
        this.burgerClasses = "navbar-burger";
        this.menuClasses = "navbar-menu";
        this.toggleActive = this.toggleActive.bind(this);
    }
    
    toggleActive(e) {
        this.setState({isActive: !this.state.isActive});
    }
    
    render() {
        this.burgerClasses = this.state.isActive ? "navbar-burger is-active" : "navbar-burger";
        this.menuClasses = this.state.isActive ? "navbar-menu is-active" : "navbar-menu";
        return (
            <nav className="navbar is-fixed-top is-black">
                <div className="navbar-brand">
                    <Link className="navbar-item" to="/">Stats Don't Lie</Link>
                    <a role="button" aria-label="menu" aria-expanded="false"
                        className={this.burgerClasses}
                        onClick={this.toggleActive} data-target="mainNavbar">
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                    </a>
                </div>
                <div id="mainNavbar" className={this.menuClasses}>
                    <div className="navbar-start">
                        <Link className="navbar-item" to="/teams">Teams</Link>
                        <Link className="navbar-item" to="#">Players</Link>
                    </div>
                    <div className="navbar-end">
                        
                    </div>
                </div>
            </nav>

        );
    }

}