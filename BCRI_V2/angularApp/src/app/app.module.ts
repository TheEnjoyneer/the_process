import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { MatMenuModule } from '@angular/material/menu';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatDividerModule } from '@angular/material/divider';
import { MatCardModule } from '@angular/material/card';
import { FlaskDataService } from './flask-data.service';
import { FrontPageComponent } from './front-page/front-page.component';
import { PopViewComponent } from './pop-view/pop-view.component';
import { MatchupCardComponent, MatchupCardLogoComponent } from './matchup-card/matchup-card.component';
import { PreviewContentComponent } from './preview-content/preview-content.component';
import { MatchupGridComponent } from './matchup-grid/matchup-grid.component';
import { LogoGridComponent } from './logo-grid/logo-grid.component';
import { InfoGridComponent } from './info-grid/info-grid.component';
import { ExplosiveGridComponent } from './explosive-grid/explosive-grid.component';
import { SuccessGridComponent } from './success-grid/success-grid.component';
import { BettingGridComponent } from './betting-grid/betting-grid.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatListModule } from '@angular/material/list';
import { FormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { Routes, RouterModule } from '@angular/router';
import { FullPreviewPageComponent } from './full-preview-page/full-preview-page.component';
import { FullRecapPageComponent } from './full-recap-page/full-recap-page.component';

@NgModule({
  imports:      [ 
                    BrowserModule, 
                    BrowserAnimationsModule,
                    MatMenuModule,
                    MatTableModule,
                    MatIconModule,
                    MatButtonModule,
                    MatToolbarModule,
                    MatGridListModule,
                    MatDividerModule,
                    MatCardModule,
                    HttpClientModule,
                    FlexLayoutModule,
                    MatListModule,
                    FormsModule,
                    MatDialogModule,
                    MatSnackBarModule,
                    RouterModule.forRoot([
                      {path: '', component: MatchupCardComponent},
                      {path: 'full-preview', component: FullPreviewPageComponent},
                      {path: 'full-recap', component: SuccessGridComponent},
                    ]),
                ],
  exports: [ RouterModule ],
  declarations: [ 
                    FrontPageComponent, 
                    PopViewComponent,
                    MatchupCardComponent,
                    MatchupCardLogoComponent,
                    PreviewContentComponent, 
                    MatchupGridComponent,
                    LogoGridComponent,
                    InfoGridComponent,
                    ExplosiveGridComponent,
                    SuccessGridComponent,
                    BettingGridComponent,
                    FullPreviewPageComponent,
                    FullRecapPageComponent
                ],
  providers:    [ FlaskDataService ],
  bootstrap:    [ FrontPageComponent ]
})
export class AppModule { 
}