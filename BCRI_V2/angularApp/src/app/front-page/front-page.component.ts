import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { MatchupCardComponent } from '../matchup-card/matchup-card.component';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import { PopViewService } from '../_services';

@Component({
  selector: 'app-front-page',
  standalone: true,
  imports: [ 
    HttpClientModule,
    MatchupCardComponent,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './front-page.component.html',
  styleUrls: ['./front-page.component.css']
})
export class FrontPageComponent {
  constructor(protected popviewService: PopViewService) { }
}