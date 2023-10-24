import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-full-preview-page',
  templateUrl: './full-preview-page.component.html',
  styleUrls: ['./full-preview-page.component.css']
})
export class FullPreviewPageComponent implements OnInit {
  gameID!: string;

  constructor(private router: Router, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.gameID = params['gameID'];
    })
  }

  ngOnInit() {
    console.log(this.gameID);
    //const gameID: any = this.route.snapshot.queryParamMap.get('gameID');

    // Something else here
  }

}
