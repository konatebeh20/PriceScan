import { Component, OnInit, OnDestroy, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Chart, ChartConfiguration, ChartType, registerables } from 'chart.js';

// Enregistrer tous les composants Chart.js
Chart.register(...registerables);

@Component({
  selector: 'app-charts',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './charts.html',
  styleUrls: ['./charts.scss']
})
export class ChartsComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('priceChart', { static: false }) priceChartRef!: ElementRef<HTMLCanvasElement>;
  
  chartConfig = {
    type: 'line' as ChartType,
    period: '30days',
    comparisonMode: 'none' as 'none' | 'byStore' | 'byType',
    selectedStores: [] as number[],
    selectedTypes: [] as string[],
    showTrends: true,
    showPredictions: false
  };

  // Mode réel du graphique (pour distinguer les comportements)
  chartMode: 'line' | 'bar' | 'area' | 'mixed' = 'line';

  priceData: any[] = [];
  predictionData: any[] = [];
  comparisonData: any[] = [];
  tableData: any[] = [];
  isLoading = false;
  currentPage = 1;
  itemsPerPage = 10;
  totalItems = 0;
  showPredictionModal = false;

  // Types de graphiques avec valeurs Chart.js valides
  chartTypes = [
    { value: 'line', label: 'Ligne', icon: 'fas fa-chart-line' },
    { value: 'bar', label: 'Barres', icon: 'fas fa-chart-bar' },
    { value: 'line', label: 'Aires', icon: 'fas fa-chart-area' },
    { value: 'bar', label: 'Mixte', icon: 'fas fa-layer-group' }
  ];

  periods = [
    { value: '7days', label: '7 derniers jours' },
    { value: '30days', label: '30 derniers jours' },
    { value: '90days', label: '3 derniers mois' },
    { value: '1year', label: '1 an' }
  ];

  comparisonModes = [
    { value: 'none', label: 'Aucune', icon: null },
    { value: 'byStore', label: 'Par magasin', icon: 'fas fa-store' },
    { value: 'byType', label: 'Par type', icon: 'fas fa-chart-bar' }
  ];

  storeData = [
    { id: 1, name: 'Carrefour Centre', type: 'supermarché' },
    { id: 2, name: 'Pharmacie Centrale', type: 'pharmacie' },
    { id: 3, name: 'Bricorama', type: 'quincaillerie' },
    { id: 4, name: 'Monoprix', type: 'supermarché' }
  ];

  predictionConfig = {
    method: 'linear',
    targetVariable: 'price',
    predictionPeriod: '15days',
    confidenceLevel: 'high',
    includeSeasonality: false,
    includeExternalFactors: false
  };

  predictionMethods = [
    { value: 'linear', label: 'Régression linéaire' },
    { value: 'polynomial', label: 'Régression polynomiale' },
    { value: 'exponential', label: 'Régression exponentielle' },
    { value: 'movingAverage', label: 'Moyenne mobile' }
  ];

  targetVariables = [
    { value: 'price', label: 'Prix moyen' },
    { value: 'volume', label: 'Volume de ventes' },
    { value: 'trend', label: 'Tendance' }
  ];

  predictionPeriods = [
    { value: '7days', label: '7 jours' },
    { value: '15days', label: '15 jours' },
    { value: '30days', label: '30 jours' },
    { value: '90days', label: '3 mois' }
  ];

  confidenceLevels = [
    { value: 'low', label: 'Faible (70%)' },
    { value: 'medium', label: 'Moyen (85%)' },
    { value: 'high', label: 'Élevé (95%)' }
  ];

  private chart: Chart | null = null;
  Math = Math;

  ngOnInit() {
    this.generateData();
  }

  ngAfterViewInit() {
    // Attendre que le canvas soit disponible et que les données soient générées
    setTimeout(() => {
      if (this.priceData.length > 0) {
        this.loadChartData();
      } else {
        // Si pas encore de données, attendre un peu plus
        setTimeout(() => {
          this.loadChartData();
        }, 500);
      }
    }, 200);
  }

  ngOnDestroy() {
    if (this.chart) {
      this.chart.destroy();
    }
  }

  generateData() {
    this.isLoading = true;
    setTimeout(() => {
      const days = this.chartConfig.period === '7days' ? 7 : 
                  this.chartConfig.period === '30days' ? 30 :
                  this.chartConfig.period === '90days' ? 90 : 365;
      
      const data = [];
      const basePrice = 2500;
      
      for (let i = days; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        
        const variation = (Math.random() - 0.5) * 400;
        const trendFactor = Math.sin((days - i) / days * Math.PI) * 200;
        const price = Math.max(1500, basePrice + variation + trendFactor);
        
        data.push({
          date: date.toISOString().split('T')[0],
          dateFormatted: date.toLocaleDateString('fr-FR'),
          averagePrice: Math.round(price),
          minPrice: Math.round(price - Math.random() * 300),
          maxPrice: Math.round(price + Math.random() * 300),
          totalReceipts: Math.round(15 + Math.random() * 25),
          trend: Math.round(price + (Math.random() - 0.5) * 100),
          prediction: this.chartConfig.showPredictions ? Math.round(price + (Math.random() - 0.3) * 150) : null
        });
      }
      
      this.priceData = data;
      this.totalItems = data.length;
      this.updateTableData();
      
      if (this.chartConfig.showPredictions) {
        this.generatePredictionData();
      }
      
      this.isLoading = false;
      
      setTimeout(() => {
        this.loadChartData();
      }, 200);
    }, 800);
  }

  generatePredictionData() {
    const predictions = [];
    const lastPrice = this.priceData[this.priceData.length - 1].averagePrice;
    
    for (let i = 1; i <= 15; i++) {
      const futureDate = new Date();
      futureDate.setDate(futureDate.getDate() + i);
      
      predictions.push({
        date: futureDate.toISOString().split('T')[0],
        dateFormatted: futureDate.toLocaleDateString('fr-FR'),
        predictedPrice: Math.round(lastPrice + (Math.random() - 0.4) * 200),
        confidence: 0.95 - (i / 15) * 0.3
      });
    }
    this.predictionData = predictions;
  }

  onChartTypeChange(type: string) {
    // Déterminer le mode réel basé sur le label
    const selectedType = this.chartTypes.find(t => t.value === type);
    if (selectedType) {
      if (selectedType.label === 'Aires') {
        this.chartMode = 'area';
        this.chartConfig.type = 'line' as ChartType; // Chart.js utilise 'line' pour les aires
      } else if (selectedType.label === 'Mixte') {
        this.chartMode = 'mixed';
        this.chartConfig.type = 'bar' as ChartType; // Chart.js utilise 'bar' comme base
      } else {
        this.chartMode = type as 'line' | 'bar';
        this.chartConfig.type = type as ChartType;
      }
    }
    this.loadChartData();
  }

  onPeriodChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    this.chartConfig.period = target.value;
    this.generateData();
  }

  onComparisonModeChange(mode: string) {
    this.chartConfig.comparisonMode = mode as 'none' | 'byStore' | 'byType';
    this.loadChartData();
  }

  onStoreSelectionChange(storeId: number, checked: boolean) {
    if (checked) {
      this.chartConfig.selectedStores.push(storeId);
    } else {
      this.chartConfig.selectedStores = this.chartConfig.selectedStores.filter(id => id !== storeId);
    }
    this.loadChartData();
  }

  onTypeSelectionChange(type: string, checked: boolean) {
    if (checked) {
      this.chartConfig.selectedTypes.push(type);
    } else {
      this.chartConfig.selectedTypes = this.chartConfig.selectedTypes.filter(t => t !== type);
    }
    this.loadChartData();
  }

  toggleTrends() {
    this.chartConfig.showTrends = !this.chartConfig.showTrends;
    this.loadChartData();
  }

  togglePredictions() {
    this.chartConfig.showPredictions = !this.chartConfig.showPredictions;
    if (this.chartConfig.showPredictions) {
      this.generatePredictionData();
    }
    this.loadChartData();
  }

  getAveragePrice(): number {
    if (this.priceData.length === 0) return 0;
    return this.priceData.reduce((sum, item) => sum + item.averagePrice, 0) / this.priceData.length;
  }

  getTrendInfo() {
    if (this.priceData.length < 2) return { label: 'Stable', color: '#6B7280', icon: 'fas fa-minus' };
    
    const recent = this.priceData.slice(-7);
    const earlier = this.priceData.slice(-14, -7);
    
    if (earlier.length === 0) return { label: 'Stable', color: '#6B7280', icon: 'fas fa-minus' };
    
    const recentAvg = recent.reduce((sum, item) => sum + item.averagePrice, 0) / recent.length;
    const earlierAvg = earlier.reduce((sum, item) => sum + item.averagePrice, 0) / earlier.length;
    
    const change = ((recentAvg - earlierAvg) / earlierAvg) * 100;
    
    if (change > 2) {
      return { 
        label: `+${change.toFixed(1)}%`, 
        color: '#10B981', 
        icon: 'fas fa-trending-up' 
      };
    } else if (change < -2) {
      return { 
        label: `${change.toFixed(1)}%`, 
        color: '#EF4444', 
        icon: 'fas fa-trending-down' 
      };
    }
    return { 
      label: 'Stable', 
      color: '#6B7280', 
      icon: 'fas fa-minus' 
    };
  }

  getTrendIcon(): string {
    return this.getTrendInfo().icon;
  }

  getTrendColor(): string {
    return this.getTrendInfo().color;
  }

  getTrendLabel(): string {
    return this.getTrendInfo().label;
  }

  getPredictedPrice(): number {
    if (this.predictionData.length === 0) return 0;
    return this.predictionData[0].predictedPrice;
  }

  getCurrentPeriodLabel(): string {
    const period = this.periods.find(p => p.value === this.chartConfig.period);
    return period ? period.label : '';
  }

  getComparisonTitle(): string {
    if (this.chartConfig.comparisonMode === 'byStore') {
      return 'Comparaison par magasin';
    } else if (this.chartConfig.comparisonMode === 'byType') {
      return 'Comparaison par type';
    }
    return 'Comparaison';
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'XOF'
    }).format(price);
  }

  formatDate(date: string): string {
    return new Date(date).toLocaleDateString('fr-FR');
  }

  loadChartData() {
    if (!this.priceChartRef || !this.priceChartRef.nativeElement) {
      console.log('Canvas non disponible');
      return;
    }

    const canvas = this.priceChartRef.nativeElement;
    const ctx = canvas.getContext('2d');
    
    if (!ctx) {
      console.log('Contexte 2D non disponible');
      return;
    }

    // S'assurer que le canvas a une taille
    const container = canvas.parentElement;
    if (container) {
      canvas.width = container.offsetWidth;
      canvas.height = 400;
    }

    if (this.chart) {
      this.chart.destroy();
    }

    // Vérifier qu'on a des données
    if (this.priceData.length === 0) {
      console.log('Aucune donnée disponible pour le graphique');
      return;
    }

    const labels = this.priceData.map(item => item.dateFormatted);
    const datasets = [];

    // Dataset principal (prix moyen)
    const mainDataset: any = {
      label: 'Prix moyen',
      data: this.priceData.map(item => item.averagePrice),
      borderColor: '#3B82F6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      borderWidth: 3,
      tension: 0.4
    };

    // Adapter selon le mode du graphique
    if (this.chartMode === 'bar') {
      mainDataset.type = 'bar';
      mainDataset.borderWidth = 0;
      mainDataset.backgroundColor = '#3B82F6';
      mainDataset.tension = 0;
    } else if (this.chartMode === 'line') {
      mainDataset.type = 'line';
      mainDataset.fill = false;
      mainDataset.backgroundColor = 'rgba(59, 130, 246, 0.1)';
    } else if (this.chartMode === 'area') {
      mainDataset.type = 'line';
      mainDataset.fill = true;
      mainDataset.backgroundColor = 'rgba(59, 130, 246, 0.3)';
    } else if (this.chartMode === 'mixed') {
      mainDataset.type = 'bar';
      mainDataset.borderWidth = 0;
      mainDataset.backgroundColor = '#3B82F6';
      mainDataset.tension = 0;
    }

    datasets.push(mainDataset);

    // Dataset tendance
    if (this.chartConfig.showTrends) {
      const trendDataset: any = {
        label: 'Tendance',
        data: this.priceData.map(item => item.trend),
        borderColor: '#10B981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 2,
        borderDash: [5, 5],
        fill: false,
        tension: 0.4
      };

      // Pour le mode mixte, la tendance est toujours en ligne
      if (this.chartMode === 'mixed' || this.chartMode === 'bar') {
        trendDataset.type = 'line';
      }

      datasets.push(trendDataset);
    }

    // Dataset prédiction
    if (this.chartConfig.showPredictions && this.predictionData.length > 0) {
      const predictionData = this.predictionData.map(item => item.predictedPrice);
      
      const predictionDataset: any = {
        label: 'Prédiction',
        data: [...Array(this.priceData.length - predictionData.length).fill(null), ...predictionData],
        borderColor: '#F59E0B',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        borderWidth: 2,
        borderDash: [10, 5],
        fill: false,
        tension: 0.4
      };

      // Pour le mode mixte, la prédiction est toujours en ligne
      if (this.chartMode === 'mixed' || this.chartMode === 'bar') {
        predictionDataset.type = 'line';
      }

      datasets.push(predictionDataset);
    }

    const config: ChartConfiguration = {
      type: this.chartConfig.type,
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top' as const,
            labels: {
              usePointStyle: true,
              padding: 20,
              font: {
                size: 12
              }
            }
          },
          tooltip: {
            mode: 'index' as const,
            intersect: false,
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${this.formatPrice(context.parsed.y)}`;
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Date'
            }
          },
          y: {
            display: true,
            grid: {
              color: 'rgba(0, 0, 0, 0.1)'
            },
            title: {
              display: true,
              text: 'Prix (XOF)'
            },
            ticks: {
              callback: (value) => {
                return this.formatPrice(value as number);
              }
            }
          }
        },
        interaction: {
          mode: 'nearest' as const,
          axis: 'x' as const,
          intersect: false
        }
      }
    };

    try {
      this.chart = new Chart(ctx, config);
      console.log('Graphique créé avec succès:', {
        type: this.chartConfig.type,
        mode: this.chartMode,
        dataPoints: this.priceData.length,
        showTrends: this.chartConfig.showTrends,
        showPredictions: this.chartConfig.showPredictions
      });
    } catch (error) {
      console.error('Erreur lors de la création du graphique:', error);
    }
  }

  updateTableData() {
    this.tableData = this.priceData;
    this.totalItems = this.priceData.length;
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.updateTableData();
  }

  getTotalPages(): number {
    return Math.ceil(this.totalItems / this.itemsPerPage);
  }

  getPageNumbers(): number[] {
    const totalPages = this.getTotalPages();
    const currentPage = this.currentPage;
    const pages: number[] = [];

    if (totalPages <= 7) {
      // Si moins de 7 pages, afficher toutes les pages
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Si plus de 7 pages, afficher avec "..." au milieu
      if (currentPage <= 4) {
        // Pages 1-5 + ... + dernière page
        for (let i = 1; i <= 5; i++) {
          pages.push(i);
        }
        pages.push(-1); // -1 représente "..."
        pages.push(totalPages);
      } else if (currentPage >= totalPages - 3) {
        // Première page + ... + pages (totalPages-4) à totalPages
        pages.push(1);
        pages.push(-1); // -1 représente "..."
        for (let i = totalPages - 4; i <= totalPages; i++) {
          pages.push(i);
        }
      } else {
        // Première page + ... + page courante ±1 + ... + dernière page
        pages.push(1);
        pages.push(-1); // -1 représente "..."
        for (let i = currentPage - 1; i <= currentPage + 1; i++) {
          pages.push(i);
        }
        pages.push(-1); // -1 représente "..."
        pages.push(totalPages);
      }
    }

    return pages;
  }

  getDisplayedItemsRange(): string {
    const start = (this.currentPage - 1) * this.itemsPerPage + 1;
    const end = Math.min(this.currentPage * this.itemsPerPage, this.totalItems);
    return `Affichage ${start} à ${end} sur ${this.totalItems} entrées`;
  }

  getComparisonData(date: string): string | null {
    const item = this.priceData.find(p => p.date === date);
    if (!item) return null;
    
    if (this.chartConfig.comparisonMode === 'byStore') {
      return `+${Math.round(Math.random() * 20)}% vs moy.`;
    } else if (this.chartConfig.comparisonMode === 'byType') {
      return `${Math.round(Math.random() * 15)}% vs type`;
    }
    return null;
  }

  openPredictionModal() {
    this.showPredictionModal = true;
  }

  closePredictionModal() {
    this.showPredictionModal = false;
  }

  generatePrediction() {
    this.isLoading = true;
    setTimeout(() => {
      this.generatePredictionData();
      this.isLoading = false;
      this.closePredictionModal();
      this.loadChartData();
    }, 2000);
  }

  getPredictionTrendPoints(): string {
    if (this.predictionData.length === 0) return '';
    
    const points = this.predictionData.map((item, index) => {
      const x = (index / (this.predictionData.length - 1)) * 100;
      const y = 100 - ((item.predictedPrice - 1500) / 2500) * 100;
      return `${x},${y}`;
    });
    
    return points.join(' ');
  }
}
