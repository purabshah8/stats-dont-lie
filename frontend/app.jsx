import React from 'react';
import { Routes, Route } from "react-router-dom";
import Teams from './components/team/teams';
import Team from './components/team/team';
import Splash from "./components/splash";
import Navbar from "./components/elements/navbar";
import Footer from "./components/elements/footer";
import Player from "./components/player/player";
import PlayerSeason from "./components/player/player_season";
import PlayerSearch from "./components/player/player_search";
import Games from "./components/game/games";
import Glossary from './components/elements/glossary';

const App = () => {
    return(
        <>
        <section className="section is-paddingless">
            <Navbar/>
            {/* <Route component={Breadcrumb}/> */}
        </section>
        <Routes>
            <Route path="/" element={<Splash/>}/>
            <Route path="/games" element={<Games/>}/>
            <Route path="/teams" element={<Teams/>}/>
            <Route path="/teams/:id" element={<Team/>}/>
            <Route path="/players" element={<PlayerSearch/>}/>
            <Route path="/players/:id" element={<Player/>}/>
            <Route path="/players/:playerId/seasons/:year" element={<PlayerSeason/>}/>
            <Route path="/glossary" element={<Glossary/>}/>
        </Routes>
        <Footer/>
        </>
    );
};

export default App;