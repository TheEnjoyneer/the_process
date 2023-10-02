import { Component, Input, OnInit } from '@angular/core';
import { FlaskDataService } from '../flask-data.service';
import { teamStatsDict, teamStatsList, teamStatsSplit, offenseStats, defenseStats, game } from '../dataInterfaces'

@Component({
  selector: 'app-matchup-grid',
  templateUrl: './matchup-grid.component.html',
  styleUrls: ['./matchup-grid.component.css']
})
export class MatchupGridComponent implements OnInit {
  @Input() gameID!: string;
  @Input() titleDir!: string;
  titleStr: string = "test";
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
  //matchupInfo!: teamStatsList[];
  homeSplit!: teamStatsSplit;
  awaySplit!: teamStatsSplit;
  gameInfo!: game;
  leftStats!: any;
  rightStats!: any;
  textStats!: any;
  leftCol!: string;
  rightCol!: string;
  colors!: any;
  styles!: any;


  constructor(private fds: FlaskDataService) { }

  ngOnInit() {
    this.gameInfo = this.fds.getGame(this.gameID);
    this.matchupInfo = this.fds.getMatchupStats(this.gameID);
    this.homeSplit = <teamStatsSplit>this.matchupInfo[this.gameInfo.homeTeam];
    this.awaySplit = <teamStatsSplit>this.matchupInfo[this.gameInfo.awayTeam];    

    if (Number(this.titleDir) == 1)
    {
      this.leftCol = "Offense";
      this.rightCol = "Defense";
      this.titleStr = "Offense vs Defense";
      if (this.awaySplit === undefined) {
        this.leftStats = this.undefOff;
      }
      else {
        this.leftStats = <offenseStats>this.awaySplit.offense;
      }
      if (this.homeSplit === undefined) {
        this.rightStats = this.undefDef;
      }
      else {
        this.rightStats = <defenseStats>this.homeSplit.defense;
      }

      this.colors = {
        left_epa: this.fds.getColor(this.leftStats.ppa, "epa", "offense"),
        left_ppo: this.fds.getColor(this.leftStats.points_per_opportunity, "ppo", "offense"),
        left_avg_fp: this.fds.getColor(this.leftStats.average_fp_start, "fp_start", "offense"),
        left_line_yards: this.fds.getColor(this.leftStats.line_yards, "line_yards", "offense"),
        left_second_level: this.fds.getColor(this.leftStats.second_level_yards, "second_level_yards", "offense"),
        left_open_field: this.fds.getColor(this.leftStats.open_field_yards, "open_field_yards", "offense"),
        left_stuff: this.fds.getColor(this.leftStats.stuff_rate, "stuff_rate", "offense"),
        right_epa: this.fds.getColor(this.rightStats.ppa, "epa", "defense"),
        right_ppo: this.fds.getColor(this.rightStats.points_per_opportunity, "ppo", "defense"),
        right_avg_fp: this.fds.getColor(this.rightStats.average_fp_start, "fp_start", "defense"),
        right_line_yards: this.fds.getColor(this.rightStats.line_yards, "line_yards", "defense"),
        right_second_level: this.fds.getColor(this.rightStats.second_level_yards, "second_level_yards", "defense"),
        right_open_field: this.fds.getColor(this.rightStats.open_field_yards, "open_field_yards", "defense"),
        right_stuff: this.fds.getColor(this.rightStats.stuff_rate, "stuff_rate", "defense"),
      };
    }
    else if (Number(this.titleDir) == 2)
    {
      this.leftCol = "Defense";
      this.rightCol = "Offense";
      this.titleStr = "Defense vs Offense";
      if (this.homeSplit === undefined) {
        this.rightStats = this.undefOff;
      }
      else {
        this.rightStats = <offenseStats>this.homeSplit.offense;
      }
      if (this.awaySplit === undefined) {
        this.leftStats = this.undefDef;
      }
      else {
        this.leftStats = <defenseStats>this.awaySplit.defense;
      }

      this.colors = {
        left_epa: this.fds.getColor(this.leftStats.ppa, "epa", "defense"),
        left_ppo: this.fds.getColor(this.leftStats.points_per_opportunity, "ppo", "defense"),
        left_avg_fp: this.fds.getColor(this.leftStats.average_fp_start, "fp_start", "defense"),
        left_line_yards: this.fds.getColor(this.leftStats.line_yards, "line_yards", "defense"),
        left_second_level: this.fds.getColor(this.leftStats.second_level_yards, "second_level_yards", "defense"),
        left_open_field: this.fds.getColor(this.leftStats.open_field_yards, "open_field_yards", "defense"),
        left_stuff: this.fds.getColor(this.leftStats.stuff_rate, "stuff_rate", "defense"),
        right_epa: this.fds.getColor(this.rightStats.ppa, "epa", "offense"),
        right_ppo: this.fds.getColor(this.rightStats.points_per_opportunity, "ppo", "offense"),
        right_avg_fp: this.fds.getColor(this.rightStats.average_fp_start, "fp_start", "offense"),
        right_line_yards: this.fds.getColor(this.rightStats.line_yards, "line_yards", "offense"),
        right_second_level: this.fds.getColor(this.rightStats.second_level_yards, "second_level_yards", "offense"),
        right_open_field: this.fds.getColor(this.rightStats.open_field_yards, "open_field_yards", "offense"),
        right_stuff: this.fds.getColor(this.rightStats.stuff_rate, "stuff_rate", "offense"),
      };
    }

    // Set text data to be in the matchup html
    this.textStats = {
      leftPPA: this.leftStats.ppa.toFixed(3),
      leftPPO: this.leftStats.points_per_opportunity.toFixed(3),
      leftFpPPA: this.leftStats.average_fp_ppa.toFixed(3),
      leftFpStart: this.leftStats.average_fp_start.toFixed(2),
      leftLineYds: this.leftStats.line_yards.toFixed(3),
      leftSecLvlYds: this.leftStats.second_level_yards.toFixed(3),
      leftOpenFldYds: this.leftStats.open_field_yards.toFixed(3),
      leftStuff: this.leftStats.stuff_rate.toFixed(3),
      rightPPA: this.rightStats.ppa.toFixed(3),
      rightPPO: this.rightStats.points_per_opportunity.toFixed(3),
      rightFpPPA: this.rightStats.average_fp_ppa.toFixed(3),
      rightFpStart: this.rightStats.average_fp_start.toFixed(2),
      rightLineYds: this.rightStats.line_yards.toFixed(3),
      rightSecLvlYds: this.rightStats.second_level_yards.toFixed(3),
      rightOpenFldYds: this.rightStats.open_field_yards.toFixed(3),
      rightStuff: this.rightStats.stuff_rate.toFixed(3),
    };
  }
}
