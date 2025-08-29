import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Price {
  private apiUrl = 'http://localhost:5000/api/prices';

  constructor(private http: HttpClient) {}

  compare(productId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/compare/${productId}`);
  }
}
