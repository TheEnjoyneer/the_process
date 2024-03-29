import { Injectable, Optional, SkipSelf } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { teamStatsDict, teamStatsList, teamStatsSplit, offenseStats, defenseStats, game, thresholds } from './dataInterfaces'
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FlaskDataService {
  //requestStrBase: string = "http://127.0.0.1:5000/";
  //requestStrBase: string = "https://98.180.111.57:5000/";
  requestStrBase: string = "https://theenjoyneer.pythonanywhere.com/";
  requestStrGames: string = ""
  requestStr: string = "";
  teamStats!: any;
  teamStatsList!: any;
  currWeekGames!: any;
  currWeekMarquisGames: number = 0;
  reloaded: boolean = false;

  constructor(private http:HttpClient) {
    this.reloadApi("loaded").then(res => {
      if (res == "True")
      {
        console.log("API-Side Data Already Loaded");
        this.reloaded = true;
        this.reloadData();
      }
      else
      {
        this.reloadApi("reloadData").then(res => {
          if (res == "Data Reloaded")
          {
            console.log("API-Side Data Reloaded");
            this.reloaded = true;
            this.reloadData();
          }
        });
      }
    });
    /*
    var reqStrExt: string = "reloadData";
    var reqStr: string = this.requestStrBase.concat(reqStrExt.toString());
    this.http.get(reqStr);

    /*
    reqStrExt = "currGames";
    reqStr = this.requestStrBase.concat(reqStrExt.toString());
    this.http.get(reqStr).subscribe(data => {
      this.currWeekGames = <game[]>JSON.parse(JSON.stringify(data));
      });

    reqStrExt = "teamStatsDict";
    reqStr = this.requestStrBase.concat(reqStrExt.toString());
    this.http.get(reqStr).subscribe(data => {
      this.teamStats = <teamStatsDict>JSON.parse(JSON.stringify(data));
      });

    reqStrExt = "teamStatsList";
    reqStr = this.requestStrBase.concat(reqStrExt.toString());
    this.http.get(reqStr).subscribe(data => {
      this.teamStatsList = <teamStatsList[]>JSON.parse(JSON.stringify(data));
      });
      */
  }

  async reloadApi(reqStrExt: string) {
    //var reqStrExt: string = "reloadData";
    var reqStr: string = this.requestStrBase.concat(reqStrExt.toString());
    return await firstValueFrom(this.http.get(reqStr));
  }

  reloadData() {
    this.reloadApi("currGames").then(data => {
      this.currWeekGames = <game[]>JSON.parse(JSON.stringify(data))
    })

    this.reloadApi("teamStatsDict").then(data => {
      this.teamStats = <teamStatsDict>JSON.parse(JSON.stringify(data))
    })

    this.reloadApi("teamStatsList").then(data => {
      this.teamStatsList = <teamStatsList[]>JSON.parse(JSON.stringify(data))
    })

    this.reloadApi("numMarquisGames").then(data => {
      this.currWeekMarquisGames = <number>JSON.parse(JSON.stringify(data))
    })
  }

  getMarquisGameNum() {
    return this.currWeekMarquisGames;
  }

  getGames(): Observable<any[]> {
    return this.currWeekGames;
  }

  getGame(gameID: string) {
    var retGame!: game;
    for (let i = 0; i < this.currWeekGames.length; i++)
    {
      if (this.currWeekGames[i].gameID == gameID)
      {
        retGame = this.currWeekGames[i];
      }
    }
    return retGame;
  }
  
  getMatchupStats(gameID: string): teamStatsDict {
    var currGame: game = this.getGame(gameID);
    var homeTeam: string = currGame.homeTeam;
    var awayTeam: string = currGame.awayTeam;
    var homeStats: teamStatsSplit = this.teamStats[currGame.homeTeam];
    var awayStats: teamStatsSplit = this.teamStats[currGame.awayTeam];
    var retObj: teamStatsDict = {};
    retObj[homeTeam] = homeStats;
    retObj[awayTeam] = awayStats;

    return retObj;
  }

  getColor(statVal: number, statType: string, unitType: string)
  {
    var retColor: string = "var(--threshold3)";
    var thresholdObj: thresholds = <thresholds>this.getStatThresholds(statType, unitType);
    let splitStrArr = unitType.split("_");
    let splitStr = splitStrArr[0];
    
    if ((statType == "fp_start" && splitStr == "defense") || (statType == "stuff_rate" && splitStr == "defense"))
    {
      if (statVal < thresholdObj.neg2Dev)
      {
        retColor = "var(--threshold0)";
      }
      else if ((statVal > thresholdObj.neg2Dev) && (statVal < thresholdObj.neg1Dev))
      {
        retColor = "var(--threshold1)";
      }
      else if ((statVal > thresholdObj.neg1Dev) && (statVal < thresholdObj.negQrtDev))
      {
        retColor = "var(--threshold2)";
      }
      else if ((statVal > thresholdObj.negQrtDev) && (statVal < thresholdObj.posQrtDev))
      {
        retColor = "var(--threshold3)";
      }
      else if ((statVal > thresholdObj.posQrtDev) && (statVal < thresholdObj.pos1Dev))
      {
        retColor = "var(--threshold4)";
      }
      else if ((statVal > thresholdObj.pos1Dev) && (statVal < thresholdObj.pos2Dev))
      {
        retColor = "var(--threshold5)";
      }
      else if (statVal > thresholdObj.pos2Dev)
      {
        retColor = "var(--threshold6)";
      }
    }
    else if ((statType == "fp_start" && splitStr == "offense") || (statType == "stuff_rate" && splitStr == "offense"))
    {
      if (statVal < thresholdObj.neg2Dev)
      {
        retColor = "var(--threshold6)";
      }
      else if ((statVal > thresholdObj.neg2Dev) && (statVal < thresholdObj.neg1Dev))
      {
        retColor = "var(--threshold5)";
      }
      else if ((statVal > thresholdObj.neg1Dev) && (statVal < thresholdObj.negQrtDev))
      {
        retColor = "var(--threshold4)";
      }
      else if ((statVal > thresholdObj.negQrtDev) && (statVal < thresholdObj.posQrtDev))
      {
        retColor = "var(--threshold3)";
      }
      else if ((statVal > thresholdObj.posQrtDev) && (statVal < thresholdObj.pos1Dev))
      {
        retColor = "var(--threshold2)";
      }
      else if ((statVal > thresholdObj.pos1Dev) && (statVal < thresholdObj.pos2Dev))
      {
        retColor = "var(--threshold1)";
      }
      else if (statVal > thresholdObj.pos2Dev)
      {
        retColor = "var(--threshold0)";
      }
    }
    else if (splitStr == "offense" || splitStr == "havoc")
    {
      if (statVal < thresholdObj.neg2Dev)
      {
        retColor = "var(--threshold0)";
      }
      else if ((statVal > thresholdObj.neg2Dev) && (statVal < thresholdObj.neg1Dev))
      {
        retColor = "var(--threshold1)";
      }
      else if ((statVal > thresholdObj.neg1Dev) && (statVal < thresholdObj.negQrtDev))
      {
        retColor = "var(--threshold2)";
      }
      else if ((statVal > thresholdObj.negQrtDev) && (statVal < thresholdObj.posQrtDev))
      {
        retColor = "var(--threshold3)";
      }
      else if ((statVal > thresholdObj.posQrtDev) && (statVal < thresholdObj.pos1Dev))
      {
        retColor = "var(--threshold4)";
      }
      else if ((statVal > thresholdObj.pos1Dev) && (statVal < thresholdObj.pos2Dev))
      {
        retColor = "var(--threshold5)";
      }
      else if (statVal > thresholdObj.pos2Dev)
      {
        retColor = "var(--threshold6)";
      }
    }
    else if (splitStr == "defense")
    {
      if (statVal < thresholdObj.neg2Dev)
      {
        retColor = "var(--threshold6)";
      }
      else if ((statVal > thresholdObj.neg2Dev) && (statVal < thresholdObj.neg1Dev))
      {
        retColor = "var(--threshold5)";
      }
      else if ((statVal > thresholdObj.neg1Dev) && (statVal < thresholdObj.negQrtDev))
      {
        retColor = "var(--threshold4)";
      }
      else if ((statVal > thresholdObj.negQrtDev) && (statVal < thresholdObj.posQrtDev))
      {
        retColor = "var(--threshold3)";
      }
      else if ((statVal > thresholdObj.posQrtDev) && (statVal < thresholdObj.pos1Dev))
      {
        retColor = "var(--threshold2)";
      }
      else if ((statVal > thresholdObj.pos1Dev) && (statVal < thresholdObj.pos2Dev))
      {
        retColor = "var(--threshold1)";
      }
      else if (statVal > thresholdObj.pos2Dev)
      {
        retColor = "var(--threshold0)";
      }
    }
  

    return retColor;
  }

  private getStatsStats(stats: number[]): thresholds {
    let arr = stats.sort((a, b) => a - b);
    const midpoint = Math.floor(arr.length / 2);
    const median = arr.length % 2 === 1 ? arr[midpoint] : (arr[midpoint-1] + arr[midpoint]) / 2;
    var thresholdObj: thresholds;
    stats = stats.map((k) => {
      return (k - median) ** 2
    });

    let sum = stats.reduce((acc, curr) => acc + curr, 0);

    let stanDev = Math.sqrt(sum / stats.length);

    thresholdObj = {
      neg2Dev: median - (2 * stanDev),
      neg1Dev: median - stanDev,
      negQrtDev: median - (0.25 * stanDev),
      posQrtDev: median + (0.25 * stanDev),
      pos1Dev: median + stanDev,
      pos2Dev: median + (2 * stanDev)
    };
;
    return thresholdObj;
  }

  // statType is the stat itself and unitType is whether we want offense or defense thresholds
  getStatThresholds(statType: string, unitType: string): thresholds {
    var statsArr: number[] = [];
    var thresholdObj!: thresholds;
    var i: number;
    if (statType == "epa")
    {
      if (unitType == "offense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.ppa);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.ppa);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "ppo")
    {
      if (unitType == "offense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.points_per_opportunity);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.points_per_opportunity);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "fp_start")
    {
      if (unitType == "offense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.average_fp_start);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.average_fp_start);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "line_yards")
    {
      if (unitType == "offense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.line_yards);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.line_yards);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "second_level_yards")
    {
      if (unitType == "offense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.second_level_yards);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.second_level_yards);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "open_field_yards")
    {
      if (unitType == "offense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.open_field_yards);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.open_field_yards);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "stuff_rate")
    {
      if (unitType == "offense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.stuff_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.stuff_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "explosiveness")
    {
      if (unitType == "offense_total")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.explosiveness);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "offense_passing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.passing_explosiveness);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "offense_rushing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.rushing_explosiveness);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense_total")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.explosiveness);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense_passing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.passing_explosiveness);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense_rushing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.rushing_explosiveness);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "havoc")
    {
      if (unitType == "havoc_total")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.havoc_total);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "havoc_f7")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.havoc_front_seven);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "havoc_db")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.havoc_db);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    else if (statType == "success_rate")
    {
      if (unitType == "offense_total")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.success_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "offense_passing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.passing_success_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "offense_rushing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.rushing_success_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "offense_power")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.offense.power_success);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense_total")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.success_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense_passing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.passing_success_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense_rushing")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.rushing_success_rate);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
      else if (unitType == "defense_power")
      {
        for (i = 0; i < this.teamStatsList.length; i++)
        {
          statsArr.push(this.teamStatsList[i].stats.defense.power_success);
        }
        thresholdObj = this.getStatsStats(statsArr);
      }
    }
    return thresholdObj;
  }
}
