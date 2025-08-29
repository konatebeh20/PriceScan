import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DashboardPageComponent } from '../../pages/dashboard-page/dashboard-page';
import { ReceiptsListComponent } from '../../pages/receipts/receipts-list/receipts-list';
import { ProductsListComponent } from '../../pages/products/products-list/products-list';
import { StoresListComponent } from '../../pages/stores/stores-list/stores-list';
import { SettingsPageComponent } from '../../pages/settings/settings-page/settings-page';
import { DemoPageComponent } from '../../pages/demo-page/demo-page';
import { ProfileComponent } from '../../pages/profile/profile';

@Component({
  selector: 'app-main-content',
  standalone: true,
  imports: [CommonModule, FormsModule, DashboardPageComponent, ReceiptsListComponent, ProductsListComponent, StoresListComponent, SettingsPageComponent, DemoPageComponent, ProfileComponent],
  templateUrl: './main-content.html',
  styleUrls: ['./main-content.scss']
})
export class MainContentComponent implements OnChanges {
  @Input() currentPage: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile' = 'dashboard';
  @Output() pageChange = new EventEmitter<'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile'>();

  constructor() {
    console.log('MainContentComponent constructor - currentPage:', this.currentPage);
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['currentPage']) {
      console.log('MainContentComponent - currentPage changé vers:', this.currentPage);
      console.log('Valeur précédente:', changes['currentPage'].previousValue);
      console.log('Valeur actuelle:', changes['currentPage'].currentValue);
    }
  }

  // Placeholder methods for future implementation
  loadProducts() {
    console.log('Loading products...');
  }

  loadReceipts() {
    console.log('Loading receipts...');
  }

  loadStores() {
    console.log('Loading stores...');
  }

  exportData() {
    console.log('Exporting data...');
  }
}
