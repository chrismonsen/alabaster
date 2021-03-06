import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/map';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'alabaster';
  private apiUrl = 'http://localhost:5000/users';
  data: any = {};

  constructor(private http: Http) {
    console.log('hello user')
    this.getUsers();
    this.getData();
  }

  getData() {
    return this.http.get(this.apiUrl)
      .map((res: Response) => res.json())
  }

  getUsers() {
    this.getData().subscribe(data => {
      console.log(data);
      this.data = data
    })
  }


}
