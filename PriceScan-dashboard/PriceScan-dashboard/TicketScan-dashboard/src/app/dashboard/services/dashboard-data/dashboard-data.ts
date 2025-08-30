import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, catchError, tap, map, retry, forkJoin } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { ErrorHandlerService } from '../error-handler/error-handler.service';
import { DataSyncService } from '../sync/sync.service';
import { ProductsService } from '../products/products.service';
import { StoresService, Store } from '../stores/stores.service';

// Interfaces pour la compatibilité avec les composants existants
export interface DashboardReceiptItem {
  name: string;
  qty: number;
  price: number;
}

export interface DashboardReceipt {
  id: number;
  store: string;
  address: string;
  date: string;
  time: string;
  ticketNumber: string;
  status: 'analyzed' | 'processing' | 'failed';
  items: DashboardReceiptItem[];
  total: string;
  type: 'scanned' | 'manual' | 'archived';
  isFavorite?: boolean;
}

export interface DashboardStats {
  totalReceipts: number;
  totalSpent: number;
  thisMonthSpent: number;
  averageReceipt: number;
  recentReceipts: DashboardReceipt[];
  totalSavings?: number;
  savingsFromPromos?: number;
  savingsFromComparison?: number;
  topCategories?: any[];
  topStores?: any[];
  // Nouvelles statistiques pour les produits et magasins
  totalProducts: number;
  activeProducts: number;
  archivedProducts: number;
  favoriteProducts: number;
  totalStores: number;
  activeStores: number;
  archivedStores: number;
  favoriteStores: number;
}

export interface DashboardUserProfile {
  user_uid: string;
  preferred_currency: string;
  preferred_language: string;
  gender: string;
  notification_preferences?: any;
}

@Injectable({
  providedIn: 'root'
})
export class DashboardDataService {
  private apiUrl = API_CONFIG.DASHBOARD.STATS;

  constructor(
    private http: HttpClient,
    private errorHandler: ErrorHandlerService,
    private syncService: DataSyncService,
    private productsService: ProductsService,
    private storesService: StoresService
  ) {
    console.log('DashboardDataService initialisé avec API:', this.apiUrl);
  }

  // Méthode principale pour les statistiques - utilise l'API PriceScan
  getStats(): Observable<DashboardStats> {
    console.log('DashboardDataService: getStats appelé');
    
    return this.http.get<any>(this.apiUrl).pipe(
      retry(2),
      tap(data => console.log('Données reçues du backend PriceScan:', data)),
      map(backendData => this.transformBackendData(backendData)),
      catchError((error) => {
        console.error('Erreur lors de la récupération des stats:', error);
        console.log('Utilisation des données du session storage');
        // Retourner les données du session storage en cas d'erreur
        return of(this.getStatsFromStorage());
      })
    );
  }

  // Méthode pour obtenir les statistiques complètes incluant produits et magasins
  getCompleteStats(): Observable<DashboardStats> {
    console.log('DashboardDataService: getCompleteStats appelé');
    
    return forkJoin({
      backendStats: this.http.get<any>(this.apiUrl).pipe(
        catchError(() => of(null))
      ),
      products: this.productsService.getProducts().pipe(
        catchError(() => of([]))
      ),
      stores: this.storesService.getStores().pipe(
        catchError(() => of([]))
      ),
      receipts: this.http.get<any[]>(`${API_CONFIG.BASE_URL}/receipts`).pipe(
        catchError(() => of([]))
      )
    }).pipe(
      map(({ backendStats, products, stores, receipts }) => {
        const baseStats = backendStats ? this.transformBackendData(backendStats) : this.getStatsFromStorage();
        
        // Calculer les statistiques des produits
        const totalProducts = products.length;
        const activeProducts = products.filter(p => p.product_is_active).length;
        const archivedProducts = products.filter(p => !p.product_is_active).length;
        const favoriteProducts = products.filter(p => p.isFavorite).length;
        
        // Calculer les statistiques des magasins
        const totalStores = stores.length;
        const activeStores = stores.filter(s => s.status !== 'archived').length;
        const archivedStores = stores.filter(s => s.status === 'archived').length;
        const favoriteStores = stores.filter(s => s.isFavorite === true).length;
        
        // Calculer les statistiques des reçus depuis la vraie base de données
        const receiptStats = this.calculateStatsFromRealReceipts(receipts);
        
        return {
          ...baseStats,
          totalReceipts: receiptStats.totalReceipts,
          totalSpent: receiptStats.totalSpent,
          thisMonthSpent: receiptStats.thisMonthSpent,
          averageReceipt: receiptStats.averageReceipt,
          totalProducts,
          activeProducts,
          archivedProducts,
          favoriteProducts,
          totalStores,
          activeStores,
          archivedStores,
          favoriteStores
        };
      }),
      catchError((error) => {
        console.error('Erreur lors de la récupération des stats complètes:', error);
        return of(this.getStatsFromStorage());
      })
    );
  }

  // Méthode pour les reçus récents - utilise l'API PriceScan
  getRecentReceipts(): Observable<DashboardReceipt[]> {
    console.log('DashboardDataService: getRecentReceipts appelé');
    
    return this.http.get<any[]>(`${API_CONFIG.DASHBOARD.RECENT_RECEIPTS}`).pipe(
      retry(2),
      tap(data => console.log('Reçus reçus du backend PriceScan:', data)),
      map(backendReceipts => this.transformBackendReceipts(backendReceipts)),
      catchError((error) => {
        console.error('Erreur lors de la récupération des reçus:', error);
        console.log('Utilisation des reçus du session storage');
        // Retourner les reçus du session storage en cas d'erreur
        return of(this.getReceiptsFromStorage());
      })
    );
  }

  // Méthodes pour la compatibilité avec l'ancien service
  getAllReceipts(): Observable<DashboardReceipt[]> {
    return this.getRecentReceipts();
  }

  getReceiptById(id: number): Observable<DashboardReceipt | undefined> {
    return this.getRecentReceipts().pipe(
      map(receipts => receipts.find(r => r.id === id))
    );
  }

  // Méthode pour récupérer les reçus depuis l'API backend
  getReceiptsFromAPI(): Observable<any[]> {
    return this.http.get<any[]>(`${API_CONFIG.BASE_URL}/receipts`).pipe(
      tap(receipts => console.log('Reçus récupérés depuis l\'API:', receipts.length)),
      catchError(error => {
        console.error('Erreur lors de la récupération des reçus:', error);
        return of([]);
      })
    );
  }

  // Méthode pour calculer les statistiques depuis les reçus réels
  private calculateStatsFromRealReceipts(receipts: any[]): {
    totalReceipts: number;
    totalSpent: number;
    thisMonthSpent: number;
    averageReceipt: number;
  } {
    const totalReceipts = receipts.length;
    
    if (totalReceipts === 0) {
      return {
        totalReceipts: 0,
        totalSpent: 0,
        thisMonthSpent: 0,
        averageReceipt: 0
      };
    }

    const totalSpent = receipts.reduce((sum, receipt) => {
      const amount = this.parseReceiptAmount(receipt.receipt_total || receipt.total || '0');
      return sum + amount;
    }, 0);

    // Calculer les dépenses du mois en cours
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    const thisMonthSpent = receipts
      .filter(receipt => {
        const receiptDate = new Date(receipt.receipt_date || receipt.date || new Date());
        return receiptDate.getMonth() === currentMonth && receiptDate.getFullYear() === currentYear;
      })
      .reduce((sum, receipt) => {
        const amount = this.parseReceiptAmount(receipt.receipt_total || receipt.total || '0');
        return sum + amount;
      }, 0);

    const averageReceipt = totalSpent / totalReceipts;

    return {
      totalReceipts,
      totalSpent,
      thisMonthSpent,
      averageReceipt
    };
  }

  // Récupérer les données depuis le session storage
  private getStatsFromStorage(): DashboardStats {
    const storedStats = sessionStorage.getItem('ticketscan_dashboard_stats');
    if (storedStats) {
      const stats = JSON.parse(storedStats);
      return this.transformBackendData(stats);
    }
    
    // Retourner les statistiques calculées depuis les reçus
    return this.calculateStatsFromReceipts();
  }

  private getReceiptsFromStorage(): DashboardReceipt[] {
    const storedReceipts = sessionStorage.getItem('ticketscan_recent_receipts');
    if (storedReceipts) {
      return JSON.parse(storedReceipts);
    }
    
    // Retourner les reçus par défaut
    return this.getDefaultReceipts();
  }

  // Récupérer les vrais reçus scannés (basés sur receipts-list.ts)
  private getDefaultReceipts(): DashboardReceipt[] {
    return [
      {
        id: 1,
        store: 'Carrefour Market',
        address: 'Bamako, Mali - Tél: +223 20 22 33 44',
        date: '15 Nov 2024',
        time: '14:30',
        ticketNumber: 'TK001',
        status: 'analyzed',
        items: [
          { name: 'Pain de mie', qty: 2, price: 1500 },
          { name: 'Lait UHT 1L', qty: 3, price: 2250 },
          { name: 'Yaourt nature', qty: 4, price: 3200 },
          { name: 'Bananes 1kg', qty: 1, price: 1800 },
          { name: 'Riz parfumé 5kg', qty: 1, price: 9700 }
        ],
        total: '18 450 F CFA',
        type: 'scanned'
      },
      {
        id: 2,
        store: 'Prosuma',
        address: 'Bamako, Mali - Tél: +223 20 22 55 66',
        date: '12 Nov 2024',
        time: '16:45',
        ticketNumber: 'TK002',
        status: 'processing',
        items: [
          { name: 'Huile végétale 5L', qty: 2, price: 12000 },
          { name: 'Sucre blanc 2kg', qty: 3, price: 4500 },
          { name: 'Farine de blé 2kg', qty: 2, price: 3200 },
          { name: 'Tomates fraîches 2kg', qty: 1, price: 2800 },
          { name: 'Poulet entier', qty: 2, price: 10250 }
        ],
        total: '32 750 F CFA',
        type: 'scanned'
      }
    ];
  }

  // Calculer les statistiques depuis les reçus
  private calculateStatsFromReceipts(): DashboardStats {
    const receipts = this.getDefaultReceipts();
    
    const totalReceipts = receipts.length;
    const totalSpent = receipts.reduce((sum, receipt) => {
      const amount = this.parseCurrencyAmount(receipt.total);
      return sum + amount;
    }, 0);
    
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    const thisMonthSpent = receipts.reduce((sum, receipt) => {
      const receiptDate = this.parseReceiptDate(receipt.date);
      
      if (receiptDate && receiptDate.getMonth() === currentMonth && receiptDate.getFullYear() === currentYear) {
        const amount = this.parseCurrencyAmount(receipt.total);
        console.log(`Reçu du mois en cours: ${receipt.store} - ${receipt.total} (${receipt.date})`);
        return sum + amount;
      }
      return sum;
    }, 0);
    
    // Calculer le panier moyen
    const averageReceipt = totalReceipts > 0 ? Math.round(totalSpent / totalReceipts) : 0;
    
    console.log('Statistiques calculées depuis les reçus:', {
      totalReceipts,
      totalSpent,
      thisMonthSpent,
      averageReceipt,
      currentMonth: currentMonth + 1, // +1 car getMonth() retourne 0-11
      currentYear
    });
    
    return {
      totalReceipts,
      totalSpent,
      thisMonthSpent,
      averageReceipt,
      recentReceipts: receipts,
      totalSavings: 0,
      savingsFromPromos: 0,
      savingsFromComparison: 0,
      topCategories: [],
      topStores: [],
      // Nouvelles statistiques avec valeurs par défaut
      totalProducts: 0,
      activeProducts: 0,
      archivedProducts: 0,
      favoriteProducts: 0,
      totalStores: 0,
      activeStores: 0,
      archivedStores: 0,
      favoriteStores: 0
    };
  }

  // Parser la date du reçu (format: "15 Nov 2024")
  private parseReceiptDate(dateStr: string): Date | null {
    try {
      // Format attendu: "15 Nov 2024"
      const parts = dateStr.split(' ');
      if (parts.length === 3) {
        const day = parseInt(parts[0]);
        const monthStr = parts[1];
        const year = parseInt(parts[2]);
        
        // Mapping des mois
        const monthMap: { [key: string]: number } = {
          'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'Jun': 5,
          'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
        };
        
        const month = monthMap[monthStr];
        if (month !== undefined && !isNaN(day) && !isNaN(year)) {
          return new Date(year, month, day);
        }
      }
    } catch (error) {
      console.error('Erreur lors du parsing de la date:', dateStr, error);
    }
    
    return null;
  }

  private parseCurrencyAmount(amountStr: string): number {
    // Convertir "18 450 F CFA" en 18450
    if (!amountStr) return 0;
    
    const numericPart = amountStr.replace(/[^\d]/g, '');
    return parseInt(numericPart) || 0;
  }

  private parseReceiptAmount(amountStr: string): number {
    // Convertir "18 450 F CFA" en 18450
    if (!amountStr) return 0;
    
    const numericPart = amountStr.replace(/[^\d]/g, '');
    return parseInt(numericPart) || 0;
  }

  private transformBackendData(backendData: any): DashboardStats {
    // Transformer les données du backend vers le format attendu
    return {
      totalReceipts: backendData.total_receipts || 0,
      totalSpent: backendData.total_spent || 0,
      thisMonthSpent: backendData.this_month_spent || 0,
      averageReceipt: backendData.avg_receipt_amount || 0,
      recentReceipts: this.getReceiptsFromStorage(), // Utiliser les reçus du storage
      totalSavings: backendData.total_savings || 0,
      savingsFromPromos: backendData.savings_from_promos || 0,
      savingsFromComparison: backendData.savings_from_comparison || 0,
      topCategories: backendData.top_categories || [],
      topStores: backendData.top_stores || [],
      // Nouvelles statistiques avec valeurs par défaut
      totalProducts: backendData.total_products || 0,
      activeProducts: backendData.active_products || 0,
      archivedProducts: backendData.archived_products || 0,
      favoriteProducts: backendData.favorite_products || 0,
      totalStores: backendData.total_stores || 0,
      activeStores: backendData.active_stores || 0,
      archivedStores: backendData.archived_stores || 0,
      favoriteStores: backendData.favorite_stores || 0
    };
  }

  private transformBackendReceipts(backendReceipts: any[]): DashboardReceipt[] {
    // Transformer les reçus du backend vers le format attendu
    return backendReceipts.map(receipt => ({
      id: receipt.id || Math.random(),
      store: receipt.store || 'Magasin inconnu',
      address: receipt.address || 'Adresse non spécifiée',
      date: receipt.date || new Date().toLocaleDateString(),
      time: receipt.time || new Date().toLocaleTimeString(),
      ticketNumber: receipt.ticket_number || 'TK' + Math.random(),
      status: receipt.status || 'analyzed',
      items: receipt.items || [],
      total: receipt.total || '0 F CFA',
      type: receipt.type || 'scanned',
      isFavorite: receipt.is_favorite || false
    }));
  }

  // Méthodes pour les graphiques (si nécessaire)
  getChartData(period: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/chart-data?period=${period}`).pipe(
      retry(2),
      catchError(() => of(this.generateMockChartData(period)))
    );
  }

  private generateMockChartData(period: string): any {
    // Générer des données mockées pour les graphiques
    const now = new Date();
    const data = [];
    
    if (period === 'month') {
      for (let i = 0; i < 12; i++) {
        data.push({
          month: i + 1,
          amount: Math.floor(Math.random() * 50000) + 10000
        });
      }
    } else if (period === 'week') {
      for (let i = 0; i < 7; i++) {
        data.push({
          day: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'][i],
          amount: Math.floor(Math.random() * 10000) + 2000
        });
      }
    }
    
    return data;
  }

  // Synchroniser les données avec l'API PriceScan
  syncDashboardData(): Observable<any> {
    return this.syncService.syncDashboardStats();
  }

  // Obtenir le profil utilisateur
  getUserProfile(): Observable<DashboardUserProfile | null> {
    return this.http.get<DashboardUserProfile>(`${API_CONFIG.DASHBOARD.PROFILE}`).pipe(
      retry(2),
      tap(profile => {
        if (profile) {
          sessionStorage.setItem('ticketscan_user_profile', JSON.stringify(profile));
        }
      }),
      catchError(error => {
        console.error('Erreur récupération profil:', error);
        const storedProfile = sessionStorage.getItem('ticketscan_user_profile');
        return of(storedProfile ? JSON.parse(storedProfile) : null);
      })
    );
  }

  // Obtenir l'activité récente
  getRecentActivity(): Observable<any[]> {
    return this.http.get<any[]>(`${API_CONFIG.DASHBOARD.ACTIVITY}`).pipe(
      retry(2),
      tap(activity => {
        if (activity) {
          sessionStorage.setItem('ticketscan_recent_activity', JSON.stringify(activity));
        }
      }),
      catchError(error => {
        console.error('Erreur récupération activité:', error);
        const storedActivity = sessionStorage.getItem('ticketscan_recent_activity');
        return of(storedActivity ? JSON.parse(storedActivity) : []);
      })
    );
  }
}
