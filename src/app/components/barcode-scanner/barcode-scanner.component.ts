import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { ZXingScannerModule } from '@zxing/ngx-scanner';
import { BarcodeFormat } from '@zxing/library';
import { PriceService } from '../../services/price.service';

@Component({
  selector: 'app-barcode-scanner',
  standalone: true,
  imports: [CommonModule, ZXingScannerModule, MatCardModule, MatProgressSpinnerModule, MatFormFieldModule],
  templateUrl: './barcode-scanner.component.html',
  styleUrls: ['./barcode-scanner.component.scss']
})
export class BarcodeScannerComponent {
  allowedFormats = [BarcodeFormat.QR_CODE, BarcodeFormat.EAN_13, BarcodeFormat.CODE_128, BarcodeFormat.DATA_MATRIX];
  scannedCode: string = '';
  productInfo: any = null;
  loading: boolean = false;
  error: string = '';

  constructor(private priceService: PriceService) {}

  onScanSuccess(result: string) {
    this.scannedCode = result;
    this.loading = true;
    this.error = '';
    this.priceService.getProductInfo(result).subscribe({
      next: (data) => {
        this.productInfo = data;
        this.loading = false;
      },
      error: () => {
        this.error = "Échec de la récupération des informations du produit";
        this.loading = false;
      }
    });
  }
}