import { Component, OnInit } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-matchup-card',
  templateUrl: './matchup-card.component.html',
  standalone: true,
  imports: [ MatCardModule, MatButtonModule ],
  styleUrls: ['./matchup-card.component.css']
})
export class MatchupCardComponent implements OnInit {
  newdata:any;

  longText = "Testing here we go bitches!";

  constructor(private http: HttpClient) { }

  ngOnInit() {
	this.getData();
  }

  getData() {
	 // this.http.get('http://127.0.0.1:5000/topGame').map(response => response.json()).subscribe(data => this.newdata = data);
    this.http.get('http://127.0.0.1:5000/topGame').subscribe(data => {
      console.log(data)
      this.newdata = data;//JSON.stringify(data);
      });
  }
}
