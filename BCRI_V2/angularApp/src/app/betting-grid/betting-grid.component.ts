import { Component, Input, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { FlaskDataService } from '../flask-data.service';

@Component({
  selector: 'app-betting-grid',
  templateUrl: './betting-grid.component.html',
  styleUrls: ['./betting-grid.component.css']
})
export class BettingGridComponent implements OnInit {
  @Input() gameID!: string;
  gamesList!: any;
  game!: any;

  constructor(private fds: FlaskDataService, public dialog: MatDialog) { }

  ngOnInit() {
    this.gamesList = this.fds.getGames();
    for (let i = 0; i < Object.keys(this.gamesList).length; i++)
    {
      let value1: boolean = this.gameID === this.gamesList[i].gameID;
      if (value1)
      {
        this.game = this.gamesList[i];
      }
    }
  }
/*
  openDialog(enterAnimationDuration: string, exitAnimationDuration: string): void {
    this.dialog.open(DialogLock, {
      width: '250px',
      enterAnimationDuration,
      exitAnimationDuration,
    })
  }
*/
}
/*
@Component({
  selector: 'dialog-lock',
  templateUrl: './dialog.html'
})
export class DialogLock {
  constructor(public dialogRef: MatDialogRef<DialogLock>) {}
}
*/