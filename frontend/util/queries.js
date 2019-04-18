import gql from "graphql-tag";

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
        roster {
            player {
                person {
                    id
                    preferredName
                    lastName
                }
            imageUrl
            }
        }
    }
}
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