import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage-angular';
import { BehaviorSubject, Observable } from 'rxjs';
import { 
  User, 
  UserPreferences, 
  LocalStorageData 
} from './interfaces';

@Injectable({
  providedIn: 'root'
})
export class StorageService {
  private _storage: Storage | null = null;
  private userSubject = new BehaviorSubject<User | null>(null);
  private preferencesSubject = new BehaviorSubject<UserPreferences | null>(null);

  public user$ = this.userSubject.asObservable();
  public preferences$ = this.preferencesSubject.asObservable();

  constructor(private storage: Storage) {
    this.init();
  }

  async init() {
    const storage = await this.storage.create();
    this._storage = storage;
    await this.loadUserData();
  }

  // User data management
  async setUser(user: User): Promise<void> {
    await this._storage?.set('user', user);
    this.userSubject.next(user);
    
    // Also save to session storage for quick access
    sessionStorage.setItem('user', JSON.stringify(user));
  }

  async getUser(): Promise<User | null> {
    const user = await this._storage?.get('user');
    if (user) {
      this.userSubject.next(user);
    }
    return user;
  }

  async updateUser(updates: Partial<User>): Promise<void> {
    const currentUser = await this.getUser();
    if (currentUser) {
      const updatedUser = { ...currentUser, ...updates, updatedAt: new Date() };
      await this.setUser(updatedUser);
    }
  }

  async clearUser(): Promise<void> {
    await this._storage?.remove('user');
    sessionStorage.removeItem('user');
    this.userSubject.next(null);
  }

  // User preferences management
  async setPreferences(preferences: UserPreferences): Promise<void> {
    await this._storage?.set('preferences', preferences);
    this.preferencesSubject.next(preferences);
    sessionStorage.setItem('preferences', JSON.stringify(preferences));
  }

  async getPreferences(): Promise<UserPreferences | null> {
    const preferences = await this._storage?.get('preferences');
    if (preferences) {
      this.preferencesSubject.next(preferences);
    }
    return preferences;
  }

  async updatePreferences(updates: Partial<UserPreferences>): Promise<void> {
    const currentPreferences = await this.getPreferences();
    if (currentPreferences) {
      const updatedPreferences = { ...currentPreferences, ...updates };
      await this.setPreferences(updatedPreferences);
    }
  }

  // Favorites management
  async getFavorites(): Promise<string[]> {
    return await this._storage?.get('favorites') || [];
  }

  async addFavorite(productId: string): Promise<void> {
    const favorites = await this.getFavorites();
    if (!favorites.includes(productId)) {
      favorites.push(productId);
      await this._storage?.set('favorites', favorites);
      sessionStorage.setItem('favorites', JSON.stringify(favorites));
    }
  }

  async removeFavorite(productId: string): Promise<void> {
    const favorites = await this.getFavorites();
    const updatedFavorites = favorites.filter(id => id !== productId);
    await this._storage?.set('favorites', updatedFavorites);
    sessionStorage.setItem('favorites', JSON.stringify(updatedFavorites));
  }

  async isFavorite(productId: string): Promise<boolean> {
    const favorites = await this.getFavorites();
    return favorites.includes(productId);
  }

  // Recent searches management
  async getRecentSearches(): Promise<string[]> {
    return await this._storage?.get('recentSearches') || [];
  }

  async addRecentSearch(query: string): Promise<void> {
    const searches = await this.getRecentSearches();
    const updatedSearches = [query, ...searches.filter(s => s !== query)].slice(0, 10);
    await this._storage?.set('recentSearches', updatedSearches);
    sessionStorage.setItem('recentSearches', JSON.stringify(updatedSearches));
  }

  async clearRecentSearches(): Promise<void> {
    await this._storage?.remove('recentSearches');
    sessionStorage.removeItem('recentSearches');
  }

  // Scan history management
  async getScanHistory(): Promise<any[]> {
    return await this._storage?.get('scanHistory') || [];
  }

  async addScanHistory(scan: any): Promise<void> {
    const history = await this.getScanHistory();
    const updatedHistory = [scan, ...history].slice(0, 50); // Keep last 50 scans
    await this._storage?.set('scanHistory', updatedHistory);
    sessionStorage.setItem('scanHistory', JSON.stringify(updatedHistory));
  }

  async clearScanHistory(): Promise<void> {
    await this._storage?.remove('scanHistory');
    sessionStorage.removeItem('scanHistory');
  }

  // Receipts management
  async getReceipts(): Promise<any[]> {
    return await this._storage?.get('receipts') || [];
  }

  async saveReceipts(receipts: any[]): Promise<void> {
    await this._storage?.set('receipts', receipts);
    sessionStorage.setItem('receipts', JSON.stringify(receipts));
  }

  async addReceipt(receipt: any): Promise<void> {
    const receipts = await this.getReceipts();
    receipts.unshift(receipt);
    await this.saveReceipts(receipts);
  }

  async updateReceipt(receiptId: string, updates: any): Promise<void> {
    const receipts = await this.getReceipts();
    const index = receipts.findIndex(r => r.id === receiptId);
    if (index !== -1) {
      receipts[index] = { ...receipts[index], ...updates, updatedAt: new Date() };
      await this.saveReceipts(receipts);
    }
  }

  async deleteReceipt(receiptId: string): Promise<void> {
    const receipts = await this.getReceipts();
    const updatedReceipts = receipts.filter(r => r.id !== receiptId);
    await this.saveReceipts(updatedReceipts);
  }

  // Settings management
  async getSettings(): Promise<any> {
    return await this._storage?.get('settings') || {};
  }

  async setSettings(settings: any): Promise<void> {
    await this._storage?.set('settings', settings);
    sessionStorage.setItem('settings', JSON.stringify(settings));
  }

  async updateSettings(updates: any): Promise<void> {
    const currentSettings = await this.getSettings();
    const updatedSettings = { ...currentSettings, ...updates };
    await this.setSettings(updatedSettings);
  }

  // Dark mode management
  async getDarkMode(): Promise<boolean> {
    return await this._storage?.get('darkMode') || false;
  }

  async setDarkMode(enabled: boolean): Promise<void> {
    await this._storage?.set('darkMode', enabled);
    sessionStorage.setItem('darkMode', enabled.toString());
  }

  // Location data management
  async getLastLocation(): Promise<{ latitude: number; longitude: number } | null> {
    return await this._storage?.get('lastLocation') || null;
  }

  async setLastLocation(latitude: number, longitude: number): Promise<void> {
    const location = { latitude, longitude, timestamp: new Date() };
    await this._storage?.set('lastLocation', location);
    sessionStorage.setItem('lastLocation', JSON.stringify(location));
  }

  // Cache management
  async getCachedData(key: string): Promise<any> {
    const cached = await this._storage?.get(`cache_${key}`);
    if (cached && cached.expiry > Date.now()) {
      return cached.data;
    }
    return null;
  }

  async setCachedData(key: string, data: any, expiryMinutes: number = 60): Promise<void> {
    const cacheEntry = {
      data,
      expiry: Date.now() + (expiryMinutes * 60 * 1000)
    };
    await this._storage?.set(`cache_${key}`, cacheEntry);
  }

  async clearCache(): Promise<void> {
    const keys = await this._storage?.keys();
    if (keys) {
      const cacheKeys = keys.filter(key => key.startsWith('cache_'));
      for (const key of cacheKeys) {
        await this._storage?.remove(key);
      }
    }
  }

  // Data export/import
  async exportData(): Promise<LocalStorageData> {
    const data: LocalStorageData = {
      user: await this.getUser() || {} as User,
      favorites: await this.getFavorites(),
      recentSearches: await this.getRecentSearches(),
      scanHistory: await this.getScanHistory(),
      receipts: await this.getReceipts(),
      settings: await this.getSettings()
    };
    return data;
  }

  async importData(data: LocalStorageData): Promise<void> {
    if (data.user) await this.setUser(data.user);
    if (data.favorites) await this._storage?.set('favorites', data.favorites);
    if (data.recentSearches) await this._storage?.set('recentSearches', data.recentSearches);
    if (data.scanHistory) await this._storage?.set('scanHistory', data.scanHistory);
    if (data.receipts) await this.saveReceipts(data.receipts);
    if (data.settings) await this.setSettings(data.settings);
  }

  // Clear all data
  async clearAllData(): Promise<void> {
    await this._storage?.clear();
    sessionStorage.clear();
    this.userSubject.next(null);
    this.preferencesSubject.next(null);
  }

  // Load user data on initialization
  private async loadUserData(): Promise<void> {
    try {
      const user = await this.getUser();
      if (user) {
        this.userSubject.next(user);
      }

      const preferences = await this.getPreferences();
      if (preferences) {
        this.preferencesSubject.next(preferences);
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  }

  // Get current user from subject
  getCurrentUser(): User | null {
    return this.userSubject.value;
  }

  // Get current preferences from subject
  getCurrentPreferences(): UserPreferences | null {
    return this.preferencesSubject.value;
  }

  // Check if storage is ready
  isStorageReady(): boolean {
    return this._storage !== null;
  }
}
