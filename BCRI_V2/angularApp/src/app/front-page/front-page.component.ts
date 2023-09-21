import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { MatchupCardComponent } from '../matchup-card/matchup-card.component';
import { CardGridComponent } from '../card-grid/card-grid.component';

@Component({
  selector: 'app-front-page',
  standalone: true,
  imports: [ 
    HttpClientModule,
    MatchupCardComponent,
    CardGridComponent
  ],
  templateUrl: './front-page.component.html',
  styleUrls: ['./front-page.component.css']
})
export class FrontPageComponent {

}