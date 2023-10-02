import { Component } from '@angular/core';
import { PopViewService } from '../_services';

@Component({
  selector: 'app-front-page',
  templateUrl: './front-page.component.html',
  styleUrls: ['./front-page.component.css']
})
export class FrontPageComponent {
  constructor(protected popviewService: PopViewService) {
   }
}