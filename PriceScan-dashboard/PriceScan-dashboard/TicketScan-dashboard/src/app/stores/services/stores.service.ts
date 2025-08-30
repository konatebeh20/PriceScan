import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map, tap, catchError } from 'rxjs/operators';

// Interface Store alignée avec la base de données
export interface Store {
  id: number;
  store_uid: string;
  store_name: string;
  store_address: string;
  store_city: string;
  store_country: string;
  store_phone?: string;
  store_email?: string;
  store_website?: string;
  store_logo?: string;
  store_is_active: boolean;
  creation_date: Date;
  updated_on: Date;
  
  // Champs calculés ou ajoutés par l'API (non présents dans la base)
  is_favorite?: boolean;
  store_status?: 'active' | 'archived';
}

// Interface pour la création/modification - Alignée avec la base de données
export interface StoreFormData {
  store_name: string;           // ✅ Nom du magasin (obligatoire)
  store_address: string;        // ✅ Adresse du magasin
  store_city: string;           // ✅ Ville du magasin
  store_country: string;        // ✅ Pays du magasin
  store_phone?: string;         // ✅ Téléphone (optionnel)
  store_email?: string;         // ✅ Email (optionnel)
  store_website?: string;       // ✅ Site web (optionnel)
}

@Injectable({
  providedIn: 'root'
})
export class StoresService {
  private readonly API_URL = 'http://localhost:5000/api/stores';
  
  // BehaviorSubject pour gérer l'état des magasins
  private storesSubject = new BehaviorSubject<Store[]>([]);
  public stores$ = this.storesSubject.asObservable();

  // Cache local
  private storesCache: Store[] = [];
  private lastFetch: number = 0;
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  constructor(private http: HttpClient) {
    this.loadStoresFromStorage();
  }

  // ========================================
  //  RÉCUPÉRATION DES MAGASINS
  // ========================================

  // Charger tous les magasins depuis l'API
  loadStores(): Observable<Store[]> {
    const now = Date.now();
    
    // Utiliser le cache si il est encore valide
    if (this.storesCache.length > 0 && (now - this.lastFetch) < this.CACHE_DURATION) {
      this.storesSubject.next(this.storesCache);
      return of(this.storesCache);
    }

    return this.http.get<Store[]>(this.API_URL).pipe(
      tap(stores => {
        this.storesCache = stores;
        this.lastFetch = now;
        this.storesSubject.next(stores);
        this.saveToStorage(stores);
        console.log(' Magasins chargés depuis l\'API:', stores.length);
      }),
      catchError(error => {
        console.error(' Erreur lors du chargement des magasins:', error);
        // Retourner les données du cache en cas d'erreur
        this.storesSubject.next(this.storesCache);
        return of(this.storesCache);
      })
    );
  }

  // Récupérer un magasin par ID
  getStoreById(id: number): Observable<Store | null> {
    const cachedStore = this.storesCache.find(store => store.id === id);
    if (cachedStore) {
      return of(cachedStore);
    }

    return this.http.get<Store>(`${this.API_URL}/${id}`).pipe(
      catchError(error => {
        console.error(` Erreur lors de la récupération du magasin ${id}:`, error);
        return of(null);
      })
    );
  }

  // ========================================
  //  CRÉATION ET MODIFICATION
  // ========================================

  // Créer un nouveau magasin
  createStore(storeData: StoreFormData): Observable<Store | null> {
    return this.http.post<Store>(this.API_URL, storeData).pipe(
      tap(newStore => {
        console.log(' Nouveau magasin créé:', newStore);
        this.addStoreToCache(newStore);
        this.storesSubject.next(this.storesCache);
        this.saveToStorage(this.storesCache);
      }),
      catchError(error => {
        console.error(' Erreur lors de la création du magasin:', error);
        return of(null);
      })
    );
  }

  // Mettre à jour un magasin
  updateStore(id: number, storeData: Partial<StoreFormData>): Observable<Store | null> {
    return this.http.put<Store>(`${this.API_URL}/${id}`, storeData).pipe(
      tap(updatedStore => {
        console.log(' Magasin mis à jour:', updatedStore);
        this.updateStoreInCache(updatedStore);
        this.storesSubject.next(this.storesCache);
        this.saveToStorage(this.storesCache);
      }),
      catchError(error => {
        console.error(` Erreur lors de la mise à jour du magasin ${id}:`, error);
        return of(null);
      })
    );
  }

  // ========================================
  // ⭐ GESTION DES FAVORIS
  // ========================================

  // Basculer le statut favori
  toggleFavorite(storeId: number): Observable<boolean> {
    const store = this.storesCache.find(s => s.id === storeId);
    if (!store) {
      return of(false);
    }

    const newFavoriteStatus = !store.is_favorite;
    
    return this.http.patch<{ response: string; message?: string }>(`${this.API_URL}/${storeId}`, {
      is_favorite: newFavoriteStatus
    }).pipe(
      map(response => {
        if (response.response === 'success') {
          // Mettre à jour le cache
          store.is_favorite = newFavoriteStatus;
          this.storesSubject.next(this.storesCache);
          this.saveToStorage(this.storesCache);
          console.log(' Statut favori mis à jour:', newFavoriteStatus);
          return true;
        }
        return false;
      }),
      catchError(error => {
        console.error(' Erreur lors de la mise à jour du favori:', error);
        return of(false);
      })
    );
  }

  // ========================================
  // 📁 GESTION DES STATUTS
  // ========================================

  // Archiver un magasin
  archiveStore(storeId: number): Observable<boolean> {
    return this.http.patch<{ response: string; message?: string }>(`${this.API_URL}/${storeId}`, {
      store_status: 'archived'
    }).pipe(
      map(response => {
        if (response.response === 'success') {
          // Mettre à jour le cache
          const store = this.storesCache.find(s => s.id === storeId);
          if (store) {
            store.store_status = 'archived';
            this.storesSubject.next(this.storesCache);
            this.saveToStorage(this.storesCache);
          }
          console.log(' Magasin archivé:', storeId);
          return true;
        }
        return false;
      }),
      catchError(error => {
        console.error(' Erreur lors de l\'archivage du magasin:', error);
        return of(false);
      })
    );
  }

  // Restaurer un magasin
  restoreStore(storeId: number): Observable<boolean> {
    return this.http.patch<{ response: string; message?: string }>(`${this.API_URL}/${storeId}`, {
      store_status: 'active'
    }).pipe(
      map(response => {
        if (response.response === 'success') {
          // Mettre à jour le cache
          const store = this.storesCache.find(s => s.id === storeId);
          if (store) {
            store.store_status = 'active';
            this.storesSubject.next(this.storesCache);
            this.saveToStorage(this.storesCache);
          }
          console.log(' Magasin restauré:', storeId);
          return true;
        }
        return false;
      }),
      catchError(error => {
        console.error(' Erreur lors de la restauration du magasin:', error);
        return of(false);
      })
    );
  }

  // ========================================
  // 🗑️ SUPPRESSION
  // ========================================

  // Supprimer un magasin
  deleteStore(storeId: number): Observable<boolean> {
    return this.http.delete<{ response: string; message?: string }>(`${this.API_URL}/${storeId}`).pipe(
      map(response => {
        if (response.response === 'success') {
          // Retirer du cache
          this.storesCache = this.storesCache.filter(s => s.id !== storeId);
          this.storesSubject.next(this.storesCache);
          this.saveToStorage(this.storesCache);
          console.log(' Magasin supprimé:', storeId);
          return true;
        }
        return false;
      }),
      catchError(error => {
        console.error(' Erreur lors de la suppression du magasin:', error);
        return of(false);
      })
    );
  }

  // ========================================
  //  FILTRES ET RECHERCHE
  // ========================================

  // Obtenir les magasins actifs
  getActiveStores(): Store[] {
    return this.storesCache.filter(store => store.store_status === 'active');
  }

  // Obtenir les magasins favoris
  getFavoriteStores(): Store[] {
    return this.storesCache.filter(store => store.is_favorite);
  }

  // Obtenir les magasins archivés
  getArchivedStores(): Store[] {
    return this.storesCache.filter(store => store.store_status === 'archived');
  }

  // Rechercher des magasins
  searchStores(query: string): Store[] {
    if (!query.trim()) return this.storesCache;
    
    const lowerQuery = query.toLowerCase();
    return this.storesCache.filter(store => 
      store.store_name.toLowerCase().includes(lowerQuery) ||
      store.store_city.toLowerCase().includes(lowerQuery) ||
      store.store_address?.toLowerCase().includes(lowerQuery) ||
      store.store_phone?.toLowerCase().includes(lowerQuery) ||
      store.store_email?.toLowerCase().includes(lowerQuery)
    );
  }

  getStoresByType(type: string): Store[] {
    // Retourner tous les magasins car store_type n'existe pas
    return this.storesCache;
  }

  // Filtrer par ville
  filterByCity(city: string): Store[] {
    if (!city) return this.storesCache;
    return this.storesCache.filter(store => store.store_city === city);
  }

  // ========================================
  //  STATISTIQUES
  // ========================================

  // Obtenir les statistiques
  getStats() {
    const total = this.storesCache.length;
    const active = this.getActiveStores().length;
    const favorites = this.getFavoriteStores().length;
    const archived = this.getArchivedStores().length;

    return {
      total,
      active,
      favorites,
      archived
    };
  }

  // ========================================
  // 💾 GESTION DU CACHE LOCAL
  // ========================================

  // Sauvegarder dans le session storage
  private saveToStorage(stores: Store[]): void {
    try {
      sessionStorage.setItem('stores_cache', JSON.stringify(stores));
      sessionStorage.setItem('stores_last_fetch', Date.now().toString());
    } catch (error) {
      console.warn(' Impossible de sauvegarder dans le session storage:', error);
    }
  }

  // Charger depuis le session storage
  private loadStoresFromStorage(): void {
    try {
      const cached = sessionStorage.getItem('stores_cache');
      const lastFetch = sessionStorage.getItem('stores_last_fetch');
      
      if (cached && lastFetch) {
        this.storesCache = JSON.parse(cached);
        this.lastFetch = parseInt(lastFetch);
        this.storesSubject.next(this.storesCache);
        console.log('📱 Magasins chargés depuis le cache local:', this.storesCache.length);
      }
    } catch (error) {
      console.warn(' Erreur lors du chargement du cache local:', error);
    }
  }

  // Ajouter un magasin au cache
  private addStoreToCache(store: Store): void {
    this.storesCache.unshift(store); // Ajouter au début
  }

  // Mettre à jour un magasin dans le cache
  private updateStoreInCache(updatedStore: Store): void {
    const index = this.storesCache.findIndex(s => s.id === updatedStore.id);
    if (index !== -1) {
      this.storesCache[index] = updatedStore;
    }
  }

  // ========================================
  //  RÉFRESH
  // ========================================

  // Forcer le rafraîchissement
  refreshStores(): Observable<Store[]> {
    this.lastFetch = 0; // Invalider le cache
    return this.loadStores();
  }

  // Obtenir les données actuelles
  getCurrentStores(): Store[] {
    return this.storesCache;
  }
}
