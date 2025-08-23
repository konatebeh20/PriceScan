import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { 
  Product, 
  Store, 
  Receipt, 
  User, 
  SearchResult,
  BarcodeScanResult,
  SearchFilters 
} from './interfaces';
import { ApiResponse } from './api-interfaces';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = environment.apiUrl;
  private headers = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  constructor(private http: HttpClient) {}

  // Generic error handler
  private handleError(error: any): Observable<never> {
    console.error('API Error:', error);
    return throwError(() => new Error(error.error?.message || 'Une erreur est survenue'));
  }

  // Set authentication token
  setAuthToken(token: string): void {
    this.headers = this.headers.set('Authorization', `Bearer ${token}`);
  }

  // Clear authentication token
  clearAuthToken(): void {
    this.headers = this.headers.delete('Authorization');
  }

  // Generic GET request
  get<T>(endpoint: string, params?: HttpParams): Observable<ApiResponse<T>> {
    return this.http.get<ApiResponse<T>>(`${this.baseUrl}${endpoint}`, { 
      headers: this.headers, 
      params 
    }).pipe(
      catchError(this.handleError)
    );
  }

  // Generic POST request
  post<T>(endpoint: string, data: any): Observable<ApiResponse<T>> {
    return this.http.post<ApiResponse<T>>(`${this.baseUrl}${endpoint}`, data, { 
      headers: this.headers 
    }).pipe(
      catchError(this.handleError)
    );
  }

  // Generic PUT request
  put<T>(endpoint: string, data: any): Observable<ApiResponse<T>> {
    return this.http.put<ApiResponse<T>>(`${this.baseUrl}${endpoint}`, data, { 
      headers: this.headers 
    }).pipe(
      catchError(this.handleError)
    );
  }

  // Generic DELETE request
  delete<T>(endpoint: string): Observable<ApiResponse<T>> {
    return this.http.delete<ApiResponse<T>>(`${this.baseUrl}${endpoint}`, { 
      headers: this.headers 
    }).pipe(
      catchError(this.handleError)
    );
  }

  // Generic PATCH request
  patch<T>(endpoint: string, data: any): Observable<ApiResponse<T>> {
    return this.http.patch<ApiResponse<T>>(`${this.baseUrl}${endpoint}`, data, { 
      headers: this.headers 
    }).pipe(
      catchError(this.handleError)
    );
  }

  // File upload
  uploadFile<T>(endpoint: string, file: File, additionalData?: any): Observable<ApiResponse<T>> {
    const formData = new FormData();
    formData.append('file', file);
    
    if (additionalData) {
      Object.keys(additionalData).forEach(key => {
        formData.append(key, additionalData[key]);
      });
    }

    return this.http.post<ApiResponse<T>>(`${this.baseUrl}${endpoint}`, formData, { 
      headers: new HttpHeaders().delete('Content-Type') // Let browser set content-type for FormData
    }).pipe(
      catchError(this.handleError)
    );
  }

  // Health check
  healthCheck(): Observable<boolean> {
    return this.http.get(`${this.baseUrl}/health`, { 
      headers: this.headers,
      responseType: 'text'
    }).pipe(
      map(() => true),
      catchError(() => throwError(() => new Error('API non disponible')))
    );
  }

  // Get API status
  getApiStatus(): Observable<{ status: string; timestamp: Date }> {
    return this.http.get<{ status: string; timestamp: string }>(`${this.baseUrl}/status`, { 
      headers: this.headers 
    }).pipe(
      map(response => ({
        status: response.status,
        timestamp: new Date(response.timestamp)
      })),
      catchError(this.handleError)
    );
  }
}
