import React from 'react';
import { Switch, Route, Link } from "react-router-dom";
import Teams from './components/team/teams';
import Team from './components/team/team';
import Splash from "./components/splash";
import Navbar from "./components/elements/navbar";
import Breadcrumb from "./components/elements/breadcrumb";
import Footer from "./components/elements/footer";
import Player from "./components/player/player";
import PlayerSeason from "./components/player/player_season";
import PlayerSearch from "./components/player/player_search";

const App = () => {
    return(
        <>
        <section className="section is-paddingless">
            <Navbar/>
            {/* <Route component={Breadcrumb}/> */}
        </section>
        <Switch>
            <Route exact path="/" component={Splash}/>
            <Route exact path="/teams" component={Teams}/>
            <Route exact path="/teams/:id" component={Team}/>
            <Route exact path="/players" component={PlayerSearch}/>
            <Route exact path="/players/:id" component={Player}/>
            <Route exact path="/players/:playerId/seasons/:year" component={PlayerSeason}/>
        </Switch>
        <Footer/>
        </>
    );
};

export default App;