import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, BehaviorSubject, timer } from 'rxjs';
import { catchError, retry, switchMap, tap, delay } from 'rxjs/operators';
import { API_CONFIG } from '../api/api.config';

export interface SyncStatus {
  isSyncing: boolean;
  lastSync: Date | null;
  syncErrors: string[];
  isOnline: boolean;
}

export interface SyncData {
  userProfile: any;
  dashboardStats: any;
  promotions: any[];
  recentReceipts: any[];
  scanHistory: any[];
}

@Injectable({
  providedIn: 'root'
})
export class DataSyncService {
  private syncStatus = new BehaviorSubject<SyncStatus>({
    isSyncing: false,
    lastSync: null,
    syncErrors: [],
    isOnline: navigator.onLine
  });

  private syncInterval: any;
  private readonly SYNC_INTERVAL = 30000; // 30 secondes

  constructor(private http: HttpClient) {
    this.initializeSync();
    this.setupOnlineOfflineDetection();
  }

  // Initialiser la synchronisation automatique
  private initializeSync() {
    // Démarrer la synchronisation automatique
    this.startAutoSync();
    
    // Synchroniser immédiatement au démarrage
    this.syncAllData();
  }

  // Démarrer la synchronisation automatique
  private startAutoSync() {
    this.syncInterval = setInterval(() => {
      if (navigator.onLine && !this.syncStatus.value.isSyncing) {
        this.syncAllData();
      }
    }, this.SYNC_INTERVAL);
  }

  // Détecter les changements de connectivité
  private setupOnlineOfflineDetection() {
    window.addEventListener('online', () => {
      this.updateOnlineStatus(true);
      this.syncAllData(); // Synchroniser quand on revient en ligne
    });

    window.addEventListener('offline', () => {
      this.updateOnlineStatus(false);
    });
  }

  // Mettre à jour le statut de connectivité
  private updateOnlineStatus(isOnline: boolean) {
    const currentStatus = this.syncStatus.value;
    this.syncStatus.next({
      ...currentStatus,
      isOnline
    });
  }

  // Synchroniser toutes les données
  syncAllData(): Observable<SyncData> {
    if (this.syncStatus.value.isSyncing) {
      return of(null as any);
    }

    this.updateSyncStatus(true, null, []);

    return this.http.get<SyncData>(`${API_CONFIG.BASE_URL}/dashboard/sync`).pipe(
      retry(3),
      tap(data => {
        this.saveToSessionStorage(data);
        this.updateSyncStatus(false, new Date(), []);
        console.log('✅ Synchronisation complète réussie');
      }),
      catchError(error => {
        console.error('❌ Erreur de synchronisation:', error);
        this.updateSyncStatus(false, null, [error.message]);
        return of(this.getDataFromSessionStorage());
      })
    );
  }

  // Synchroniser le profil utilisateur
  syncUserProfile(): Observable<any> {
    return this.http.get(`${API_CONFIG.USERS.PROFILE}`).pipe(
      retry(2),
      tap(profile => {
        sessionStorage.setItem('ticketscan_user_profile', JSON.stringify(profile));
        console.log('✅ Profil utilisateur synchronisé');
      }),
      catchError(error => {
        console.error('❌ Erreur synchronisation profil:', error);
        return of(this.getUserProfileFromStorage());
      })
    );
  }

  // Synchroniser les statistiques du dashboard
  syncDashboardStats(): Observable<any> {
    return this.http.get(`${API_CONFIG.DASHBOARD.STATS}`).pipe(
      retry(2),
      tap(stats => {
        sessionStorage.setItem('ticketscan_dashboard_stats', JSON.stringify(stats));
        console.log('✅ Statistiques dashboard synchronisées');
      }),
      catchError(error => {
        console.error('❌ Erreur synchronisation stats:', error);
        return of(this.getDashboardStatsFromStorage());
      })
    );
  }

  // Synchroniser les promotions
  syncPromotions(): Observable<any[]> {
    return this.http.get<any[]>(`${API_CONFIG.PROMOTIONS.ACTIVE}`).pipe(
      retry(2),
      tap(promotions => {
        sessionStorage.setItem('ticketscan_promotions', JSON.stringify(promotions));
        console.log('✅ Promotions synchronisées');
      }),
      catchError(error => {
        console.error('❌ Erreur synchronisation promotions:', error);
        return of(this.getPromotionsFromStorage());
      })
    );
  }

  // Synchroniser l'historique des scans
  syncScanHistory(): Observable<any[]> {
    return this.http.get<any[]>(`${API_CONFIG.RECEIPTS.SCAN_HISTORY}`).pipe(
      retry(2),
      tap(history => {
        sessionStorage.setItem('ticketscan_scan_history', JSON.stringify(history));
        console.log('✅ Historique des scans synchronisé');
      }),
      catchError(error => {
        console.error('❌ Erreur synchronisation historique:', error);
        return of(this.getScanHistoryFromStorage());
      })
    );
  }

  // Sauvegarder les données dans le session storage
  private saveToSessionStorage(data: SyncData) {
    if (data.userProfile) {
      sessionStorage.setItem('ticketscan_user_profile', JSON.stringify(data.userProfile));
    }
    if (data.dashboardStats) {
      sessionStorage.setItem('ticketscan_dashboard_stats', JSON.stringify(data.dashboardStats));
    }
    if (data.promotions) {
      sessionStorage.setItem('ticketscan_promotions', JSON.stringify(data.promotions));
    }
    if (data.recentReceipts) {
      sessionStorage.setItem('ticketscan_recent_receipts', JSON.stringify(data.recentReceipts));
    }
    if (data.scanHistory) {
      sessionStorage.setItem('ticketscan_scan_history', JSON.stringify(data.scanHistory));
    }
  }

  // Récupérer les données depuis le session storage
  private getDataFromSessionStorage(): SyncData {
    return {
      userProfile: this.getUserProfileFromStorage(),
      dashboardStats: this.getDashboardStatsFromStorage(),
      promotions: this.getPromotionsFromStorage(),
      recentReceipts: this.getRecentReceiptsFromStorage(),
      scanHistory: this.getScanHistoryFromStorage()
    };
  }

  // Méthodes de récupération depuis le storage
  private getUserProfileFromStorage(): any {
    const profile = sessionStorage.getItem('ticketscan_user_profile');
    return profile ? JSON.parse(profile) : null;
  }

  private getDashboardStatsFromStorage(): any {
    const stats = sessionStorage.getItem('ticketscan_dashboard_stats');
    return stats ? JSON.parse(stats) : null;
  }

  private getPromotionsFromStorage(): any[] {
    const promotions = sessionStorage.getItem('ticketscan_promotions');
    return promotions ? JSON.parse(promotions) : [];
  }

  private getRecentReceiptsFromStorage(): any[] {
    const receipts = sessionStorage.getItem('ticketscan_recent_receipts');
    return receipts ? JSON.parse(receipts) : [];
  }

  private getScanHistoryFromStorage(): any[] {
    const history = sessionStorage.getItem('ticketscan_scan_history');
    return history ? JSON.parse(history) : [];
  }

  // Mettre à jour le statut de synchronisation
  private updateSyncStatus(isSyncing: boolean, lastSync: Date | null, errors: string[]) {
    this.syncStatus.next({
      ...this.syncStatus.value,
      isSyncing,
      lastSync,
      syncErrors: errors
    });
  }

  // Obtenir le statut de synchronisation
  getSyncStatus(): Observable<SyncStatus> {
    return this.syncStatus.asObservable();
  }

  // Forcer une synchronisation manuelle
  forceSync(): Observable<SyncData> {
    console.log('🔄 Synchronisation manuelle déclenchée');
    return this.syncAllData();
  }

  // Arrêter la synchronisation automatique
  stopAutoSync() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }

  // Nettoyer les ressources
  ngOnDestroy() {
    this.stopAutoSync();
  }
}
