import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatchupCardComponent } from '../matchup-card/matchup-card.component'

@Component({
  selector: 'app-card-grid',
  standalone: true,
  imports: [ 
    HttpClientModule,
    MatchupCardComponent,
    MatGridListModule
  ],
  templateUrl: './card-grid.component.html',
  styleUrls: ['./card-grid.component.css']
})
export class CardGridComponent {

}
