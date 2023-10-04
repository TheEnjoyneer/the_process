import { Component } from '@angular/core';
import { PopViewService } from '../_services';
import { FlaskDataService } from '../flask-data.service';

@Component({
  selector: 'app-front-page',
  templateUrl: './front-page.component.html',
  styleUrls: ['./front-page.component.css']
})
export class FrontPageComponent {
  constructor(protected fds: FlaskDataService, protected popviewService: PopViewService) { }
}