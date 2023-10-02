export interface teamStatsList {
    team: string;
    stats: teamStatsSplit;
}

export interface teamStatsDict {
    [team: string]: teamStatsSplit;
}

export interface teamStatsSplit {
    defense: defenseStats;
    offense: offenseStats;
}

export interface defenseStats {
    average_fp_ppa: number;
    average_fp_start: number;
    drives: number;
    explosiveness: number;
    havoc_db: number;
    havoc_front_seven: number;
    havoc_total: number;
    line_yards: number;
    open_field_yards: number;
    passing_explosiveness: number;
    passing_success_rate: number;
    plays: number;
    points_per_opportunity: number;
    power_success: number;
    ppa: number;
    rushing_explosiveness: number;
    rushing_success_rate: number;
    second_level_yards: number;
    stuff_rate: number;
    success_rate: number;
}

export interface offenseStats {
    average_fp_ppa: number;
    average_fp_start: number;
    drives: number;
    explosiveness: number;
    line_yards: number;
    open_field_yards: number;
    passing_explosiveness: number;
    passing_rate: number;
    passing_success_rate: number;
    plays: number;
    points_per_opportunity: number;
    power_success: number;
    ppa: number;
    rushing_explosiveness: number;
    rushing_rate: number;
    rushing_success_rate: number;
    second_level_yards: number;
    stuff_rate: number;
    success_rate: number;
}

export interface game {
    gameID: string;
    homeTeam: string;
    awayTeam: string;
    homeTeamRank: string;
    awayTeamRank: string;
    homeLogo: string;
    awayLogo: string;
    homeAbbr: string;
    awayAbbr: string;
    homeAbbrRank: string;
    awayAbbrRank: string;
    conferences: string;
    venue: string;
    location: string;
    provider: string;
    openSpread: number;
    currSpread: number;
    currTotal: number;
    openTotal: number;
    moneyline: number;
    homeWinProb: number;
    startTime: string;
    startDate: string;
    completed: boolean;
    homePostWinProb: number;
    awayPostWinProb: number;
}

export interface thresholds {
    neg2Dev: number;
    neg1Dev: number;
    negQrtDev: number;
    posQrtDev: number;
    pos1Dev: number;
    pos2Dev: number;
}