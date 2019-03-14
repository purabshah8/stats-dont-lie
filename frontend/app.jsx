import React from 'react';
import { Switch, Route, Link } from "react-router-dom";
import Teams from './components/teams';

const App = () => {
    return(
            <Switch>
                <Route exact path="/" component={() => (
                    <>
                    <h1>Stats don't Lie!</h1>
                    <Link to="/teams">Teams</Link>
                    </>
                )}/>
                <Route exact path="/teams" component={Teams} />
            </Switch>
    );
};

export default App;