import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { PopViewService } from '../_services';
import { PopViewComponent } from '../pop-view/pop-view.component';

@Component({
  selector: 'app-matchup-card',
  templateUrl: './matchup-card.component.html',
  standalone: true,
  imports: [ MatCardModule, MatButtonModule, NgFor, PopViewComponent ],
  styleUrls: ['./matchup-card.component.css']
})
export class MatchupCardComponent implements OnInit {
  newdata:any;

  constructor(private http: HttpClient, protected popviewService: PopViewService) { }

  ngOnInit() {
	this.getData();
  }

  getData() {
	 // this.http.get('http://127.0.0.1:5000/topGame').map(response => response.json()).subscribe(data => this.newdata = data);
    this.http.get('http://127.0.0.1:5000/gameCards').subscribe(data => {
      console.log(data)
      this.newdata = data;//JSON.stringify(data);
      });
  }
}

