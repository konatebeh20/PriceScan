import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../../services/user/user.service';
import { BarcodeScannerService } from '../../../services/barcode/barcode-scanner.service';
import { ProductsService } from '../../../services/products/products.service';
import { StoresService } from '../../../services/stores/stores.service';
import { ReceiptsService } from '../../../services/receipts/receipts.service';

@Component({
  selector: 'app-receipts-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './receipts-list.html',
  styleUrls: ['./receipts-list.scss']
})
export class ReceiptsListComponent implements OnInit, OnDestroy {
  // User and store management
  currentUser: any = null;
  userStores: any[] = [];
  selectedStore: any = null;

  // Time management
  currentTime: string = '';
  timeInterval: any;

  // Barcode scanning
  scannedBarcode: string = '';
  isScanning: boolean = false;
  scannerMessage: string = '';
  scannedProducts: any[] = [];

  // Manual receipt form
  manualReceipt: any = {
    storeId: '',
    storeName: '',
    storeAddress: '',
    date: '',
    time: '',
    items: [],
    total: 0
  };

  // Receipts list
  receipts: any[] = [];
  filteredReceipts: any[] = [];
  searchTerm: string = '';
  filterType: 'all' | 'archived' | 'active' = 'all';
  
  // Tab management
  activeTab: 'scanned' | 'manual' | 'archived' = 'scanned';
  
  // Compatibility getter used by template (legacy name)
  get isScannerActive(): boolean {
    return this.isScanning;
  }
  
  // Filter properties
  selectedStoreFilter: string = '';
  selectedPeriod: string = '';
  selectedAmount: string = '';
  selectedStatus: string = '';
  
  // Store list for manual form
  stores: any[] = [];

  constructor(
    private userService: UserService,
    private barcodeScannerService: BarcodeScannerService,
    private productsService: ProductsService,
    private storesService: StoresService,
    private receiptsService: ReceiptsService
  ) {}

  ngOnInit(): void {
    this.loadCurrentUser();
    this.loadUserStores();
    this.loadReceipts();
    this.startTimeUpdate();
    this.initializeManualForm();
    this.setupBarcodeListener();
  }

  ngOnDestroy(): void {
    this.stopTimeUpdate();
    this.cleanupBarcodeListener();
  }

  // Time management
  startTimeUpdate(): void {
    this.updateCurrentTime();
    this.timeInterval = setInterval(() => {
      this.updateCurrentTime();
    }, 1000);
  }

  stopTimeUpdate(): void {
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  }

  updateCurrentTime(): void {
    const now = new Date();
    this.currentTime = now.toTimeString().slice(0, 5);
    // Keep manual receipt time in sync
    if (this.manualReceipt) {
      this.manualReceipt.time = this.currentTime;
    }
  }

  // User and store management
  loadCurrentUser(): void {
    this.currentUser = this.userService.getCurrentUser();
    if (this.currentUser) {
      this.autoFillStoreInfo();
    }
  }

  loadUserStores(): void {
    if (this.currentUser?.accountType !== 'particulier') {
      this.userStores = this.storesService.getCurrentStores();
      this.stores = this.storesService.getCurrentStores();
    }
  }

  autoFillStoreInfo(): void {
    if (this.currentUser?.accountType !== 'particulier') {
      this.manualReceipt.storeName = this.currentUser.businessName || '';
      this.manualReceipt.storeAddress = this.buildStoreAddress();
    }
  }

  buildStoreAddress(): string {
    if (!this.currentUser) return '';
    
    const address = this.currentUser.businessAddress || '';
    const location = this.currentUser.businessLocation || '';
    
    if (address && location) {
      return `${address}, ${location}`;
    } else if (address) {
      return address;
    } else if (location) {
      return location;
    }
    return '';
  }

  onStoreChange(): void {
    const found = this.stores.find(s => String(s.id) === String(this.manualReceipt.storeId));
    if (found) {
      this.manualReceipt.storeName = found.name;
      this.manualReceipt.storeAddress = found.address;
    }
  }

  setActiveTab(tab: 'scanned' | 'manual' | 'archived'): void {
    this.activeTab = tab;
  }

  // Barcode scanning
  setupBarcodeListener(): void {
    document.addEventListener('barcodeScanned', (event: any) => {
      this.handleScannedBarcode(event.detail.barcode);
    });
  }

  cleanupBarcodeListener(): void {
    document.removeEventListener('barcodeScanned', () => {});
  }

  startBarcodeScanner(): void {
    this.isScanning = true;
    this.scannerMessage = 'Scanner activé - Scannez un code-barres';
    this.barcodeScannerService.startScanner();
  }

  stopBarcodeScanner(): void {
    this.isScanning = false;
    this.scannerMessage = 'Scanner arrêté';
    this.barcodeScannerService.stopScanner();
  }

  handleScannedBarcode(barcode: string): void {
    this.scannedBarcode = barcode;
    this.scannerMessage = `Code-barres scanné: ${barcode}`;
    
    // Auto-stop scanner after successful scan
    setTimeout(() => {
      this.stopBarcodeScanner();
    }, 2000);

    this.addScannedProduct(barcode);
  }

  addScannedProduct(barcode: string): void {
    const product = this.productsService.searchProductsByBarcode(barcode);
    
    if (product) {
      // Check if product already exists in scanned products
      const existingProduct = this.scannedProducts.find(p => p.barcode === barcode);
      
      if (existingProduct) {
        existingProduct.quantity += 1;
        existingProduct.totalPrice = existingProduct.quantity * existingProduct.price;
      } else {
        const scannedProduct = {
          barcode: barcode,
          name: product.name,
          price: product.price,
          quantity: 1,
          totalPrice: product.price
        };
        this.scannedProducts.push(scannedProduct);
      }
      
      this.updateManualReceiptTotal();
    } else {
      this.scannerMessage = `Produit non trouvé pour le code: ${barcode}`;
    }
  }

  updateScannedProductQuantity(barcode: string, change: number): void {
    const product = this.scannedProducts.find(p => p.barcode === barcode);
    if (product) {
      product.quantity = Math.max(1, product.quantity + change);
      product.totalPrice = product.quantity * product.price;
      this.updateManualReceiptTotal();
    }
  }

  removeScannedProduct(barcode: string): void {
    this.scannedProducts = this.scannedProducts.filter(p => p.barcode !== barcode);
    this.updateManualReceiptTotal();
  }

  // Manual receipt form
  initializeManualForm(): void {
    const now = new Date();
    this.manualReceipt = {
      storeId: '',
      storeName: this.currentUser?.accountType !== 'particulier' ? (this.currentUser.businessName || '') : '',
      storeAddress: this.currentUser?.accountType !== 'particulier' ? this.buildStoreAddress() : '',
      date: now.toISOString().split('T')[0],
      time: this.currentTime,
      items: [
        { name: '', price: 0, qty: 1 }
      ],
      total: 0
    };
    this.scannedProducts = [];
  }

  addProductRow(): void {
    this.manualReceipt.items.push({
      name: '',
      price: 0,
      qty: 1
    });
  }

  removeProductRow(index: number): void {
    this.manualReceipt.items.splice(index, 1);
    this.updateManualReceiptTotal();
  }

  updateManualReceiptTotal(): void {
    let total = 0;
    
    // Add scanned products total
    total += this.scannedProducts.reduce((sum: number, product: any) => sum + product.totalPrice, 0);
    
    // Add manual items total
    total += this.manualReceipt.items.reduce((sum: number, item: any) => sum + (item.price * item.qty), 0);
    
    this.manualReceipt.total = total;
  }

  saveManualReceipt(): void {
    // Convert scanned products to receipt items
    const allItems = [
      ...this.scannedProducts.map(product => ({
        name: product.name,
        price: product.price,
        qty: product.quantity
      })),
      ...this.manualReceipt.items
    ];

    const receipt = {
      store: this.manualReceipt.storeName,
      address: this.manualReceipt.storeAddress,
      date: this.manualReceipt.date,
      time: this.manualReceipt.time,
      items: allItems,
      total: this.manualReceipt.total.toString(),
      type: 'manual' as const,
      ticketNumber: 'MAN' + Date.now(),
      status: 'analyzed' as const,
      isFavorite: false
    };

    this.receiptsService.addReceipt(receipt);
    this.loadReceipts();
    this.resetManualForm();
  }

  resetManualForm(): void {
    this.initializeManualForm();
    this.scannedProducts = [];
    this.scannedBarcode = '';
    this.scannerMessage = '';
  }

  // Receipts management
  loadReceipts(): void {
    this.receipts = this.receiptsService.getCurrentReceipts();
    this.filterReceipts();
  }

  filterReceipts(): void {
    let filtered = this.receipts;

    if (this.searchTerm) {
      filtered = filtered.filter(receipt =>
        receipt.store.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        receipt.items.some((item: any) => item.name.toLowerCase().includes(this.searchTerm.toLowerCase()))
      );
    }

    if (this.filterType === 'archived') {
      filtered = filtered.filter(receipt => receipt.type === 'archived');
    } else if (this.filterType === 'active') {
      filtered = filtered.filter(receipt => receipt.type !== 'archived');
    }

    this.filteredReceipts = filtered;
  }

  // Receipt actions
  archiveReceipt(receipt: any): void {
    this.receiptsService.updateReceipt(receipt.id, { type: 'archived' });
    this.loadReceipts();
  }

  restoreReceipt(receipt: any): void {
    this.receiptsService.updateReceipt(receipt.id, { type: 'manual' });
    this.loadReceipts();
  }

  deleteReceipt(receipt: any): void {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce reçu ?')) {
      this.receiptsService.deleteReceipt(receipt.id);
      this.loadReceipts();
    }
  }

  toggleFavorite(receipt: any): void {
    this.receiptsService.updateReceipt(receipt.id, { isFavorite: !receipt.isFavorite });
    this.loadReceipts();
  }

  viewReceipt(receipt: any): void {
    console.log('Voir le reçu:', receipt);
  }

  printReceipt(receipt: any): void {
    console.log('Imprimer le reçu:', receipt);
  }

  // Getters
  get archivedReceipts(): any[] {
    return this.receipts.filter(receipt => receipt.type === 'archived');
  }

  getStatusLabel(receiptStatus: 'analyzed' | 'processing' | 'failed'): string {
    switch (receiptStatus) {
      case 'analyzed': return 'Analysé';
      case 'processing': return 'En cours';
      case 'failed': return 'Échoué';
      default: return '';
    }
  }
}
