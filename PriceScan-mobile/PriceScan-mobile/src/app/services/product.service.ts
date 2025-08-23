import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';

export interface Product {
  id?: string;
  name: string;
  description?: string;
  category: string;
  brand?: string;
  barcode?: string;
  imageUrl?: string;
  averagePrice?: number;
  lowestPrice?: number;
  highestPrice?: number;
  priceHistory?: PricePoint[];
  createdAt?: string;
  updatedAt?: string;
}

export interface PricePoint {
  id?: string;
  price: number;
  store: string;
  date: string;
  availability: boolean;
}

export interface PriceComparison {
  product: Product;
  prices: StorePrice[];
  bestPrice: StorePrice;
  averagePrice: number;
  priceRange: {
    min: number;
    max: number;
  };
}

export interface StorePrice {
  id?: string;
  storeName: string;
  storeLogo?: string;
  price: number;
  availability: boolean;
  lastUpdated: string;
  shippingCost?: number;
  totalCost: number;
  rating?: number;
  reviewCount?: number;
}

export interface SearchFilters {
  category?: string;
  brand?: string;
  minPrice?: number;
  maxPrice?: number;
  availability?: boolean;
  sortBy?: 'price' | 'rating' | 'name' | 'date';
  sortOrder?: 'asc' | 'desc';
}

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  constructor(private apiService: ApiService) { }

  // Rechercher des produits
  searchProducts(query: string, filters?: SearchFilters): Observable<Product[]> {
    let endpoint = `/products/search?q=${encodeURIComponent(query)}`;
    
    if (filters) {
      if (filters.category) endpoint += `&category=${filters.category}`;
      if (filters.brand) endpoint += `&brand=${filters.brand}`;
      if (filters.minPrice) endpoint += `&minPrice=${filters.minPrice}`;
      if (filters.maxPrice) endpoint += `&maxPrice=${filters.maxPrice}`;
      if (filters.availability !== undefined) endpoint += `&availability=${filters.availability}`;
      if (filters.sortBy) endpoint += `&sortBy=${filters.sortBy}`;
      if (filters.sortOrder) endpoint += `&sortOrder=${filters.sortOrder}`;
    }
    
    return this.apiService.get<Product[]>(endpoint);
  }

  // Rechercher par code-barres
  searchByBarcode(barcode: string): Observable<Product> {
    return this.apiService.get<Product>(`/products/barcode/${barcode}`);
  }

  // Obtenir la comparaison de prix pour un produit
  getPriceComparison(productId: string): Observable<PriceComparison> {
    return this.apiService.get<PriceComparison>(`/products/${productId}/prices`);
  }

  // Obtenir l'historique des prix
  getPriceHistory(productId: string, days: number = 30): Observable<PricePoint[]> {
    return this.apiService.get<PricePoint[]>(`/products/${productId}/price-history?days=${days}`);
  }

  // Obtenir les produits populaires
  getPopularProducts(limit: number = 10): Observable<Product[]> {
    return this.apiService.get<Product[]>(`/products/popular?limit=${limit}`);
  }

  // Obtenir les produits par catégorie
  getProductsByCategory(category: string, limit: number = 20): Observable<Product[]> {
    return this.apiService.get<Product[]>(`/products/category/${category}?limit=${limit}`);
  }

  // Obtenir les détails d'un produit
  getProductDetails(productId: string): Observable<Product> {
    return this.apiService.get<Product>(`/products/${productId}`);
  }

  // Ajouter un produit aux favoris
  addToFavorites(productId: string, userId: string): Observable<any> {
    return this.apiService.post<any>('/favorites', { productId, userId });
  }

  // Supprimer un produit des favoris
  removeFromFavorites(productId: string, userId: string): Observable<any> {
    return this.apiService.delete<any>(`/favorites/${productId}?userId=${userId}`);
  }

  // Obtenir les favoris d'un utilisateur
  getUserFavorites(userId: string): Observable<Product[]> {
    return this.apiService.get<Product[]>(`/favorites/user/${userId}`);
  }

  // Définir une alerte de prix
  setPriceAlert(productId: string, userId: string, targetPrice: number): Observable<any> {
    return this.apiService.post<any>('/price-alerts', {
      productId,
      userId,
      targetPrice
    });
  }

  // Obtenir les alertes de prix d'un utilisateur
  getUserPriceAlerts(userId: string): Observable<any[]> {
    return this.apiService.get<any[]>(`/price-alerts/user/${userId}`);
  }

  // Supprimer une alerte de prix
  removePriceAlert(alertId: string): Observable<any> {
    return this.apiService.delete<any>(`/price-alerts/${alertId}`);
  }

  // Obtenir les suggestions de produits
  getProductSuggestions(query: string): Observable<string[]> {
    return this.apiService.get<string[]>(`/products/suggestions?q=${encodeURIComponent(query)}`);
  }

  // Obtenir les catégories disponibles
  getCategories(): Observable<string[]> {
    return this.apiService.get<string[]>('/products/categories');
  }

  // Obtenir les marques disponibles
  getBrands(): Observable<string[]> {
    return this.apiService.get<string[]>('/products/brands');
  }
}
