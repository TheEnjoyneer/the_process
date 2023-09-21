import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ 
    HttpClientModule
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  newdata:any;

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