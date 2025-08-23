import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { ApiService } from './api.service';
import { 
  Product, 
  Store, 
  Receipt,
  PriceComparison,
  PriceComparisonResponse
} from './interfaces';

@Injectable({
  providedIn: 'root'
})
export class DataConsultationService {
  
  constructor(private apiService: ApiService) {}

  // ========================================
  // CONSULTATION DES PRODUITS
  // ========================================

  /**
   * Rechercher des produits par nom
   */
  searchProducts(query: string): Observable<Product[]> {
    return this.apiService.get<Product[]>(`/products/search?q=${encodeURIComponent(query)}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Rechercher un produit par code-barres
   */
  searchProductByBarcode(barcode: string): Observable<Product | null> {
    return this.apiService.get<Product>(`/products/barcode/${barcode}`).pipe(
      map(response => response.data!),
      catchError(() => from([null]))
    );
  }

  /**
   * Rechercher un produit par QR code
   */
  searchProductByQRCode(qrCode: string): Observable<Product | null> {
    return this.apiService.get<Product>(`/products/qrcode/${qrCode}`).pipe(
      map(response => response.data!),
      catchError(() => from([null]))
    );
  }

  /**
   * Obtenir les détails d'un produit
   */
  getProductDetails(productId: string): Observable<Product> {
    return this.apiService.get<Product>(`/products/${productId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les produits populaires
   */
  getPopularProducts(): Observable<Product[]> {
    return this.apiService.get<Product[]>('/products/popular').pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les produits par catégorie
   */
  getProductsByCategory(categoryId: string): Observable<Product[]> {
    return this.apiService.get<Product[]>(`/products/category/${categoryId}`).pipe(
      map(response => response.data!)
    );
  }

  // ========================================
  // COMPARAISON DE PRIX
  // ========================================

  /**
   * Comparer les prix d'un produit entre magasins
   */
  compareProductPrices(productId: string): Observable<PriceComparisonResponse> {
    return this.apiService.get<PriceComparisonResponse>(`/prices/compare/${productId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir l'historique des prix d'un produit
   */
  getProductPriceHistory(productId: string): Observable<any[]> {
    return this.apiService.get<any[]>(`/prices/history/${productId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les prix actuels d'un produit
   */
  getCurrentPrices(productId: string): Observable<any[]> {
    return this.apiService.get<any[]>(`/prices/current/${productId}`).pipe(
      map(response => response.data!)
    );
  }

  // ========================================
  // MAGASINS ET LOCALISATION
  // ========================================

  /**
   * Rechercher des magasins
   */
  searchStores(query: string, city?: string): Observable<Store[]> {
    const params = city ? `?q=${encodeURIComponent(query)}&city=${encodeURIComponent(city)}` : `?q=${encodeURIComponent(query)}`;
    return this.apiService.get<Store[]>(`/stores/search${params}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les magasins à proximité
   */
  getNearbyStores(latitude: number, longitude: number, radius: number = 5000): Observable<Store[]> {
    return this.apiService.get<Store[]>(`/stores/nearby?lat=${latitude}&lng=${longitude}&radius=${radius}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les détails d'un magasin
   */
  getStoreDetails(storeId: string): Observable<Store> {
    return this.apiService.get<Store>(`/stores/${storeId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir tous les magasins
   */
  getAllStores(): Observable<Store[]> {
    return this.apiService.get<Store[]>('/stores').pipe(
      map(response => response.data!)
    );
  }

  // ========================================
  // RECEIPTS (RECEIPTS)
  // ========================================

  /**
   * Obtenir les reçus d'un utilisateur
   */
  getUserReceipts(userId: string): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/user/${userId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir un reçu spécifique
   */
  getReceipt(receiptId: string): Observable<Receipt> {
    return this.apiService.get<Receipt>(`/receipts/${receiptId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les reçus par type
   */
  getReceiptsByType(type: string): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/type/${type}`).pipe(
      map(response => response.data!)
    );
  }

  // ========================================
  // STATISTIQUES ET ANALYSES
  // ========================================

  /**
   * Obtenir les statistiques d'un utilisateur
   */
  getUserStats(userId: string): Observable<any> {
    return this.apiService.get<any>(`/stats/user/${userId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les statistiques des prix
   */
  getPriceStats(): Observable<any> {
    return this.apiService.get<any>('/stats/prices').pipe(
      map(response => response.data!)
    );
  }

  /**
   * Obtenir les statistiques des magasins
   */
  getStoreStats(): Observable<any> {
    return this.apiService.get<any>('/stats/stores').pipe(
      map(response => response.data!)
    );
  }

  // ========================================
  // FAVORIS
  // ========================================

  /**
   * Obtenir les produits favoris d'un utilisateur
   */
  getUserFavorites(userId: string): Observable<Product[]> {
    return this.apiService.get<Product[]>(`/favorites/user/${userId}`).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Ajouter un produit aux favoris
   */
  addToFavorites(userId: string, productId: string): Observable<any> {
    return this.apiService.post<any>('/favorites/add', { userId, productId }).pipe(
      map(response => response.data!)
    );
  }

  /**
   * Retirer un produit des favoris
   */
  removeFromFavorites(userId: string, productId: string): Observable<any> {
    return this.apiService.delete<any>(`/favorites/remove/${userId}/${productId}`).pipe(
      map(response => response.data!)
    );
  }

  // ========================================
  // UTILITAIRES
  // ========================================

  /**
   * Vérifier la disponibilité du service
   */
  isServiceAvailable(): Observable<boolean> {
    return this.apiService.get<any>('/health').pipe(
      map(() => true),
      catchError(() => from([false]))
    );
  }

  /**
   * Obtenir les informations système
   */
  getSystemInfo(): Observable<any> {
    return this.apiService.get<any>('/system/info').pipe(
      map(response => response.data!)
    );
  }
}
