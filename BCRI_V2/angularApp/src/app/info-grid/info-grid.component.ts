import { Component, Input, OnInit } from '@angular/core';
import { FlaskDataService } from '../flask-data.service';

@Component({
  selector: 'app-info-grid',
  templateUrl: './info-grid.component.html',
  styleUrls: ['./info-grid.component.css']
})
export class InfoGridComponent implements OnInit {
  @Input() gameID!: string;
  game!: any;;

  constructor(private fds: FlaskDataService) { }

  ngOnInit() {
    this.game = this.fds.getGame(this.gameID);
  }
}
