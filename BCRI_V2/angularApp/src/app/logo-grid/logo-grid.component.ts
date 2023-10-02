import { Component, Input, OnInit } from '@angular/core';
import { FlaskDataService } from '../flask-data.service';

@Component({
  selector: 'app-logo-grid',
  //standalone: true,
  templateUrl: './logo-grid.component.html',
  styleUrls: ['./logo-grid.component.css']
})
export class LogoGridComponent implements OnInit {
  @Input() gameID!: string;
  @Input() teamSel!: string;
  game!: any;
  imgSrc: string = "https://www.seekpng.com/png/full/140-1404801_ncaa-college-football-ncaa-football-logo.png";

  constructor(private fds: FlaskDataService) { }

  ngOnInit() {
    this.game = this.fds.getGame(this.gameID);

    if (Number(this.teamSel) == 1)
    {
      this.imgSrc = this.game.awayLogo;
    }
    else if (Number(this.teamSel) == 2)
    {
      this.imgSrc = this.game.homeLogo;
    }
  }
}
