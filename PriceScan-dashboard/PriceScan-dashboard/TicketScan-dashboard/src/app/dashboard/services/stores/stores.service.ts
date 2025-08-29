import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { getApiConfig } from '../api/api.config';

export interface Store {
  id: string;
  name: string;
  type: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre';
  address: string;
  city: string;
  phone?: string;
  email?: string;
  description?: string;
  status: 'active' | 'archived';
  isFavorite: boolean;
  receiptsCount: number;
  totalSpent: number;
  lastVisit: Date;
  createdAt: Date;
  updatedAt: Date;
}

@Injectable({
  providedIn: 'root'
})
export class StoresService {
  private readonly STORAGE_KEY = 'ticketscan_stores';
  private readonly API_URL = getApiConfig().STORES.BASE;

  private storesSubject = new BehaviorSubject<Store[]>([]);
  public stores$ = this.storesSubject.asObservable();

  constructor() {
    this.loadFromStorage();
    this.loadFromDatabase();
  }

  private loadFromStorage(): void {
    try {
      const stored = sessionStorage.getItem(this.STORAGE_KEY);
      if (stored) {
        const stores = JSON.parse(stored).map((store: any) => ({
          ...store,
          lastVisit: new Date(store.lastVisit),
          createdAt: new Date(store.createdAt),
          updatedAt: new Date(store.updatedAt)
        }));
        this.storesSubject.next(stores);
      }
    } catch (error) {
      console.error('Erreur lors du chargement depuis le stockage:', error);
    }
  }

  private saveToStorage(stores: Store[]): void {
    try {
      console.log('💾 [StoresService] Sauvegarde dans le session storage:', stores.length, 'magasins');
      console.log('🔑 [StoresService] Clé de stockage:', this.STORAGE_KEY);
      
      const dataToStore = JSON.stringify(stores);
      console.log('📦 [StoresService] Données à stocker (taille):', dataToStore.length, 'caractères');
      
      sessionStorage.setItem(this.STORAGE_KEY, dataToStore);
      
      // Vérification immédiate
      const verification = sessionStorage.getItem(this.STORAGE_KEY);
      if (verification) {
        const parsed = JSON.parse(verification);
        console.log('✅ [StoresService] Vérification session storage réussie:', parsed.length, 'magasins stockés');
      } else {
        console.error('❌ [StoresService] Échec de la vérification session storage');
      }
    } catch (error) {
      console.error('❌ [StoresService] Erreur lors de la sauvegarde dans le stockage:', error);
    }
  }

  getStores(): Observable<Store[]> {
    return this.stores$;
  }

  getCurrentStores(): Store[] {
    return this.storesSubject.value;
  }

  addStore(store: Omit<Store, 'id' | 'createdAt' | 'updatedAt'>): Promise<Store> {
    return new Promise((resolve, reject) => {
      console.log('🔄 [StoresService] Début de l\'ajout du magasin:', store);
      
      const newStore: Store = {
        ...store,
        id: this.generateId(),
        createdAt: new Date(),
        updatedAt: new Date()
      };

      console.log('✅ [StoresService] Nouveau magasin créé avec ID:', newStore.id);

      const currentStores = this.storesSubject.value;
      const updatedStores = [...currentStores, newStore];
      
      console.log('📊 [StoresService] Nombre total de magasins après ajout:', updatedStores.length);
      
      // Mettre à jour le BehaviorSubject
      this.storesSubject.next(updatedStores);
      console.log('🔄 [StoresService] BehaviorSubject mis à jour');
      
      // Sauvegarder dans le session storage
      this.saveToStorage(updatedStores);
      console.log('💾 [StoresService] Session storage mis à jour');
      
      // Vérifier le session storage
      const storedData = sessionStorage.getItem(this.STORAGE_KEY);
      console.log('🔍 [StoresService] Vérification session storage:', storedData ? 'Données présentes' : 'Aucune donnée');
      
      // Synchroniser avec la base de données
      this.syncToDatabase(newStore, 'create')
        .then(() => {
          console.log('✅ [StoresService] Synchronisation avec la base de données réussie');
          resolve(newStore);
        })
        .catch(error => {
          console.error('❌ [StoresService] Erreur lors de la synchronisation:', error);
          reject(error);
        });
    });
  }

  updateStore(id: string, updates: Partial<Store>): Promise<Store> {
    return new Promise((resolve, reject) => {
      const currentStores = this.storesSubject.value;
      const storeIndex = currentStores.findIndex(s => s.id === id);
      
      if (storeIndex === -1) {
        reject(new Error('Magasin non trouvé'));
        return;
      }

      const updatedStore = {
        ...currentStores[storeIndex],
        ...updates,
        updatedAt: new Date()
      };

      const updatedStores = [...currentStores];
      updatedStores[storeIndex] = updatedStore;
      
      this.storesSubject.next(updatedStores);
      this.saveToStorage(updatedStores);
      
      this.syncToDatabase(updatedStore, 'update')
        .then(() => resolve(updatedStore))
        .catch(reject);
    });
  }

  deleteStore(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const currentStores = this.storesSubject.value;
      const storeToDelete = currentStores.find(s => s.id === id);
      
      if (!storeToDelete) {
        reject(new Error('Magasin non trouvé'));
        return;
      }

      const updatedStores = currentStores.filter(s => s.id !== id);
      this.storesSubject.next(updatedStores);
      this.saveToStorage(updatedStores);
      
      this.syncToDatabase(storeToDelete, 'delete')
        .then(() => resolve())
        .catch(reject);
    });
  }

  toggleFavorite(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const currentStores = this.storesSubject.value;
      const storeIndex = currentStores.findIndex(s => s.id === id);
      
      if (storeIndex === -1) {
        reject(new Error('Magasin non trouvé'));
        return;
      }

      const updatedStore = {
        ...currentStores[storeIndex],
        isFavorite: !currentStores[storeIndex].isFavorite,
        updatedAt: new Date()
      };

      const updatedStores = [...currentStores];
      updatedStores[storeIndex] = updatedStore;
      
      this.storesSubject.next(updatedStores);
      this.saveToStorage(updatedStores);
      
      this.syncToDatabase(updatedStore, 'update')
        .then(() => resolve())
        .catch(reject);
    });
  }

  archiveStore(id: string): Promise<void> {
    return this.updateStore(id, { status: 'archived' }).then(() => {});
  }

  restoreStore(id: string): Promise<void> {
    return this.updateStore(id, { status: 'active' }).then(() => {});
  }

  searchStoresByName(query: string): Store[] {
    const stores = this.storesSubject.value;
    return stores.filter(store => 
      store.name.toLowerCase().includes(query.toLowerCase())
    );
  }

  getStoresByType(type: string): Store[] {
    const stores = this.storesSubject.value;
    return stores.filter(store => store.type === type);
  }

  getFavoriteStores(): Store[] {
    const stores = this.storesSubject.value;
    return stores.filter(store => store.isFavorite);
  }

  private generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  private async syncToDatabase(store: Store, action: 'create' | 'update' | 'delete'): Promise<void> {
    try {
      console.log(`🔄 [StoresService] Début synchronisation ${action} avec la base de données`);
      console.log(`🌐 [StoresService] URL API:`, this.API_URL);
      console.log(`📤 [StoresService] Données à envoyer:`, store);
      
      const url = action === 'delete' 
        ? `${this.API_URL}/${store.id}`
        : this.API_URL;

      const method = action === 'create' ? 'POST' : action === 'update' ? 'PUT' : 'DELETE';
      console.log(`📡 [StoresService] Méthode HTTP:`, method);
      
      const response = await fetch(url, {
        method,
        headers: {
          ...getApiConfig().DEFAULT_HEADERS
        },
        body: action !== 'delete' ? JSON.stringify(store) : undefined
      });

      console.log(`📥 [StoresService] Réponse API reçue:`, response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ [StoresService] Erreur API ${response.status}:`, errorText);
        throw new Error(`Erreur API: ${response.status} - ${errorText}`);
      }

      console.log(`✅ [StoresService] Magasin ${action === 'create' ? 'créé' : action === 'update' ? 'mis à jour' : 'supprimé'} avec succès dans la base de données`);
    } catch (error) {
      console.error(`❌ [StoresService] Erreur lors de la synchronisation avec la base de données (${action}):`, error);
      // Ne pas rejeter - on garde les données en local même si la sync échoue
      console.log(`⚠️ [StoresService] Les données restent en local malgré l'échec de la synchronisation`);
    }
  }

  async loadFromDatabase(): Promise<void> {
    try {
      const response = await fetch(this.API_URL, {
        headers: getApiConfig().DEFAULT_HEADERS
      });

      if (response.ok) {
        const stores = await response.json();
        const storesWithDates = stores.map((store: any) => ({
          ...store,
          lastVisit: new Date(store.lastVisit),
          createdAt: new Date(store.createdAt),
          updatedAt: new Date(store.updatedAt)
        }));
        
        this.storesSubject.next(storesWithDates);
        this.saveToStorage(storesWithDates);
      }
    } catch (error) {
      console.error('Erreur lors du chargement depuis la base de données:', error);
    }
  }

  clearStorage(): void {
    sessionStorage.removeItem(this.STORAGE_KEY);
    this.storesSubject.next([]);
  }
}
