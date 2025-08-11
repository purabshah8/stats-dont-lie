import React, { useState } from 'react';
import { useQuery } from "@apollo/client";
import { Link } from "react-router-dom";
import { SEARCH } from "../../util/queries";
import Loading from '../elements/loading';

export default function Search() {
    const [searchString, setSearchString] = useState("");
    const [isFocused, setIsFocused] = useState(false);

    const { loading, error, data } = useQuery(SEARCH, {
        variables: { term: searchString },
        skip: searchString.length <= 2
    });

    const toggleFocus = (e) => {
        e.preventDefault();
        setIsFocused(!isFocused);
    };

    const searchPlayers = () => {
        if (searchString.length <= 2) return null;
        
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
    };

    let underlineClasses = "underline";
    if (isFocused)
        underlineClasses += " is-focused";
        
    return (
        <div className="container search-container">
            <div className="search-input">
                <input
                    onFocus={toggleFocus}
                    onBlur={toggleFocus}
                    autoComplete="off"
                    placeholder="Search Players" 
                    type="text" 
                    id="player-search-large" 
                    value={searchString}
                    onChange={(e) => setSearchString(e.target.value)}/>
                <div className={underlineClasses}></div>
            </div>
            <div className="results">
                {searchPlayers()}
            </div>
        </div>
    );
}
