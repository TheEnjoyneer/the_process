import { Component, Input, OnInit } from '@angular/core';
import { FlaskDataService } from '../flask-data.service';
import { teamStatsDict, teamStatsList, teamStatsSplit, offenseStats, defenseStats, game } from '../dataInterfaces'

export interface tableElement {
  category: string;
  value: string;
}

@Component({
  selector: 'app-success-grid',
  templateUrl: './success-grid.component.html',
  styleUrls: ['./success-grid.component.css']
})
export class SuccessGridComponent implements OnInit {
  @Input() gameID!: string;
  @Input() teamSel!: string;
  undefOff: offenseStats = {
    average_fp_ppa: 0,
    average_fp_start: 0,
    drives: 0,
    explosiveness: 0,
    line_yards: 0,
    open_field_yards: 0,
    passing_explosiveness: 0,
    passing_rate: 0,
    passing_success_rate: 0,
    plays: 0,
    points_per_opportunity: 0,
    power_success: 0,
    ppa: 0,
    rushing_explosiveness: 0,
    rushing_rate: 0,
    rushing_success_rate: 0,
    second_level_yards: 0,
    stuff_rate: 0,
    success_rate: 0
  };
  undefDef: defenseStats = {
    average_fp_ppa: 0,
    average_fp_start: 0,
    drives: 0,
    explosiveness: 0,
    havoc_db: 0,
    havoc_front_seven: 0,
    havoc_total: 0,
    line_yards: 0,
    open_field_yards: 0,
    passing_explosiveness: 0,
    passing_success_rate: 0,
    plays: 0,
    points_per_opportunity: 0,
    power_success: 0,
    ppa: 0,
    rushing_explosiveness: 0,
    rushing_success_rate: 0,
    second_level_yards: 0,
    stuff_rate: 0,
    success_rate: 0
  }
  matchupInfo!: teamStatsDict;
  homeSplit!: teamStatsSplit;
  awaySplit!: teamStatsSplit;
  gameInfo!: game;
  offStats!: offenseStats;
  defStats!: defenseStats;
  textStats!: any;
  colors!: any;

  constructor(private fds: FlaskDataService) { }

  ngOnInit() {
    this.gameInfo = this.fds.getGame(this.gameID);
    this.matchupInfo = this.fds.getMatchupStats(this.gameID);
    this.homeSplit = this.matchupInfo[this.gameInfo.homeTeam];
    this.awaySplit = this.matchupInfo[this.gameInfo.awayTeam];
    this.offStats = this.undefOff;
    this.defStats = this.undefDef;

    if (Number(this.teamSel) == 1)
    {
      if (this.awaySplit === undefined) {
        this.offStats = this.undefOff;
        this.defStats = this.undefDef;
      }
      else {
        this.offStats = this.awaySplit.offense;
        this.defStats = this.awaySplit.defense;
      }
    }
    else if (Number(this.teamSel) == 2)
    {
      if (this.homeSplit === undefined) {
        this.offStats = this.undefOff;
        this.defStats = this.undefDef;
      }
      else {
        this.offStats = this.homeSplit.offense;
        this.defStats = this.homeSplit.defense;
      }
    }

    // Set text data to be in the matchup html
    this.textStats = {
      offSR: (this.offStats.success_rate*100).toFixed(2),
      offPassSR: (this.offStats.passing_success_rate*100).toFixed(2),
      offRushSR: (this.offStats.rushing_success_rate*100).toFixed(2),
      offPwrSR: (this.offStats.power_success*100).toFixed(2),
      defSR: (this.defStats.success_rate*100).toFixed(2),
      defPassSR: (this.defStats.passing_success_rate*100).toFixed(2),
      defRushSR: (this.defStats.rushing_success_rate*100).toFixed(2),
      defPwrSR: (this.defStats.power_success*100).toFixed(2)
    };

    this.colors = {
      offSR: this.fds.getColor(this.offStats.success_rate, "success_rate", "offense_total"),
      offPassSR: this.fds.getColor(this.offStats.passing_success_rate, "success_rate", "offense_passing"),
      offRushSR: this.fds.getColor(this.offStats.rushing_success_rate, "success_rate", "offense_rushing"),
      offPwrSR: this.fds.getColor(this.offStats.power_success, "success_rate", "offense_power"),
      defSR: this.fds.getColor(this.defStats.success_rate, "success_rate", "defense_total"),
      defPassSR: this.fds.getColor(this.defStats.passing_success_rate, "success_rate", "defense_passing"),
      defRushSR: this.fds.getColor(this.defStats.rushing_success_rate, "success_rate", "defense_rushing"),
      defPwrSR: this.fds.getColor(this.defStats.power_success, "success_rate", "defense_power"),
    }
  }
}
