import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    loadComponent: () => import('./components/price-comparison/price-comparison.component').then(m => m.PriceComparisonComponent)
  },
  {
    path: 'scanner',
    loadComponent: () => import('./components/receipt-scanner/receipt-scanner.component').then(m => m.ReceiptScannerComponent)
  },
  {
    path: 'receipts',
    loadComponent: () => import('./components/receipt-list/receipt-list.component').then(m => m.ReceiptListComponent)
  },
  {
    path: '**',
    redirectTo: '/home'
  }
];
