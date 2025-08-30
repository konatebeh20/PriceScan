import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { getApiConfig } from '../api/api.config';

export interface Store {
  id: number;
  store_uid: string;
  store_name: string;
  store_address?: string;
  store_city?: string;
  store_country?: string;
  store_phone?: string;
  store_email?: string;
  store_website?: string;
  store_logo?: string;
  creation_date?: string;
  updated_on?: string;
  // Propriétés supplémentaires pour la compatibilité
  name?: string;
  type?: string;
  address?: string;
  city?: string;
  lastVisit?: Date;
  createdAt?: Date;
  updatedAt?: Date;
  isFavorite?: boolean;
  status?: string;
  // Propriétés pour les statistiques
  receiptsCount?: number;
  totalSpent?: number;
}

@Injectable({
  providedIn: 'root'
})
export class StoresService {
  private readonly API_URL = getApiConfig().STORES.BASE;
  private storesSubject = new BehaviorSubject<Store[]>([]);
  public stores$ = this.storesSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadStores();
  }

  private loadStores(): void {
    this.http.get<any>(`${this.API_URL}`).subscribe({
      next: (response) => {
        if (response.response === 'success') {
          this.storesSubject.next(response.stores);
          console.log(' Magasins chargés:', response.stores.length);
        } else {
          console.error(' Erreur API magasins:', response.message);
        }
      },
      error: (error) => {
        console.error(' Erreur lors du chargement des magasins:', error);
      }
    });
  }

  getStores(): Observable<Store[]> {
    return this.stores$;
  }

  getCurrentStores(): Store[] {
    return this.storesSubject.value;
  }

  getStoreById(id: number): Store | undefined {
    return this.getCurrentStores().find(store => store.id === id);
  }

  refreshStores(): void {
    this.loadStores();
  }

  // Méthodes CRUD manquantes
  addStore(storeData: Partial<Store>): Promise<Store> {
    return new Promise((resolve, reject) => {
      this.http.post<any>(`${this.API_URL}`, storeData).subscribe({
        next: (response) => {
          if (response.response === 'success') {
            this.refreshStores();
            resolve(response.store);
          } else {
            reject(new Error(response.message || 'Erreur lors de l\'ajout du magasin'));
          }
        },
        error: (error) => reject(error)
      });
    });
  }

  updateStore(id: string, storeData: Partial<Store>): Promise<Store> {
    return new Promise((resolve, reject) => {
      this.http.put<any>(`${this.API_URL}/${id}`, storeData).subscribe({
        next: (response) => {
          if (response.response === 'success') {
            this.refreshStores();
            resolve(response.store);
          } else {
            reject(new Error(response.message || 'Erreur lors de la mise à jour du magasin'));
          }
        },
        error: (error) => reject(error)
      });
    });
  }

  deleteStore(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.http.delete<any>(`${this.API_URL}/${id}`).subscribe({
        next: (response) => {
          if (response.response === 'success') {
            this.refreshStores();
            resolve();
          } else {
            reject(new Error(response.message || 'Erreur lors de la suppression du magasin'));
          }
        },
        error: (error) => reject(error)
      });
    });
  }

  toggleFavorite(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      // Simuler le changement de favori
      const stores = this.getCurrentStores();
      const store = stores.find(s => s.id.toString() === id);
      if (store) {
        store.isFavorite = !store.isFavorite;
        this.storesSubject.next([...stores]);
        resolve();
      } else {
        reject(new Error('Magasin non trouvé'));
      }
    });
  }

  archiveStore(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.updateStore(id, { status: 'archived' })
        .then(() => resolve())
        .catch(reject);
    });
  }

  restoreStore(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.updateStore(id, { status: 'active' })
        .then(() => resolve())
        .catch(reject);
    });
  }
}
