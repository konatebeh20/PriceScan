import { Routes } from '@angular/router';
import { BarcodeScannerComponent } from './components/barcode-scanner/barcode-scanner.component';
import { PriceEntryComponent } from './components/price-entry/price-entry.component';
import { ProductComparisonComponent } from './components/product-comparison/product-comparison.component';
import { PriceHistoryChartComponent } from './components/price-history-chart/price-history-chart.component';

export const routes: Routes = [
  { path: 'scan', component: BarcodeScannerComponent },
  { path: 'entry', component: PriceEntryComponent },
  { path: 'comparison', component: ProductComparisonComponent },
  { path: 'history', component: PriceHistoryChartComponent },
  { path: '', redirectTo: '/scan', pathMatch: 'full' }
];