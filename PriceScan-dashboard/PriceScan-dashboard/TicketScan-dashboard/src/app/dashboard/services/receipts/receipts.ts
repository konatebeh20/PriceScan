import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Receipts {
  private apiUrl = 'http://localhost:5000/api/receipts';

  constructor(private http: HttpClient) {}

  uploadReceipt(file: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/upload`, file);
  }

  getHistory(userId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/history/${userId}`);
  }
}
