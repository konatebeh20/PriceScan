import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ExportOptions {
  format: 'excel' | 'csv' | 'json' | 'txt';
  dateRange: 'all' | 'last7days' | 'last30days' | 'last3months' | 'custom';
  startDate?: string;
  endDate?: string;
  includeReceipts: boolean;
  includeProducts: boolean;
  includeStores: boolean;
  includeAnalytics: boolean;
  dataQuality: 'basic' | 'detailed' | 'full';
}

@Component({
  selector: 'app-export-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './export-modal.html',
  styleUrls: ['./export-modal.scss']
})
export class ExportModalComponent {
  @Input() isOpen = false;
  @Output() closeModal = new EventEmitter<void>();
  @Output() exportData = new EventEmitter<ExportOptions>();

  exportOptions: ExportOptions = {
    format: 'excel',
    dateRange: 'all',
    includeReceipts: true,
    includeProducts: true,
    includeStores: true,
    includeAnalytics: true,
    dataQuality: 'detailed'
  };

  formats = [
    { value: 'excel', label: 'Excel (.xlsx)', icon: 'fas fa-file-excel', description: 'Format Excel avec graphiques et formules' },
    { value: 'csv', label: 'CSV (.csv)', icon: 'fas fa-file-csv', description: 'Format CSV pour analyse de données' },
    { value: 'json', label: 'JSON (.json)', icon: 'fas fa-file-code', description: 'Format JSON pour développement et API' },
    { value: 'txt', label: 'Texte (.txt)', icon: 'fas fa-file-alt', description: 'Format texte simple pour compatibilité' }
  ];

  dateRanges = [
    { value: 'all', label: 'Toutes les données' },
    { value: 'last7days', label: '7 derniers jours' },
    { value: 'last30days', label: '30 derniers jours' },
    { value: 'last3months', label: '3 derniers mois' },
    { value: 'custom', label: 'Période personnalisée' }
  ];

  dataQualityOptions = [
    { value: 'basic', label: 'Basique', description: 'Données essentielles uniquement' },
    { value: 'detailed', label: 'Détaillé', description: 'Données complètes avec métadonnées' },
    { value: 'full', label: 'Complet', description: 'Toutes les données + analyses avancées' }
  ];

  showCustomDateInputs = false;

  onDateRangeChange() {
    this.showCustomDateInputs = this.exportOptions.dateRange === 'custom';
  }

  onExport() {
    // Validation des dates personnalisées
    if (this.exportOptions.dateRange === 'custom') {
      if (!this.exportOptions.startDate || !this.exportOptions.endDate) {
        alert('Veuillez sélectionner une période personnalisée');
        return;
      }
      
      const startDate = new Date(this.exportOptions.startDate);
      const endDate = new Date(this.exportOptions.endDate);
      
      if (startDate > endDate) {
        alert('La date de début doit être antérieure à la date de fin');
        return;
      }
    }

    // Émettre les options d'export
    this.exportData.emit(this.exportOptions);
    
    // Simuler l'export
    this.simulateExport();
  }

  private simulateExport() {
    const format = this.exportOptions.format;
    const fileName = `ticketscan_export_${new Date().toISOString().split('T')[0]}.${this.getFileExtension(format)}`;
    
    // Simulation de téléchargement
    console.log(`Export en cours... Format: ${format}, Fichier: ${fileName}`);
    
    // Ici, tu pourrais implémenter la vraie logique d'export
    // Pour l'instant, on simule avec un délai
    setTimeout(() => {
      alert(`Export terminé ! Fichier: ${fileName}\n\nLes données sont optimisées pour:\n- Analyse de données (EDA)\n- Data Science\n- Machine Learning`);
      this.closeModal.emit();
    }, 2000);
  }

  private getFileExtension(format: string): string {
    const extensions: { [key: string]: string } = {
      'excel': 'xlsx',
      'csv': 'csv',
      'json': 'json',
      'txt': 'txt'
    };
    return extensions[format] || 'txt';
  }

  close() {
    this.closeModal.emit();
  }

  setFormat(format: string) {
    this.exportOptions.format = format as 'excel' | 'csv' | 'json' | 'txt';
  }

  setDataQuality(quality: string) {
    this.exportOptions.dataQuality = quality as 'basic' | 'detailed' | 'full';
  }

  // Méthodes pour la qualité des données
  getDataQualityDescription(quality: string): string {
    const descriptions: { [key: string]: string } = {
      'basic': 'Données essentielles pour analyses simples',
      'detailed': 'Données complètes avec métadonnées et relations',
      'full': 'Toutes les données + analyses avancées et prédictives'
    };
    return descriptions[quality] || '';
  }

  getFormatDescription(format: string): string {
    const formatInfo = this.formats.find(f => f.value === format);
    return formatInfo ? formatInfo.description : '';
  }
}
