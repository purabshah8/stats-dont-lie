import React from 'react';

export default class Splash extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div className="section">
                <div className="title has-text-centered">Stats Don't Lie</div>
                <div className="subtitle has-text-centered is-6">Explore NBA stats using D3</div>
                
                <div className="container">
                    <div className="title is-4">2018-19 Team Stats</div>
                </div>
            </div>

        );
    }

}