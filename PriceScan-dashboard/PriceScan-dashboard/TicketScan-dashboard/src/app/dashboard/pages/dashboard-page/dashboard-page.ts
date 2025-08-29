import { Component, Output, EventEmitter, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { QuickActionsComponent } from '../../includes/quick-actions/quick-actions';
import { ChartsComponent } from '../../includes/charts/charts';
import { DashboardDataService, DashboardStats, DashboardReceipt } from '../../services/dashboard-data/dashboard-data';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, QuickActionsComponent, ChartsComponent],
  templateUrl: './dashboard-page.html',
  styleUrls: ['./dashboard-page.scss']
})
export class DashboardPageComponent implements OnInit, OnDestroy {
  @Output() pageChange = new EventEmitter<'dashboard' | 'receipts' | 'products' | 'stores' | 'settings'>();

  currentDateTime: string = '';
  private timeInterval: any;
  private statsSubscription: Subscription | null = null;

  // Données dynamiques pour l'aperçu rapide
  totalReceipts: number = 0;
  totalSpent: number = 0;
  thisMonthSpent: number = 0;
  averageReceipt: number = 0;

  // Données d'activité récente
  recentReceipts: any[] = [];

  constructor(private dashboardDataService: DashboardDataService) {
    console.log('✅ DashboardPageComponent constructor appelé');
  }

  ngOnInit() {
    console.log('✅ DashboardPageComponent ngOnInit appelé');
    
    // Ne plus initialiser avec des valeurs statiques
    // Les données viendront directement du service
    
    this.updateDateTime();
    this.loadDashboardData();
    
    // Mettre à jour toutes les secondes
    this.timeInterval = setInterval(() => {
      this.updateDateTime();
    }, 1000);
  }

  ngOnDestroy() {
    console.log('✅ DashboardPageComponent ngOnDestroy appelé');
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
    if (this.statsSubscription) {
      this.statsSubscription.unsubscribe();
    }
  }

  private updateDateTime() {
    const now = new Date();
    const options: Intl.DateTimeFormatOptions = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    };
    
    this.currentDateTime = now.toLocaleDateString('fr-FR', options);
  }

  private loadDashboardData() {
    console.log('✅ Chargement des données du dashboard...');
    // S'abonner aux statistiques du service
    this.statsSubscription = this.dashboardDataService.getStats().subscribe(
      (stats: DashboardStats) => {
        console.log('✅ Statistiques reçues:', stats);
        // Utiliser les données du service
        this.totalReceipts = stats.totalReceipts;
        this.totalSpent = stats.totalSpent;
        this.thisMonthSpent = stats.thisMonthSpent;
        this.averageReceipt = stats.averageReceipt;
        
        // Charger les reçus récents
        this.loadRecentReceipts();
      },
      (error) => {
        console.error('❌ Erreur lors du chargement des statistiques:', error);
      }
    );
  }

  private loadRecentReceipts() {
    console.log('✅ Chargement des reçus récents...');
    this.dashboardDataService.getRecentReceipts().subscribe(
      (receipts: DashboardReceipt[]) => {
        console.log('✅ Reçus reçus:', receipts);
        this.recentReceipts = receipts.map(receipt => ({
          id: receipt.id,
          amount: this.parseCurrencyAmount(receipt.total),
          store: receipt.store,
          type: this.getStoreType(receipt.store),
          date: new Date(receipt.date),
          formattedDate: new Date(receipt.date).toLocaleDateString('fr-FR', { 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric' 
          })
        }));
        console.log('✅ Reçus formatés:', this.recentReceipts);
      },
      (error) => {
        console.error('❌ Erreur lors du chargement des reçus:', error);
      }
    );
  }

  private parseCurrencyAmount(amountStr: string): number {
    // Convertir "18 450 F CFA" en 18450
    if (!amountStr) return 0;
    
    const numericPart = amountStr.replace(/[^\d]/g, '');
    return parseInt(numericPart) || 0;
  }

  private getStoreType(storeName: string): string {
    // Déterminer le type de magasin basé sur le nom
    const lowerName = storeName.toLowerCase();
    
    if (lowerName.includes('pharmacie') || lowerName.includes('pharma')) {
      return 'Médicaments';
    } else if (lowerName.includes('brico') || lowerName.includes('quincaillerie')) {
      return 'Bricolage';
    } else if (lowerName.includes('carrefour') || lowerName.includes('prosuma') || lowerName.includes('casino')) {
      return 'Alimentation';
    } else {
      return 'Autres';
    }
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'XOF'
    }).format(amount);
  }

  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings') {
    console.log('✅ Navigation vers:', pageName);
    this.pageChange.emit(pageName);
  }

  // Méthode pour rafraîchir manuellement les données
  refreshData() {
    this.loadDashboardData();
  }
}
