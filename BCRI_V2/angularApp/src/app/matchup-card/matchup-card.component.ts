import { Component, OnInit } from '@angular/core';
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

