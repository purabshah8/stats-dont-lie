import React from 'react';
import { Query } from "react-apollo";
import { GET_NAV_STATE } from '../util/queries';
import { Link } from "react-router-dom";
import { ApolloConsumer } from 'react-apollo';


export default class Navbar extends React.Component {
    constructor(props) {
        super(props);
        // this.state = {
        //     theme: "default",
        //     navMenuIsActive: false,
        // };
        // this.updateNavState();
        // this.burgerClasses = "navbar-burger";
        // this.menuClasses = "navbar-menu";
        // this.toggleActive = this.toggleActive.bind(this);
    }

    // updateNavState() {
    //     let navState;
    //     let queryComponent = <Query query={GET_NAV_STATE}>
    //         {
    //             ({loading, error, data}) => {
    //                 debugger;
    //                 navState = data;
    //             }
    //         }
    //     </Query>;
    //     debugger;
    //     this.state = navState;
    // }

    render() {
        return(
            <ApolloConsumer>
                {
                    client => {
                        const { navMenuIsActive, theme } = client.readQuery({query: GET_NAV_STATE});
                        let activeStr = navMenuIsActive ? "is-active" : "";
                        const toggleNavMenu = () => {
                            client.writeQuery({ 
                                query: GET_NAV_STATE,
                                data: { 
                                    theme,
                                    navMenuIsActive: !navMenuIsActive,
                                }
                            });
                        };
                        return(
                            <nav className={`navbar is-fixed-top ${theme}-theme`}>
                                <div className="navbar-brand">
                                    <Link className="navbar-item" to="/">Stats Don't Lie</Link>
                                    <a role="button" aria-label="menu" aria-expanded="false"
                                        className={`navbar-menu ${activeStr}`}
                                        onClick={toggleNavMenu}
                                        data-target="mainNavbar">
                                        
                                        <span aria-hidden="true"></span>
                                        <span aria-hidden="true"></span>
                                        <span aria-hidden="true"></span>
                                    </a>
                                </div>
                                <div id="mainNavbar" className={`navbar-burger ${activeStr}`}>
                                    <div className="navbar-start">
                                        <Link className="navbar-item" to="/teams">Teams</Link>
                                        <Link className="navbar-item" to="#">Players</Link>
                                        <Link className="navbar-item" to="">Seasons</Link>
                                    </div>
                                    <div className="navbar-end">
                                        
                                    </div>
                                </div>
                            </nav>
                        );
                    }
                }
            </ApolloConsumer>
        );
    }
    
    // toggleActive(e) {
    //     this.setState({isActive: !this.state.isActive});
    // }
    
    // render() {
    //     let menuClasses = "navbar-burger";
    //     debugger;
    //     menuClasses += this.state.isActive ? " is-active" : "";
    //     this.burgerClasses = this.state.isActive ? "navbar-burger is-active" : "navbar-burger";
    //     this.menuClasses = this.state.isActive ? "navbar-menu is-active" : "navbar-menu";
    //     this.navClasses = ;
    //     return (
    //         <nav className={this.navClasses}>
    //             <div className="navbar-brand">
    //                 <Link className="navbar-item" to="/">Stats Don't Lie</Link>
    //                 {this.renderMenu()}
    //             </div>
    //             <div id="mainNavbar" className={this.menuClasses}>
    //                 <div className="navbar-start">
    //                     <Link className="navbar-item" to="/teams">Teams</Link>
    //                     <Link className="navbar-item" to="#">Players</Link>
    //                 </div>
    //                 <div className="navbar-end">
                        
    //                 </div>
    //             </div>
    //         </nav>

    //     );
    // }

}