import { Component, OnInit, Input } from '@angular/core';
import { PopViewService } from '../_services';
import { FlaskDataService } from '../flask-data.service';
import { ActivatedRoute, Router } from '@angular/router';
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

  constructor(private fds: FlaskDataService, protected popviewService: PopViewService, private router: Router, private activeRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.game = this.fds.getGame(this.gameID);
    this.homeLogo = this.game.homeLogo;
    this.awayLogo = this.game.awayLogo;
    this.currWeekMarquisGames = this.fds.getMarquisGameNum();
  }

  pageLink() {
    if (this.game.completed == true)
    {
      this.router.navigate(['/full-recap'], {queryParams: {
        gameID: this.gameID,
      }});
    }
    else {
      this.router.navigate(['/full-preview'], {queryParams: {
        gameID: this.gameID,
      }});
    }
  }
}

