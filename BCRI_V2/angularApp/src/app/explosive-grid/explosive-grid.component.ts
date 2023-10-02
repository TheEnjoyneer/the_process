import { Component, Input, OnInit } from '@angular/core';
import { FlaskDataService } from '../flask-data.service';
import { teamStatsDict, teamStatsList, teamStatsSplit, offenseStats, defenseStats, game } from '../dataInterfaces'

@Component({
  selector: 'app-explosive-grid',
  templateUrl: './explosive-grid.component.html',
  styleUrls: ['./explosive-grid.component.css']
})
export class ExplosiveGridComponent implements OnInit {
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
      offEx: this.offStats.explosiveness.toFixed(3),
      offPassEx: this.offStats.passing_explosiveness.toFixed(3),
      offRushEx: this.offStats.rushing_explosiveness.toFixed(3),
      defEx: this.defStats.explosiveness.toFixed(3),
      defPassEx: this.defStats.passing_explosiveness.toFixed(3),
      defRushEx: this.defStats.rushing_explosiveness.toFixed(3),
      havoc: (this.defStats.havoc_total*100).toFixed(2),
      havocF7: (this.defStats.havoc_front_seven*100).toFixed(2),
      havocDb: (this.defStats.havoc_db*100).toFixed(2)
    };

    this.colors = {
      offEx: this.fds.getColor(this.offStats.explosiveness, "explosiveness", "offense_total"),
      offPassEx: this.fds.getColor(this.offStats.passing_explosiveness, "explosiveness", "offense_passing"),
      offRushEx: this.fds.getColor(this.offStats.rushing_explosiveness, "explosiveness", "offense_rushing"),
      defEx: this.fds.getColor(this.defStats.explosiveness, "explosiveness", "defense_total"),
      defPassEx: this.fds.getColor(this.defStats.passing_explosiveness, "explosiveness", "defense_passing"),
      defRushEx: this.fds.getColor(this.defStats.rushing_explosiveness, "explosiveness", "defense_rushing"),
      havoc: this.fds.getColor(this.defStats.havoc_total, "havoc", "havoc_total"),
      havocF7: this.fds.getColor(this.defStats.havoc_front_seven, "havoc", "havoc_f7"),
      havocDb: this.fds.getColor(this.defStats.havoc_db, "havoc", "havoc_db")
    };
  }
}
