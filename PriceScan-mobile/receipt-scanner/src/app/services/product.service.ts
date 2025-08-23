import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { ApiService } from './api.service';
import { 
  Product, 
  Store, 
  SearchResult, 
  SearchFilters, 
  BarcodeScanResult,
  PriceComparison,
  ApiResponse 
} from './interfaces';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private searchResultsSubject = new BehaviorSubject<SearchResult | null>(null);
  private currentProductSubject = new BehaviorSubject<Product | null>(null);
  private priceComparisonSubject = new BehaviorSubject<PriceComparison[]>([]);

  public searchResults$ = this.searchResultsSubject.asObservable();
  public currentProduct$ = this.currentProductSubject.asObservable();
  public priceComparison$ = this.priceComparisonSubject.asObservable();

  constructor(private apiService: ApiService) {}

  // Search products
  searchProducts(query: string, filters?: SearchFilters, page: number = 1): Observable<SearchResult> {
    const params = new URLSearchParams();
    params.set('q', query);
    params.set('page', page.toString());
    
    if (filters) {
      if (filters.category) params.set('category', filters.category);
      if (filters.priceRange) {
        params.set('minPrice', filters.priceRange.min.toString());
        params.set('maxPrice', filters.priceRange.max.toString());
      }
      if (filters.location) {
        params.set('lat', filters.location.latitude.toString());
        params.set('lng', filters.location.longitude.toString());
        params.set('radius', filters.location.radius.toString());
      }
      if (filters.storeType) params.set('storeType', filters.storeType.join(','));
      if (filters.inStock !== undefined) params.set('inStock', filters.inStock.toString());
      if (filters.rating) params.set('rating', filters.rating.toString());
    }

    return this.apiService.get<SearchResult>(`/products/search?${params.toString()}`).pipe(
      map(response => response.data!),
      tap(results => this.searchResultsSubject.next(results))
    );
  }

  // Get product by ID
  getProductById(id: string): Observable<Product> {
    return this.apiService.get<Product>(`/products/${id}`).pipe(
      map(response => response.data!),
      tap(product => this.currentProductSubject.next(product))
    );
  }

  // Get product by barcode
  getProductByBarcode(barcode: string): Observable<Product> {
    return this.apiService.get<Product>(`/products/barcode/${barcode}`).pipe(
      map(response => response.data!),
      tap(product => this.currentProductSubject.next(product))
    );
  }

  // Scan barcode and get product info
  scanBarcode(barcode: string, location?: { latitude: number; longitude: number }): Observable<BarcodeScanResult> {
    const data: any = { barcode };
    if (location) {
      data.latitude = location.latitude;
      data.longitude = location.longitude;
    }

    return this.apiService.post<BarcodeScanResult>('/products/scan', data).pipe(
      map(response => response.data!)
    );
  }

  // Get price comparison for a product
  getPriceComparison(productId: string, location?: { latitude: number; longitude: number }): Observable<PriceComparison[]> {
    const params = new URLSearchParams();
    if (location) {
      params.set('lat', location.latitude.toString());
      params.set('lng', location.longitude.toString());
    }

    return this.apiService.get<PriceComparison[]>(`/products/${productId}/prices?${params.toString()}`).pipe(
      map(response => response.data!),
      tap(prices => this.priceComparisonSubject.next(prices))
    );
  }

  // Get nearby stores for a product
  getNearbyStores(productId: string, latitude: number, longitude: number, radius: number = 10): Observable<Store[]> {
    const params = new URLSearchParams();
    params.set('lat', latitude.toString());
    params.set('lng', longitude.toString());
    params.set('radius', radius.toString());

    return this.apiService.get<Store[]>(`/products/${productId}/stores/nearby?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Get popular products
  getPopularProducts(limit: number = 10): Observable<Product[]> {
    return this.apiService.get<Product[]>(`/products/popular?limit=${limit}`).pipe(
      map(response => response.data!)
    );
  }

  // Get products by category
  getProductsByCategory(category: string, page: number = 1): Observable<SearchResult> {
    const params = new URLSearchParams();
    params.set('category', category);
    params.set('page', page.toString());

    return this.apiService.get<SearchResult>(`/products/category?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Get trending products
  getTrendingProducts(period: 'day' | 'week' | 'month' = 'week', limit: number = 10): Observable<Product[]> {
    const params = new URLSearchParams();
    params.set('period', period);
    params.set('limit', limit.toString());

    return this.apiService.get<Product[]>(`/products/trending?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Get product price history
  getProductPriceHistory(productId: string, period: 'month' | 'quarter' | 'year' = 'month'): Observable<any[]> {
    return this.apiService.get<any[]>(`/products/${productId}/price-history?period=${period}`).pipe(
      map(response => response.data!)
    );
  }

  // Set price alert
  setPriceAlert(productId: string, targetPrice: number): Observable<any> {
    return this.apiService.post<any>('/products/price-alerts', {
      productId,
      targetPrice
    }).pipe(
      map(response => response.data!)
    );
  }

  // Get user's price alerts
  getUserPriceAlerts(): Observable<any[]> {
    return this.apiService.get<any[]>('/products/price-alerts').pipe(
      map(response => response.data!)
    );
  }

  // Delete price alert
  deletePriceAlert(alertId: string): Observable<any> {
    return this.apiService.delete<any>(`/products/price-alerts/${alertId}`).pipe(
      map(response => response.data!)
    );
  }

  // Get current search results
  getCurrentSearchResults(): SearchResult | null {
    return this.searchResultsSubject.value;
  }

  // Get current product
  getCurrentProduct(): Product | null {
    return this.currentProductSubject.value;
  }

  // Get current price comparison
  getCurrentPriceComparison(): PriceComparison[] {
    return this.priceComparisonSubject.value;
  }

  // Clear search results
  clearSearchResults(): void {
    this.searchResultsSubject.next(null);
  }

  // Clear current product
  clearCurrentProduct(): void {
    this.currentProductSubject.next(null);
  }

  // Clear price comparison
  clearPriceComparison(): void {
    this.priceComparisonSubject.next([]);
  }
}
