import gql from "graphql-tag";


const playerFragments = {
    name: gql`
    fragment playerName on PlayerType {
        person {
            id
            preferredName
            lastName
        }
    }
    `,
};


const teamSeasonFragments = {
    roster : gql`
    fragment teamRoster on TeamSeasonType {
        roster {
            player {
            ...playerName
            imageUrl
            }
        }
    }
    ${playerFragments.name}
    `,
};

const teamFragments = {
    name: gql`
    fragment teamName on TeamType {
        city
        name
        abbreviation
    }
    `,
};

export const GET_ALL_TEAMS = gql`
    query {
        allTeams {
            id
            city
            name
            abbreviation
        }
    }
`;

export const GET_TEAM = gql`
query TeamDetails($teamId: Int!) {
    team(id: $teamId) {
        city
        name
        abbreviation
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
}`;

export const GET_ROSTER = gql`
query roster($teamId: Int!, $year: Int!) {
    teamSeason(teamId: $teamId, year: $year) {
        ...teamRoster
    }
}
${teamSeasonFragments.roster}
`;

export const GET_PLAYER = gql`
query ($playerId: Int!) {
    player(id: $playerId) {
        person {
            preferredName
            firstName
            lastName
            dob
            college
            birthplace {
                city
                state
                country
            }
        }
        rookieSeason {
            year
        }
        finalSeason {
            year
        }
        height
        weight
        shootingHand
        positions
        imageUrl
    }
  }
`;

export const GET_PLAYER_SEASON = gql`
query getPlayerSeason($playerId: Int!, $year: Int!) {
    playerSeason(playerId: $playerId, year: $year) {
        player {
            ...playerName
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
${playerFragments.name}
${teamFragments.name}
`;