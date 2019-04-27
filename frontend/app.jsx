import React from 'react';
import { Switch, Route, Link } from "react-router-dom";
import Teams from './components/team/teams';
import Team from './components/team/team';
import Splash from "./components/splash";
import Navbar from "./components/navbar";
import Breadcrumb from "./components/breadcrumb";
import Footer from "./components/footer";
import Player from "./components/player/player";
import Players from "./components/player/players";

const App = () => {
    return(
        <>
        <section className="section is-paddingless">
            <Navbar/>
            <Route component={Breadcrumb}/>
        </section>
        <Switch>
            <Route exact path="/" component={Splash}/>
            <Route exact path="/teams" component={Teams}/>
            <Route exact path="/teams/:id" component={Team}/>
            <Route exact path="/players" component={Players}/>
            <Route exact path="/players/:id" component={Player}/>
        </Switch>
        <Footer/>
        </>
    );
};

export default App;