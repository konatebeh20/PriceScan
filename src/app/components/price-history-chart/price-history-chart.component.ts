import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { NgChartsModule } from 'ng2-charts';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PriceService } from '../../services/price.service';

@Component({
  selector: 'app-price-history-chart',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    NgChartsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './price-history-chart.component.html',
  styleUrls: ['./price-history-chart.component.scss']
})
export class PriceHistoryChartComponent {
  productCode: string = '';
  lineChartType: ChartType = 'line';
  lineChartData: ChartData<'line'> = { datasets: [], labels: [] };
  lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Prix (€)' }
      },
      x: {
        title: { display: true, text: 'Date' }
      }
    }
  };
  loading: boolean = false;
  error: string = '';

  constructor(private priceService: PriceService) {}

  onProductCodeChange() {
    this.lineChartData = { datasets: [], labels: [] };
    this.error = '';
  }

  loadHistory() {
    this.loading = true;
    this.error = '';
    this.priceService.getPrices(this.productCode).subscribe({
      next: (data) => {
        const stores = [...new Set(data.map(item => item.store))];
        this.lineChartData.labels = [...new Set(data.map(item => new Date(item.date).toLocaleDateString('fr-FR')))].sort();
        this.lineChartData.datasets = stores.map(store => ({
          data: data.filter(item => item.store === store).map(item => item.price),
          label: store,
          borderColor: this.getRandomColor(),
          fill: false
        }));
        this.loading = false;
      },
      error: () => {
        this.error = "Échec du chargement de l'historique des prix";
        this.loading = false;
      }
    });
  }

  private getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
}