import { Component, OnInit, Input } from '@angular/core';
import { PopViewService } from '../_services';
import { FlaskDataService } from '../flask-data.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-matchup-card',
  templateUrl: './matchup-card.component.html',
  styleUrls: ['./matchup-card.component.css']
})
export class MatchupCardComponent implements OnInit {
  gameData!: any;
  myTimeout!: ReturnType<typeof setTimeout>;
  defaultLogo: string = "https://www.seekpng.com/png/full/140-1404801_ncaa-college-football-ncaa-football-logo.png";

  constructor(private fds: FlaskDataService, protected popviewService: PopViewService) {
  }

  ngOnInit() {
    this.myTimeout = setTimeout(() => { this.waitLoad() }, 1000);
  }

  waitLoad() {
    if (this.gameData === undefined)
    {
      this.gameData = this.fds.getGames();
      this.ngOnInit();
    }
    else
    {
      clearTimeout(this.myTimeout);
    }
  }
}

@Component({
  selector: 'app-matchup-card-logo',
  templateUrl: './matchup-card-logo.component.html',
  styleUrls: ['./matchup-card.component.css']
})
export class MatchupCardLogoComponent implements OnInit {
  @Input() gameID!: string;
  game!: any;
  homeLogo!: any;
  awayLogo!: any;
  currWeekMarquisGames!: number;
  styleString!: string;
  defaultLogo: string = "https://www.seekpng.com/png/full/140-1404801_ncaa-college-football-ncaa-football-logo.png";

  constructor(private fds: FlaskDataService, protected popviewService: PopViewService) {
  }

  ngOnInit() {
    this.game = this.fds.getGame(this.gameID);
    this.homeLogo = this.game.homeLogo;
    this.awayLogo = this.game.awayLogo;
    this.currWeekMarquisGames = this.fds.getMarquisGameNum();

    /*
    const test = document.getElementById('test');

    let styleStr1 = new String("div app-matchup-card-logo:nth-child(");
    let styleStr2 = new String(") { min-width: 500px; }\n");
    let fullStr: string = "";
    for (let i = 0; i < this.currWeekMarquisGames; i++)
    {
      let indexStr = new String(i);
      let nextStr = styleStr1.concat((indexStr.concat(styleStr2.toString())).toString());
      fullStr = fullStr.concat(nextStr.toString());
    }

    if (test != null)
    {
      //test.style = fullStr;
    }
    //this.styleString = fullStr.toString();
    */
  }
}

