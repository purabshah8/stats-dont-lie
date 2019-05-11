import React, { Component } from 'react';
import { Query } from "react-apollo";
import { Link } from "react-router-dom";
import { SEARCH } from "../../util/queries";
import Loading from '../elements/loading';
export default class Search extends Component {
    constructor(props) {
        super(props);
        this.state = {
            searchString: "",
            isFocused: false,
        };

        this.toggleFocus = this.toggleFocus.bind(this);
    }

    update(field) {
        return e => {
          this.setState({[field]: e.target.value});
        };
    }

    searchPlayers() {
        const { searchString } = this.state;
        if (searchString.length > 2) {
            return (
                <Query query={SEARCH} variables={ { term: this.state.searchString } }>
                    {
                        ({ loading, error, data }) => {
                            if (loading) return <Loading />;
                            if (error) return `Error! ${error.message}`;

                            let { search } = data;
                            const results = search.map(player => {
                                let { person, imageUrl, positions, currentTeam } = player;
                                let uniquePos = positions.filter(pos => pos.length > 1);
                                if (positions.indexOf("C") !== -1)
                                    uniquePos.push("C");
                                const { id, preferredName, lastName } = person;
                                const { city, name, abbreviation } = currentTeam;
                                if (!imageUrl)
                                    imageUrl = "https://www.maxwell.syr.edu/uploadedImages/exed/people/students/IFS_Phase_V/August_2010/unknown-person.png";
                                return (
                                    <li key={id} className={`${abbreviation}-theme column is-two-fifths`}>
                                        <Link className="result-link" to={`/players/${id}/seasons/2019`}>
                                            <div className="result-item">
                                                <div className="result-info">
                                                    <figure className="image">
                                                        <img className="player-image" src={imageUrl} />
                                                    </figure>
                                                    <div>
                                                        <p className="is-size-3 has-text-centered">{preferredName} </p>
                                                        <p className="is-size-3 has-text-centered">{lastName}</p>
                                                        <p className="is-size-5 has-text-centered">{}</p>
                                                        <p className="is-size-5 has-text-centered">{uniquePos.join(" | ")}</p>
                                                    </div>
                                                </div>
                                                <div className="result-team has-text-centered">{city + " " + name}</div>
                                            </div>
                                        </Link>
                                    </li>
                                );
                            });
                            return (
                                <ul className="columns is-centered is-multiline search-results">
                                    {results}
                                </ul>
                            );
                        }
                    }
                </Query>
            );
        }
        else return null;
    }

    toggleFocus(e) {
        e.preventDefault();
        this.setState({
            isFocused: !this.state.isFocused
        });
    }


    render() {
        let underlineClasses = "underline";
        if (this.state.isFocused)
            underlineClasses += " is-focused";
        return (
            <div className="container search-container">
                <div className="search-input">
                    <input
                        onFocus={this.toggleFocus}
                        onBlur={this.toggleFocus}
                        autoComplete="off"
                        placeholder="Search Players" 
                        type="text" 
                        id="player-search-large" 
                        value={this.state.searchString}
                        onChange={this.update('searchString')}/>
                    <div className={underlineClasses}></div>

                </div>
                <div className="results">
                    {this.searchPlayers()}
                </div>
            </div>
        );
    }
}
