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
      height
      weight
      shootingHand
      positions
      imageUrl
    }
  }
`;