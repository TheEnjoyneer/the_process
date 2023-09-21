import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({ providedIn: 'root' })
export class ApiserviceService {

    constructor(private http: HttpClient) { }

    getdata(): any  {
        return this.http.get('http://127.0.0.1:5000/topGame').pipe((data) => {
            console.log(data);
            return data;
        });
    }
}