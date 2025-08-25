import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule, CurrencyPipe, DatePipe } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PriceService } from '../../services/price.service';

@Component({
  selector: 'app-product-comparison',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatTableModule,
    MatProgressSpinnerModule,
    CurrencyPipe,
    DatePipe
  ],
  templateUrl: './product-comparison.component.html',
  styleUrls: ['./product-comparison.component.scss']
})
export class ProductComparisonComponent {
  productCode: string = '';
  comparisons: any[] = [];
  displayedColumns: string[] = ['store', 'price', 'date'];
  loading: boolean = false;
  error: string = '';

  constructor(private priceService: PriceService) {}

  onProductCodeChange() {
    this.comparisons = [];
    this.error = '';
  }

  loadComparisons() {
    this.loading = true;
    this.error = '';
    this.priceService.getPrices(this.productCode).subscribe({
      next: (data) => {
        this.comparisons = data.sort((a, b) => a.price - b.price);
        this.loading = false;
      },
      error: () => {
        this.error = "Échec du chargement des comparaisons";
        this.loading = false;
      }
    });
  }
}