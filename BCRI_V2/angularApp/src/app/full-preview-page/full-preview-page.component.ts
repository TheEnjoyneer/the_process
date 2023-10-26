import { Component, OnInit } from '@angular/core';
import { FlaskDataService } from '../flask-data.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-full-preview-page',
  templateUrl: './full-preview-page.component.html',
  styleUrls: ['./full-preview-page.component.css']
})
export class FullPreviewPageComponent implements OnInit {
  //@Input() gameID!: string;
  gameID!: string;
  game!: any;
  homeWP!: string;
  awayWP!: string;

  constructor(private fds: FlaskDataService, private router: Router, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.gameID = params['gameID'];
      this.game = this.fds.getGame(this.gameID);
    })
  }

  ngOnInit() {
    //this.game = this.fds.getGame(this.gameID);
    //console.log(this.game);
    //this.game = this.fds.getGame(this.gameID);
    //this.homeWP = (this.game.homeWinProb*100).toFixed(2);
    //this.awayWP = ((1 - this.game.homeWinProb)*100).toFixed(2);
    //const gameID: any = this.route.snapshot.queryParamMap.get('gameID');

    // Something else here
  }

}
