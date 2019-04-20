import React from 'react';
import { Switch, Route, Link } from "react-router-dom";
import Teams from './components/teams';
import Team from './components/team';
import Splash from "./components/splash";
import Navbar from "./components/navbar";
import Player from "./components/player/player";

const App = () => {
    return(
        <>
        <Navbar/>
        <Switch>
            <Route exact path="/" component={Splash}/>
            <Route exact path="/teams" component={Teams} />
            <Route exact path="/teams/:id" component={Team} />
            <Route exact path="/players/:id" component={Player} />
        </Switch>
        </>
    );
};

export default App;