import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExportModalComponent } from '../export-modal/export-modal';
import { ChartsComponent } from '../charts/charts';
import { DashboardDataService, DashboardStats } from '../../services/dashboard-data/dashboard-data';

@Component({
  selector: 'app-quick-actions',
  standalone: true,
  imports: [CommonModule, ExportModalComponent, ChartsComponent],
  templateUrl: './quick-actions.html',
  styleUrls: ['./quick-actions.scss']
})
export class QuickActionsComponent {
  @Output() pageChange = new EventEmitter<'dashboard' | 'receipts' | 'products' | 'stores' | 'settings'>();

  showExportModal = false;
  showCharts = false;

  constructor(private dashboardDataService: DashboardDataService) {}

  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings') {
    // Si c'est "receipts", rediriger vers "Saisie Manuelle"
    if (pageName === 'receipts') {
      // Ici tu pourrais émettre un événement spécifique pour "Saisie Manuelle"
      console.log('Redirection vers Saisie Manuelle...');
    }
    this.pageChange.emit(pageName);
  }

  addTestReceipt() {
    // Créer un reçu de test pour vérifier la cohérence des données
    const testReceipt = {
      store: 'Monoprix Test',
      address: 'Avenue Test, Abidjan - Tél: +225 27 22 33 44',
      date: new Date().toLocaleDateString('en-US', { 
        month: 'short', 
        day: '2-digit', 
        year: 'numeric' 
      }),
      time: new Date().toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      }),
      ticketNumber: `TK${Date.now()}`,
      status: 'analyzed',
      items: [
        { name: 'Pommes Golden 1kg', qty: 2, price: 2500 },
        { name: 'Pain complet 500g', qty: 1, price: 1200 },
        { name: 'Jus d\'ananas 1L', qty: 1, price: 1800 }
      ],
      total: '7 000 F CFA',
      type: 'manual'
    };

    // Utiliser le service pour ajouter le reçu
    this.dashboardDataService.getStats().subscribe(
      (stats: DashboardStats) => {
        console.log('Reçu de test ajouté:', testReceipt);
        console.log('Statistiques actuelles:', stats);
        alert('Reçu de test ajouté ! Vérifiez la cohérence des données dans l\'aperçu rapide.');
      },
      (error) => {
        console.error('Erreur lors de la récupération des stats:', error);
        alert('Erreur lors de la récupération des statistiques');
      }
    );
  }

  openExportModal() {
    this.showExportModal = true;
  }

  closeExportModal() {
    this.showExportModal = false;
  }

  onExportData(exportOptions: any) {
    console.log('Export options:', exportOptions);
    // Ici tu pourrais implémenter la vraie logique d'export
    this.closeExportModal();
  }

  toggleCharts() {
    this.showCharts = !this.showCharts;
  }
}
