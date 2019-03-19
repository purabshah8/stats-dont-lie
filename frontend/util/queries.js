import gql from "graphql-tag";


export const GET_ALL_TEAMS = gql `
    query {
        allTeams {
            id
            city
            name
        }
    }
`;

export const getTeam = (queryType, queryValue) => {

    return gql `
    {
    team(${queryType}: ${queryValue}) {
        city
        name
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
    }
`
}