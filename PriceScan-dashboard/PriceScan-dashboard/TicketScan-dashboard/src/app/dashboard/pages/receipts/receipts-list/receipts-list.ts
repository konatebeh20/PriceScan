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
  // selectedStore: any = null; // Remplacé par la nouvelle propriété

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
    isAddressEditable: false, // Permettre la saisie manuelle de l'adresse
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
  // selectedStoreFilter: string = ''; // Remplacé par selectedStore
  selectedPeriod: string = '';
  selectedAmount: string = '';
  selectedStatus: string = '';
  
  // Store list for manual form
  stores: any[] = [];
  availableStores: any[] = []; // Magasins disponibles depuis la base de données

  // Propriétés pour la modal
  showReceiptModal = false;
  selectedReceipt: any = null;

  // Données dynamiques pour les filtres
  storesForFilter: any[] = [];
  periodsForFilter: any[] = [];
  amountsForFilter: any[] = [];
  statusesForFilter: any[] = [];

  // Propriétés des filtres (remplacent les anciennes)
  selectedStore: string = '';
  // selectedPeriod: string = '';
  // selectedAmount: string = '';
  // selectedStatus: string = '';

  constructor(
    private userService: UserService,
    private barcodeScannerService: BarcodeScannerService,
    private productsService: ProductsService,
    private storesService: StoresService,
    private receiptsService: ReceiptsService
  ) {}

  ngOnInit(): void {
    this.loadFilterData();
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
    // Charger tous les magasins disponibles depuis la base de données
    this.storesService.refreshStores();
    
    // S'abonner aux changements des magasins
    this.storesService.getStores().subscribe((stores) => {
      this.availableStores = stores;
      this.stores = stores;
      
      // Si l'utilisateur est un commerce, filtrer ses magasins spécifiques
      if (this.currentUser?.accountType !== 'particulier') {
        // Pour l'instant, on prend tous les magasins disponibles
        // TODO: Implémenter la logique de filtrage par propriétaire quand l'API le supporte
        this.userStores = stores;
      }
      
      console.log(' Magasins chargés:', stores.length);
    });
  }

  autoFillStoreInfo(): void {
    if (this.currentUser?.accountType !== 'particulier') {
      this.manualReceipt.storeName = this.currentUser.businessName || '';
      this.manualReceipt.storeAddress = this.buildStoreAddress();
    } else {
      // Si c'est un particulier, utiliser son nom d'utilisateur
      this.manualReceipt.storeName = this.currentUser?.u_username || this.currentUser?.username || '';
      this.manualReceipt.storeAddress = this.currentUser?.u_business_address || this.currentUser?.businessAddress || '';
    }
  }

  // Obtenir l'icône du type de compte
  getAccountTypeIcon(): string {
    if (!this.currentUser) return 'fa-user';
    
    switch (this.currentUser.accountType) {
      case 'supermarche':
        return 'fa-shopping-cart';
      case 'pharmacie':
        return 'fa-pills';
      case 'quincaillerie':
        return 'fa-tools';
      case 'boutique':
        return 'fa-store';
      case 'particulier':
        return 'fa-user';
      default:
        return 'fa-building';
    }
  }

  // Obtenir le label du type de compte
  getAccountTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      'supermarche': 'Supermarché',
      'pharmacie': 'Pharmacie',
      'quincaillerie': 'Quincaillerie',
      'boutique': 'Boutique',
      'particulier': 'Particulier'
    };
    return labels[type] || type;
  }

  // Obtenir l'icône du type de magasin pour les reçus
  getStoreTypeIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'supermarche': 'fa-shopping-basket',
      'pharmacie': 'fa-medkit',
      'quincaillerie': 'fa-wrench',
      'boutique': 'fa-store',
      'particulier': 'fa-user',
      'autre': 'fa-store'
    };
    return icons[type] || 'fa-store';
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
      this.manualReceipt.storeName = found.store_name || found.name || '';
      this.manualReceipt.storeAddress = found.store_address || found.address || '';
      
      // Mettre à jour automatiquement l'adresse complète
      this.updateStoreAddress(found);
    }
  }
  
  // Mettre à jour l'adresse complète du magasin
  updateStoreAddress(store: any): void {
    let fullAddress = '';
    
    if (store.store_address || store.address) {
      fullAddress += store.store_address || store.address;
    }
    
    if (store.store_city || store.city) {
      if (fullAddress) fullAddress += ', ';
      fullAddress += store.store_city || store.city;
    }
    
    if (store.store_country) {
      if (fullAddress) fullAddress += ', ';
      fullAddress += store.store_country;
    }
    
    this.manualReceipt.storeAddress = fullAddress;
    
    // Si aucune adresse n'est trouvée, permettre la saisie manuelle
    if (!fullAddress) {
      this.manualReceipt.storeAddress = '';
      this.manualReceipt.isAddressEditable = true;
    } else {
      this.manualReceipt.isAddressEditable = false;
    }
  }
  
  // Permettre la saisie manuelle de l'adresse
  enableManualAddressEdit(): void {
    this.manualReceipt.isAddressEditable = true;
    this.manualReceipt.storeAddress = '';
  }
  
  // Désactiver la saisie manuelle et revenir à l'adresse automatique
  disableManualAddressEdit(): void {
    this.manualReceipt.isAddressEditable = false;
    // Reconstruire l'adresse depuis le magasin sélectionné
    if (this.manualReceipt.storeId) {
      const selectedStore = this.stores.find(s => String(s.id) === String(this.manualReceipt.storeId));
      if (selectedStore) {
        this.updateStoreAddress(selectedStore);
      }
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
          name: product.product_name,
          price: product.price_amount,
          quantity: 1,
          totalPrice: product.price_amount
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
      isAddressEditable: false, // Initialiser la propriété d'édition
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

  // Charger les données pour les filtres depuis la base de données
  loadFilterData(): void {
    this.loadStoresForFilter();
    this.loadPeriodsForFilter();
    this.loadAmountsForFilter();
    this.loadStatusesForFilter();
  }

  // Charger les magasins pour le filtre
  loadStoresForFilter(): void {
    // TODO: Remplacer par un appel API réel
    this.storesForFilter = [
      { id: 'carrefour', name: 'Carrefour Market', city: 'Abidjan' },
      { id: 'prosuma', name: 'Prosuma', city: 'Abidjan' },
      { id: 'casino', name: 'Casino', city: 'Yamoussoukro' },
      { id: 'citydia', name: 'Citydia', city: 'Bouaké' },
      { id: 'pharmacie_centrale', name: 'Pharmacie Centrale', city: 'Abidjan' },
      { id: 'quincaillerie_modern', name: 'Quincaillerie Moderne', city: 'San-Pédro' }
    ];
  }

  // Charger les périodes pour le filtre
  loadPeriodsForFilter(): void {
    this.periodsForFilter = [
      { id: 'today', name: 'Aujourd\'hui', value: 'today' },
      { id: 'week', name: 'Cette semaine', value: 'week' },
      { id: 'month', name: 'Ce mois', value: 'month' },
      { id: 'year', name: 'Cette année', value: 'year' },
      { id: 'custom', name: 'Période personnalisée', value: 'custom' }
    ];
  }

  // Charger les montants pour le filtre
  loadAmountsForFilter(): void {
    this.amountsForFilter = [
      { id: 'low', name: 'Moins de 10 000 F CFA', min: 0, max: 10000 },
      { id: 'medium', name: '10 000 - 30 000 F CFA', min: 10000, max: 30000 },
      { id: 'high', name: 'Plus de 30 000 F CFA', min: 30000, max: null },
      { id: 'custom', name: 'Montant personnalisé', min: null, max: null }
    ];
  }

  // Charger les statuts pour le filtre
  loadStatusesForFilter(): void {
    this.statusesForFilter = [
      { id: 'analyzed', name: 'Analysé', color: '#10b981' },
      { id: 'processing', name: 'En cours', color: '#f59e0b' },
      { id: 'failed', name: 'Échoué', color: '#ef4444' },
      { id: 'pending', name: 'En attente', color: '#6b7280' }
    ];
  }

  // Filtrer les reçus selon les critères sélectionnés
  filterReceipts(): void {
    let filtered = [...this.receipts];

    // Filtre par magasin
    if (this.selectedStore) {
      filtered = filtered.filter(receipt => receipt.storeId === this.selectedStore);
    }

    // Filtre par période
    if (this.selectedPeriod) {
      filtered = filtered.filter(receipt => this.isInPeriod(receipt.date, this.selectedPeriod));
    }

    // Filtre par montant
    if (this.selectedAmount) {
      const amountFilter = this.amountsForFilter.find(a => a.id === this.selectedAmount);
      if (amountFilter) {
        filtered = filtered.filter(receipt => {
          const total = parseFloat(receipt.total.toString().replace(/[^\d.-]/g, ''));
          if (amountFilter.min !== null && amountFilter.max !== null) {
            return total >= amountFilter.min && total <= amountFilter.max;
          } else if (amountFilter.min !== null) {
            return total >= amountFilter.min;
          } else if (amountFilter.max !== null) {
            return total <= amountFilter.max;
          }
          return true;
        });
      }
    }

    // Filtre par statut
    if (this.selectedStatus) {
      filtered = filtered.filter(receipt => receipt.status === this.selectedStatus);
    }

    this.filteredReceipts = filtered;
    console.log(` Filtrage: ${filtered.length} reçus trouvés sur ${this.receipts.length}`);
  }

  // Vérifier si une date est dans la période sélectionnée
  isInPeriod(dateStr: string, period: string): boolean {
    const date = new Date(dateStr);
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    
    switch (period) {
      case 'today':
        return date >= today;
      case 'week':
        const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
        return date >= weekAgo;
      case 'month':
        const monthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
        return date >= monthAgo;
      case 'year':
        const yearAgo = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());
        return date >= yearAgo;
      default:
        return true;
    }
  }

  // Réinitialiser tous les filtres
  resetFilters(): void {
    this.selectedStore = '';
    this.selectedPeriod = '';
    this.selectedAmount = '';
    this.selectedStatus = '';
    this.filteredReceipts = [...this.receipts];
    console.log(' Filtres réinitialisés');
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
    this.selectedReceipt = receipt;
    this.showReceiptModal = true;
  }

  closeReceiptModal(): void {
    this.showReceiptModal = false;
    this.selectedReceipt = null;
  }

  printReceipt(receipt: any): void {
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      const printContent = `
        <html>
          <head>
            <title>Reçu - ${receipt.store}</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 20px; }
              .receipt-header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }
              .store-name { font-size: 24px; font-weight: bold; }
              .receipt-number { font-size: 18px; color: #666; }
              .receipt-date { font-size: 16px; color: #666; }
              .items-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
              .items-table th, .items-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
              .items-table th { background-color: #f5f5f5; }
              .total-section { text-align: right; font-size: 18px; font-weight: bold; margin-top: 20px; }
              @media print { body { margin: 0; } }
            </style>
          </head>
          <body>
            <div class="receipt-header">
              <div class="store-name">${receipt.store}</div>
              <div class="receipt-number">#${receipt.ticketNumber}</div>
              <div class="receipt-date">${receipt.date} à ${receipt.time}</div>
            </div>
            
            <table class="items-table">
              <thead>
                <tr>
                  <th>Article</th>
                  <th>Quantité</th>
                  <th>Prix unitaire</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                ${receipt.items.map((item: any) => `
                  <tr>
                    <td>${item.name}</td>
                    <td>${item.qty}</td>
                    <td>${item.price} F CFA</td>
                    <td>${item.qty * item.price} F CFA</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
            
            <div class="total-section">
              <div>Total: ${receipt.total} F CFA</div>
            </div>
          </body>
        </html>
      `;
      printWindow.document.write(printContent);
      printWindow.document.close();
      printWindow.print();
    }
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
