import React from 'react';
import PlayerDetails from "./player_details";

export default class Player extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="section">
                <PlayerDetails playerId={this.props.match.params.id} />
            </div>
        );
    }
}