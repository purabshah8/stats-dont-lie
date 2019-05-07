import gql from "graphql-tag";

export const personFragments = {
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

export const playerFragments = {
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

export const statFragments = {
    stats: gql`
    fragment stats on FullStatlineType {
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
        started
        ts
        efg
        tpar
        ftr
        orbPct
        drbPct
        trbPct
        astPct
        stlPct
        blkPct
        tovPct
        usgRate
        ortg
        drtg
        possessions
        pace
    }`
};

export const teamSeasonFragments = {
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

export const teamFragments = {
    name: gql`
    fragment teamName on TeamType {
        id
        city
        name
        abbreviation
    }
    `,
};