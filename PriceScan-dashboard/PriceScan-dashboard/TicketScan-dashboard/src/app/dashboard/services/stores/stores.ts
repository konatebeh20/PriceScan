import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StoreService {
  private apiUrl = 'http://localhost:5000/api/stores';

  constructor(private http: HttpClient) {}

  getAll(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  getById(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  create(store: any): Observable<any> {
    return this.http.post(this.apiUrl, store);
  }

  update(id: string, store: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, store);
  }

  delete(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  getStores(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}
