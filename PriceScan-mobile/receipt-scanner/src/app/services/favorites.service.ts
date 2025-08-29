import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface FavoriteProduct {
  id: number;
  product: string;
  barcode: string;
  timestamp: string;
  price: number;
  store: string;
  isFavorite: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class FavoritesService {
  private favoritesSubject = new BehaviorSubject<number[]>([]);
  private historyFavoritesSubject = new BehaviorSubject<FavoriteProduct[]>([]);

  constructor() {
    this.loadFavorites();
    this.loadHistoryFavorites();
  }

  // Observable pour les IDs des favoris
  get favorites$(): Observable<number[]> {
    return this.favoritesSubject.asObservable();
  }

  // Observable pour les favoris de l'historique
  get historyFavorites$(): Observable<FavoriteProduct[]> {
    return this.historyFavoritesSubject.asObservable();
  }

  // Méthodes pour gérer les favoris
  addToFavorites(productId: number): void {
    const currentFavorites = this.favoritesSubject.value;
    if (!currentFavorites.includes(productId)) {
      const newFavorites = [...currentFavorites, productId];
      this.favoritesSubject.next(newFavorites);
      localStorage.setItem('ps_favorites', JSON.stringify(newFavorites));
    }
  }

  removeFromFavorites(productId: number): void {
    const currentFavorites = this.favoritesSubject.value;
    const newFavorites = currentFavorites.filter(id => id !== productId);
    this.favoritesSubject.next(newFavorites);
    localStorage.setItem('ps_favorites', JSON.stringify(newFavorites));
  }

  isFavorite(productId: number): boolean {
    return this.favoritesSubject.value.includes(productId);
  }

  // Méthodes pour gérer les favoris de l'historique
  addToHistoryFavorites(product: any): void {
    const currentHistoryFavorites = this.historyFavoritesSubject.value;
    const newFavorite: FavoriteProduct = {
      id: product.id,
      product: product.name,
      barcode: `FAV_${product.id}`,
      timestamp: new Date().toISOString(),
      price: product.currentPrice || product.price,
      store: product.store,
      isFavorite: true
    };

    // Vérifier si pas déjà présent
    if (!currentHistoryFavorites.find(f => f.id === product.id)) {
      const newHistoryFavorites = [...currentHistoryFavorites, newFavorite];
      this.historyFavoritesSubject.next(newHistoryFavorites);
      localStorage.setItem('ps_history_favorites', JSON.stringify(newHistoryFavorites));
    }
  }

  removeFromHistoryFavorites(productId: number): void {
    const currentHistoryFavorites = this.historyFavoritesSubject.value;
    const newHistoryFavorites = currentHistoryFavorites.filter(f => f.id !== productId);
    this.historyFavoritesSubject.next(newHistoryFavorites);
    localStorage.setItem('ps_history_favorites', JSON.stringify(newHistoryFavorites));
  }

  // Charger les favoris depuis le localStorage
  private loadFavorites(): void {
    try {
      const stored = localStorage.getItem('ps_favorites');
      if (stored) {
        const favorites = JSON.parse(stored);
        this.favoritesSubject.next(favorites);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des favoris:', error);
    }
  }

  // Charger les favoris de l'historique depuis le localStorage
  private loadHistoryFavorites(): void {
    try {
      const stored = localStorage.getItem('ps_history_favorites');
      if (stored) {
        const historyFavorites = JSON.parse(stored);
        this.historyFavoritesSubject.next(historyFavorites);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des favoris de l\'historique:', error);
    }
  }

  // Rafraîchir les données
  refresh(): void {
    this.loadFavorites();
    this.loadHistoryFavorites();
  }
}
