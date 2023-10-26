import { Component } from '@angular/core';
import { PopViewService } from '../_services';
import { FlaskDataService } from '../flask-data.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-front-page',
  templateUrl: './front-page.component.html',
  styleUrls: ['./front-page.component.css']
})
export class FrontPageComponent {
  testBool!: boolean;

  constructor(protected fds: FlaskDataService, protected popviewService: PopViewService, private router: Router) { }

  reloadBackend()
  {
    this.fds.reloadApi("reloadData").then(res => {
      if (res == "Data Reloaded")
      {
        console.log("conditional worked");
        this.fds.reloadData();
        window.location.reload();
      }
    });
  }

  homeLink()
  {
    this.router.navigate(['/']);
  }

  recapsLink()
  {
    this.router.navigate(['/recaps']);
  }

  fantasyLink()
  {
    this.router.navigate(['/fantasy']);
  }
}