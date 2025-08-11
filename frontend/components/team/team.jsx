import React, { useEffect } from 'react';
import { Link } from "react-router-dom";
import { useQuery, useReactiveVar } from "@apollo/client";
import { useParams, useLocation } from "react-router-dom";
import { GET_TEAM, GET_ROSTER } from '../../util/queries';
import SeasonPicker from "../elements/season_picker";
import Loading from '../elements/loading';
import { themeVar } from "../../root";

function TeamHeader({ teamId }) {
    const location = useLocation();
    const { loading, error, data } = useQuery(GET_TEAM, {
        variables: { teamId: parseInt(teamId) }
    });

    // Update theme using reactive variable in useEffect (must be before early returns)
    useEffect(() => {
        if (data?.team?.abbreviation) {
            themeVar(data.team.abbreviation);
        }
    }, [data?.team?.abbreviation]);

    if (loading) return <Loading />;
    if (error) return <div>Error! {error.message}</div>;

    const { team } = data;
    const { abbreviation, city, name, arena, division, yearFounded } = team;
    const divisionArray = division.name.split(" ");
    const divisionString = "Division: " + divisionArray[0];

    const conferenceArray = division.conference.name.split("ern ");
    const conferenceString = "Conference: " + conferenceArray[0];
    
    return(
        <>
        <div className={`${abbreviation}-theme`}>
            <div className="primary-background">
            </div>
            <div className="container">
                <div className="level">
                    <div className="level-left">
                        <div className="level-item">
                            <figure className="is-square is-96x96-touch">
                                <img alt={`${team.city} ${team.name}`} 
                                    src={`https://statsdontlie-media.s3.amazonaws.com/${abbreviation}.svg`} 
                                    className="team-logo" />
                            </figure>
                        </div>
                        <div className="level-item is-flexed team-name">
                            <p className="is-size-2 is-size-4-touch has-text-weight-semibold">{city}</p>
                            <p className="is-size-1 is-size-3-touch has-text-weight-semibold">{name}</p>
                            <p className="is-size-5 is-size-6-touch">est. {yearFounded}</p>
                        </div>
                        <div className="level-item is-flexed team-info">
                            <p className="is-size-4 is-size-5-touch has-text-left">{divisionString}</p>
                            <p className="is-size-4 is-size-5-touch has-text-left">{conferenceString}</p>
                            <div className="arena-name">
                                <ion-icon name="home"></ion-icon>
                                <p className="is-size-4 is-size-5-touch">{arena.name}</p>
                            </div>
                        </div>
                    </div>
                    <div className="level-right">
                    </div>
                </div>
            </div>
            <div className="secondary-diagonal"></div>
            <div className="secondary-background">
            </div>
        </div>
        <SeasonPicker 
            path={location.pathname} 
            start={yearFounded} 
            end={2019}/>
        </>
    );
}

function TeamRoster({ teamId }) {
    const { loading, error, data } = useQuery(GET_ROSTER, {
        variables: { teamId: parseInt(teamId), year: 2019 }
    });
    const theme = useReactiveVar(themeVar);

    if (loading) return null;
    if (error) return <div>Error! {error.message}</div>;
    
    const { teamSeason } = data;
    const comparePlayers = (a,b) => {
        const aLast = a.player.person.lastName;
        const bLast = b.player.person.lastName;
        if (aLast.toUpperCase() < bLast.toUpperCase())
            return -1;
        if (aLast.toUpperCase() > bLast.toUpperCase())
            return 1;
        return 0;
    };
    const sortedRoster = [...teamSeason.roster].sort(comparePlayers);
    const players = sortedRoster.map(datum => {
            const { player } = datum;
            let { person, positions, imageUrl } = player;
            const fullName = person.preferredName + " " + person.lastName;
            const isLongerThanOne = el => el.length > 1;
            if (positions.some(isLongerThanOne))
                positions = positions.filter(isLongerThanOne);
            positions = positions.join(", ");
            if (!imageUrl)
                imageUrl = "https://www.maxwell.syr.edu/uploadedImages/exed/people/students/IFS_Phase_V/August_2010/unknown-person.png";
            return(
                <div key={person.id}
                    className="roster-item column is-one-fifth is-flexed zoom-in">
                    <Link className="link"
                        to={`/players/${person.id}/seasons/2019`}>
                        <div className="is-flexed">
                            <p className="roster-text">{fullName}</p>
                        </div>
                        <figure className="is-flexed">
                            <img src={imageUrl} />
                        </figure>
                        <div className="is-flexed">
                            <p className="roster-pos">{positions}</p>
                        </div>
                    </Link>
                </div>
            );
        });
    return(
        <div className="container">
            <div className={`columns is-centered is-tablet is-multiline is-3 ${theme}-theme`}>
                {players}
            </div>
        </div>
    ); 
}

export default function Team() {
    const { id } = useParams();
    
    return (
        <div className="">
            <TeamHeader teamId={id} />
            <TeamRoster teamId={id} />
        </div>
    );
}