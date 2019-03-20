import gql from "graphql-tag";

export const GET_ALL_TEAMS = gql`
    query {
        allTeams {
            id
            city
            name
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