import gql from "graphql-tag";


const personFragments = {
    details: gql`
    fragment personDetails on PersonType {
        id
        preferredName
        lastName
        dob
        college
        birthplace {
            city
            state
            country
        }
    }
    `
};

const playerFragments = {
    name: gql`
    fragment playerName on PlayerType {
        person {
            id
            preferredName
            lastName
        }
        imageUrl
    }
    `,
    details: gql`
    fragment playerDetails on PlayerType {
        height
        weight
        shootingHand
        positions
    }
    `
};


const teamSeasonFragments = {
    roster : gql`
    fragment teamRoster on TeamSeasonType {
        roster {
            player {
            ...playerName
            positions
            }
        }
    }
    ${playerFragments.name}
    `,
};

const teamFragments = {
    name: gql`
    fragment teamName on TeamType {
        id
        city
        name
        abbreviation
    }
    `,
};

export const GET_ALL_TEAMS = gql`
query {
    allTeams {
        ...teamName
    }
}
${teamFragments.name}
`;

export const GET_TEAM = gql`
query TeamDetails($teamId: Int!) {
    team(id: $teamId) {
        ...teamName
        arena {
            name
        }
        division {
            name
            conference {
                name
            }
        }
        yearFounded
    }
}
${teamFragments.name}
`;

export const GET_ROSTER = gql`
query roster($teamId: Int!, $year: Int!) {
    teamSeason(teamId: $teamId, year: $year) {
        ...teamRoster
    }
    theme @client
}
${teamSeasonFragments.roster}
`;

export const GET_PLAYER = gql`
query ($playerId: Int!) {
    player(id: $playerId) {
        person {
            ...personDetails
        }
        rookieSeason {
            year
        }
        finalSeason {
            year
        }
        currentTeam {
            ...teamName
        }
        ...playerDetails
        imageUrl
    }
}
${personFragments.details}
${teamFragments.name}
${playerFragments.details}
`;

export const GET_PLAYER_SEASON = gql`
query getPlayerSeason($playerId: Int!, $year: Int!) {
    playerSeason(playerId: $playerId, year: $year) {
        player {
            person {
                ...personDetails
            }
            rookieSeason {
                year
            }
            finalSeason {
                year
            }
            ...playerDetails
            imageUrl
        }
        teamSeason {
            team {
                ...teamName
            }
        }
        rawStats {
            mp
            fg
            fga
            fgPct
            tp
            tpa
            tpPct
            ft
            fta
            ftPct
            orb
            drb
            trb
            ast
            stl
            blk
            tov
            pf
            pts
            plusMinus
            started
        }
    }
}
${personFragments.details}
${teamFragments.name}
${playerFragments.details}
`;


export const GET_NAV_STATE = gql`
query navStateQuery {
    navMenuIsActive @client
    theme @client
}
`;

export const GET_THEME = gql`
query themeQuery {
    theme @client
}
`;