import { Component, Input, OnInit } from '@angular/core';
import { FlaskDataService } from '../flask-data.service';

@Component({
  selector: 'app-preview-content',
  templateUrl: './preview-content.component.html',
  styleUrls: ['./preview-content.component.css']
})
export class PreviewContentComponent implements OnInit {
    @Input() gameID!: string;
    game!: any;
    homeWP!: string;
    awayWP!: string;

    constructor(private fds: FlaskDataService) { }

    ngOnInit() {
      this.game = this.fds.getGame(this.gameID);
      this.homeWP = (this.game.homeWinProb*100).toFixed(2);
      this.awayWP = ((1 - this.game.homeWinProb)*100).toFixed(2);
    }
}
