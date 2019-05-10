import gql from "graphql-tag";
import * as fragments from "./fragments";

export const GET_ALL_TEAMS = gql`
query {
    allTeams {
        ...teamName
    }
}
${fragments.teamFragments.name}
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
${fragments.teamFragments.name}
`;

export const GET_ROSTER = gql`
query roster($teamId: Int!, $year: Int!) {
    teamSeason(teamId: $teamId, year: $year) {
        ...teamRoster
    }
    theme @client
}
${fragments.teamSeasonFragments.roster}
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
${fragments.personFragments.details}
${fragments.teamFragments.name}
${fragments.playerFragments.details}
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
            season {
                startDate
                playoffsStartDate
                aggregateStats {
                    averages {
                        ...stats
                    }
                    standardDeviations {
                        ...stats
                    }
                }
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
            gameDates
        }
        totalStats {
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
            gp
            starts
            ts
            efg
            tpar
            ftr
        }
    }
}
${fragments.personFragments.details}
${fragments.teamFragments.name}
${fragments.playerFragments.details}
${fragments.statFragments.stats}
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

export const GET_SEASON_STATS = gql`
query seasonStatsQuery($year: Int, $leagueId: Int){
    season(year:2019) {
    aggregateStats {
        averages {
        ...stats
        }
        standardDeviations {
        ...stats
        }
    }
    }
}
${fragments.statFragments.stats}
`;

export const SEARCH = gql`
query playerSearchQuery($term: String) {
    search(term: $term) {
        ...playerName
        currentTeam {
            ...teamName
        }
        positions
    }
}
${fragments.playerFragments.name}
${fragments.teamFragments.name}
`;