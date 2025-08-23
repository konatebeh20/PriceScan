import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage-angular';

@Injectable({
  providedIn: 'root'
})
export class StorageService {
  private _storage: Storage | null = null;

  constructor(private storage: Storage) {
    this.init();
  }

  async init() {
    const storage = await this.storage.create();
    this._storage = storage;
  }

  // Sauvegarder des données
  async set(key: string, value: any): Promise<void> {
    if (this._storage) {
      await this._storage.set(key, value);
    }
  }

  // Récupérer des données
  async get(key: string): Promise<any> {
    if (this._storage) {
      return await this._storage.get(key);
    }
    return null;
  }

  // Supprimer des données
  async remove(key: string): Promise<void> {
    if (this._storage) {
      await this._storage.remove(key);
    }
  }

  // Vider tout le stockage
  async clear(): Promise<void> {
    if (this._storage) {
      await this._storage.clear();
    }
  }

  // Obtenir toutes les clés
  async keys(): Promise<string[]> {
    if (this._storage) {
      return await this._storage.keys();
    }
    return [];
  }

  // Obtenir la taille du stockage
  async length(): Promise<number> {
    if (this._storage) {
      return await this._storage.length();
    }
    return 0;
  }

  // Méthodes spécifiques pour les reçus
  async saveReceipt(receipt: any): Promise<void> {
    const receipts = await this.get('receipts') || [];
    receipts.push(receipt);
    await this.set('receipts', receipts);
  }

  async getReceipts(): Promise<any[]> {
    return await this.get('receipts') || [];
  }

  async updateReceipt(receiptId: string, updatedReceipt: any): Promise<void> {
    const receipts = await this.get('receipts') || [];
    const index = receipts.findIndex((r: any) => r.id === receiptId);
    if (index !== -1) {
      receipts[index] = updatedReceipt;
      await this.set('receipts', receipts);
    }
  }

  async deleteReceipt(receiptId: string): Promise<void> {
    const receipts = await this.get('receipts') || [];
    const filteredReceipts = receipts.filter((r: any) => r.id !== receiptId);
    await this.set('receipts', filteredReceipts);
  }

  // Méthodes spécifiques pour les produits
  async saveProduct(product: any): Promise<void> {
    const products = await this.get('products') || [];
    const existingIndex = products.findIndex((p: any) => p.id === product.id);
    
    if (existingIndex !== -1) {
      products[existingIndex] = product;
    } else {
      products.push(product);
    }
    
    await this.set('products', products);
  }

  async getProducts(): Promise<any[]> {
    return await this.get('products') || [];
  }

  async getProductById(productId: string): Promise<any> {
    const products = await this.get('products') || [];
    return products.find((p: any) => p.id === productId);
  }

  // Méthodes pour les favoris
  async addToFavorites(productId: string): Promise<void> {
    const favorites = await this.get('favorites') || [];
    if (!favorites.includes(productId)) {
      favorites.push(productId);
      await this.set('favorites', favorites);
    }
  }

  async removeFromFavorites(productId: string): Promise<void> {
    const favorites = await this.get('favorites') || [];
    const filteredFavorites = favorites.filter((id: string) => id !== productId);
    await this.set('favorites', filteredFavorites);
  }

  async getFavorites(): Promise<string[]> {
    return await this.get('favorites') || [];
  }

  async isFavorite(productId: string): Promise<boolean> {
    const favorites = await this.get('favorites') || [];
    return favorites.includes(productId);
  }

  // Méthodes pour les alertes de prix
  async savePriceAlert(alert: any): Promise<void> {
    const alerts = await this.get('priceAlerts') || [];
    const existingIndex = alerts.findIndex((a: any) => a.productId === alert.productId);
    
    if (existingIndex !== -1) {
      alerts[existingIndex] = alert;
    } else {
      alerts.push(alert);
    }
    
    await this.set('priceAlerts', alerts);
  }

  async getPriceAlerts(): Promise<any[]> {
    return await this.get('priceAlerts') || [];
  }

  async removePriceAlert(alertId: string): Promise<void> {
    const alerts = await this.get('priceAlerts') || [];
    const filteredAlerts = alerts.filter((a: any) => a.id !== alertId);
    await this.set('priceAlerts', filteredAlerts);
  }

  // Méthodes pour les paramètres utilisateur
  async saveUserSettings(settings: any): Promise<void> {
    await this.set('userSettings', settings);
  }

  async getUserSettings(): Promise<any> {
    return await this.get('userSettings') || {};
  }

  // Méthodes pour la synchronisation
  async setLastSyncTime(): Promise<void> {
    await this.set('lastSyncTime', new Date().toISOString());
  }

  async getLastSyncTime(): Promise<string> {
    return await this.get('lastSyncTime') || '';
  }

  async needsSync(): Promise<boolean> {
    const lastSync = await this.getLastSyncTime();
    if (!lastSync) return true;
    
    const lastSyncDate = new Date(lastSync);
    const now = new Date();
    const diffHours = (now.getTime() - lastSyncDate.getTime()) / (1000 * 60 * 60);
    
    // Synchroniser toutes les 6 heures
    return diffHours >= 6;
  }
}
