import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PriceService {
  private apiUrl = `${environment.apiUrl}/prices`;

  constructor(private http: HttpClient) {}

  savePrice(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  getPrices(productCode: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/${productCode}`);
  }

  getProductInfo(productCode: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/product/${productCode}`);
  }
}