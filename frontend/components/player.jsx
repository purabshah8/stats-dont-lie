import React from 'react';
import { Query } from "react-apollo";
import { Link } from "react-router-dom";
import { GET_PLAYER} from '../util/queries';

export default class Player extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Query query={GET_PLAYER} variables={ { playerId: this.props.match.params.id } }>
                    {
                        ({loading, error, data}) => {
                            if (loading) return 'Loading...';
                            if (error) return `Error! ${error.message}`;
                            let partial;
                            if (data) {
                                let player = data.player;
                                let person = data.player.person;
                                partial = <div className="container">
                                            <div className="name">
                                                {person.preferredName} {person.lastName}
                                            </div>
                                            <figure>
                                                <img src={player.imageUrl} />
                                            </figure>
                                        </div>;
                            }
                            return partial;
                        }
                    }
                </Query>
            </div>
        );
    }
}