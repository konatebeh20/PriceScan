import { Component, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnInit {
  protected readonly title = signal('TicketScan-dashboard');
  
  // User management system avec sessionStorage
  users: any[] = [];
  currentUser: any = null;
  
  // Products management system
  products: any[] = [];
  manualReceipts: any[] = [];
  archivedReceipts: any[] = [];
  stores: any[] = [];
  productRowCounter = 0;
  confirmAction: any = null;
  currentViewingReceipt: any = null;
  barcodeScannerStream: any = null;
  scannedProductData: any = null;
  
  // UI State
  currentTab: 'login' | 'register' = 'login';
  currentPage: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' = 'dashboard';
  isSidebarCollapsed = false;
  isDarkTheme = false;
  isUserMenuOpen = false;
  isLoading = false;
  
  // Notification system
  notification = { show: false, message: '', type: 'success' };
  
  // Computed properties for template
  get activeProductsCount(): number {
    return this.products.filter(p => p.status === 'active').length;
  }
  
  get archivedProductsCount(): number {
    return this.products.filter(p => p.status === 'archived').length;
  }
  
  get activeStoresCount(): number {
    return this.stores.filter(s => s.status === 'active').length;
  }
  
  get archivedStoresCount(): number {
    return this.stores.filter(s => s.status === 'archived').length;
  }
  
  // Sample data
  sampleProducts = [
    { id: 1, name: 'Pain de mie', category: 'alimentaire', price: 750, unit: 'pièce', description: 'Pain de mie complet', status: 'active', createdAt: '2024-11-10', updatedAt: '2024-11-15' },
    { id: 2, name: 'Lait UHT 1L', category: 'alimentaire', price: 750, unit: 'l', description: 'Lait entier UHT', status: 'active', createdAt: '2024-11-10', updatedAt: '2024-11-15' },
    { id: 3, name: 'Yaourt nature', category: 'alimentaire', price: 800, unit: 'pièce', description: 'Yaourt nature 125g', status: 'active', createdAt: '2024-11-10', updatedAt: '2024-11-15' },
    { id: 4, name: 'Bananes', category: 'alimentaire', price: 1800, unit: 'kg', description: 'Bananes fraîches', status: 'active', createdAt: '2024-11-10', updatedAt: '2024-11-15' },
    { id: 5, name: 'Riz parfumé', category: 'alimentaire', price: 1940, unit: 'kg', description: 'Riz parfumé de qualité', status: 'active', createdAt: '2024-11-10', updatedAt: '2024-11-15' },
    { id: 6, name: 'Huile végétale', category: 'alimentaire', price: 6000, unit: 'l', description: 'Huile végétale 5L', status: 'active', createdAt: '2024-11-10', updatedAt: '2024-11-15' },
    { id: 7, name: 'Dentifrice', category: 'hygiene', price: 2500, unit: 'pièce', description: 'Dentifrice fluoré', status: 'archived', createdAt: '2024-11-05', updatedAt: '2024-11-10' }
  ];

  sampleStores = [
    { id: 1, name: 'Carrefour Market', type: 'supermarche', address: 'Boulevard Lagunaire, Cocody, Abidjan, Côte d\'Ivoire', phone: '+225 27 22 44 55 66', email: 'contact@carrefour-ci.com', notes: 'Grand supermarché avec tous produits', status: 'active', createdAt: '2024-11-01', updatedAt: '2024-11-15' },
    { id: 2, name: 'Prosuma', type: 'supermarche', address: 'Rue des Jardins, Plateau, Abidjan, Côte d\'Ivoire', phone: '+225 27 20 30 40 50', email: 'info@prosuma.ci', notes: 'Supermarché de proximité', status: 'active', createdAt: '2024-11-01', updatedAt: '2024-11-15' },
    { id: 3, name: 'Casino', type: 'supermarche', address: 'Avenue Chardy, Cocody, Abidjan, Côte d\'Ivoire', phone: '+225 27 22 33 44 55', email: 'contact@casino-ci.com', notes: 'Supermarché français', status: 'active', createdAt: '2024-11-01', updatedAt: '2024-11-15' },
    { id: 4, name: 'Pharmacie Centrale', type: 'pharmacie', address: 'Avenue Houphouët-Boigny, Plateau, Abidjan, Côte d\'Ivoire', phone: '+225 27 20 21 22 23', email: 'contact@pharmacie-centrale.ci', notes: 'Pharmacie principale du centre-ville', status: 'active', createdAt: '2024-11-01', updatedAt: '2024-11-15' },
    { id: 5, name: 'Magasin du Coin', type: 'magasin', address: 'Quartier Résidentiel, Yopougon, Abidjan, Côte d\'Ivoire', phone: '+225 27 23 45 67 89', email: '', notes: 'Petit magasin de quartier', status: 'active', createdAt: '2024-11-01', updatedAt: '2024-11-15' }
  ];

  sampleReceipts = [
    {
      id: 1,
      store: 'Carrefour Market',
      address: 'Bamako, Mali - Tél: +223 20 22 33 44',
      date: '15 Nov 2024',
      time: '14:30',
      ticketNumber: 'TK001',
      status: 'analyzed',
      items: [
        { name: 'Pain de mie', qty: 2, price: '1 500 F CFA' },
        { name: 'Lait UHT 1L', qty: 3, price: '2 250 F CFA' },
        { name: 'Yaourt nature', qty: 4, price: '3 200 F CFA' },
        { name: 'Bananes 1kg', qty: 1, price: '1 800 F CFA' },
        { name: 'Riz parfumé 5kg', qty: 1, price: '9 700 F CFA' }
      ],
      total: '18 450 F CFA'
    },
    {
      id: 2,
      store: 'Prosuma',
      address: 'Bamako, Mali - Tél: +223 20 22 55 66',
      date: '12 Nov 2024',
      time: '16:45',
      ticketNumber: 'TK002',
      status: 'processing',
      items: [
        { name: 'Huile végétale 5L', qty: 2, price: '12 000 F CFA' },
        { name: 'Sucre blanc 2kg', qty: 3, price: '4 500 F CFA' },
        { name: 'Farine de blé 2kg', qty: 2, price: '3 200 F CFA' },
        { name: 'Tomates fraîches 2kg', qty: 1, price: '2 800 F CFA' },
        { name: 'Poulet entier', qty: 2, price: '10 250 F CFA' }
      ],
      total: '32 750 F CFA'
    }
  ];

  ngOnInit() {
    this.initializeApp();
  }

  private initializeApp() {
    // Load data from sessionStorage
    this.users = JSON.parse(sessionStorage.getItem('ticketscan_users') || '[]');
    this.currentUser = JSON.parse(sessionStorage.getItem('ticketscan_current_user') || 'null');
    this.products = JSON.parse(sessionStorage.getItem('ticketscan_products') || '[]');
    this.manualReceipts = JSON.parse(sessionStorage.getItem('ticketscan_manual_receipts') || '[]');
    this.archivedReceipts = JSON.parse(sessionStorage.getItem('ticketscan_archived_receipts') || '[]');
    this.stores = JSON.parse(sessionStorage.getItem('ticketscan_stores') || '[]');

    // Initialize sample data if empty
    if (this.products.length === 0) {
      this.products = this.sampleProducts;
      sessionStorage.setItem('ticketscan_products', JSON.stringify(this.products));
    }

    if (this.stores.length === 0) {
      this.stores = this.sampleStores;
      sessionStorage.setItem('ticketscan_stores', JSON.stringify(this.stores));
    }

    // Check if user is already logged in
    if (this.currentUser) {
      this.showDashboard();
      this.updateUserDisplay();
      this.loadReceipts();
      this.loadDashboardData();
    }
  }

  // Tab switching functionality
  switchTab(tabName: 'login' | 'register') {
    this.currentTab = tabName;
    this.clearFormErrors();
  }

  // Form validation helpers
  clearFormErrors() {
    // Implementation for clearing form errors
  }

  // Business fields toggle
  toggleBusinessFields() {
    // Implementation for toggling business fields
    this.showSuccessMessage('Champs commerciaux mis à jour');
  }

  // Password strength checker
  checkPasswordStrength() {
    // Implementation for checking password strength
    this.showSuccessMessage('Vérification de la force du mot de passe...');
  }

  // Authentication handlers
  handleLogin(event: Event) {
    event.preventDefault();
    // Implementation for login
    this.showSuccessMessage('Connexion en cours...');
  }

  handleRegister(event: Event) {
    event.preventDefault();
    // Implementation for registration
    this.showSuccessMessage('Inscription en cours...');
  }

  // Navigation functions
  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings') {
    this.currentPage = pageName;
  }

  // Dashboard functions
  showDashboard() {
    // Implementation for showing dashboard
  }

  updateUserDisplay() {
    // Implementation for updating user display
  }

  loadReceipts() {
    // Implementation for loading receipts
  }

  loadDashboardData() {
    // Implementation for loading dashboard data
  }

  // Utility functions
  logout() {
    this.currentUser = null;
    sessionStorage.removeItem('ticketscan_current_user');
    this.showSuccessMessage('Déconnexion réussie. À bientôt !');
  }

  toggleSidebar() {
    this.isSidebarCollapsed = !this.isSidebarCollapsed;
  }

  toggleUserMenu() {
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }

  toggleTheme() {
    this.isDarkTheme = !this.isDarkTheme;
    document.body.setAttribute('data-theme', this.isDarkTheme ? 'dark' : '');
  }

  // Receipt functions
  switchReceiptTab(tabName: string) {
    // Implementation for switching receipt tabs
  }

  filterReceipts() {
    // Implementation for filtering receipts
  }

  viewReceipt(id: number) {
    // Implementation for viewing receipt
    this.showSuccessMessage('Affichage du reçu...');
  }

  printReceipt(id: number) {
    // Implementation for printing receipt
    this.showSuccessMessage('Impression en cours...');
  }

  archiveReceipt(id: number) {
    // Implementation for archiving receipt
    this.showSuccessMessage('Reçu archivé avec succès !');
  }

  // Product functions
  showAddProductModal() {
    // Implementation for showing add product modal
    this.showSuccessMessage('Modal d\'ajout de produit...');
  }

  editProduct(id: number) {
    // Implementation for editing product
    this.showSuccessMessage('Édition du produit...');
  }

  archiveProduct(id: number) {
    // Implementation for archiving product
    this.showSuccessMessage('Produit archivé avec succès !');
  }

  restoreProduct(id: number) {
    // Implementation for restoring product
    this.showSuccessMessage('Produit restauré avec succès !');
  }

  deleteProduct(id: number) {
    // Implementation for deleting product
    this.showSuccessMessage('Produit supprimé avec succès !');
  }

  // Store functions
  showAddStoreModal() {
    // Implementation for showing add store modal
    this.showSuccessMessage('Modal d\'ajout de magasin...');
  }

  editStore(id: number) {
    // Implementation for editing store
    this.showSuccessMessage('Édition du magasin...');
  }

  archiveStore(id: number) {
    // Implementation for archiving store
    this.showSuccessMessage('Magasin archivé avec succès !');
  }

  restoreStore(id: number) {
    // Implementation for restoring store
    this.showSuccessMessage('Magasin restauré avec succès !');
  }

  deleteStore(id: number) {
    // Implementation for deleting store
    this.showSuccessMessage('Magasin supprimé avec succès !');
  }

  // Settings functions
  toggleSetting(settingName: string) {
    // Implementation for toggling settings
    this.showSuccessMessage(`Paramètre "${settingName}" modifié`);
  }

  exportAllData() {
    // Implementation for exporting all data
    this.showSuccessMessage('Export des données en cours...');
  }

  importData() {
    // Implementation for importing data
    this.showSuccessMessage('Import des données en cours...');
  }

  resetAllData() {
    // Implementation for resetting all data
    this.showSuccessMessage('Réinitialisation des données...');
  }

  // User profile functions
  showUserProfile() {
    // Implementation for showing user profile
    this.showSuccessMessage('Affichage du profil utilisateur...');
  }

  // Dashboard calculations
  calculateTotalSpent(): number {
    const allReceipts = [...this.sampleReceipts, ...this.manualReceipts];
    let total = 0;
    allReceipts.forEach(receipt => {
      const amount = parseInt(receipt.total.replace(/[^\d]/g, ''));
      total += amount;
    });
    return total;
  }

  calculateThisMonthSpent(): number {
    const allReceipts = [...this.sampleReceipts, ...this.manualReceipts];
    let total = 0;
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    allReceipts.forEach(receipt => {
      const receiptDate = new Date(receipt.date);
      if (receiptDate.getMonth() === currentMonth && receiptDate.getFullYear() === currentYear) {
        const amount = parseInt(receipt.total.replace(/[^\d]/g, ''));
        total += amount;
      }
    });
    return total;
  }

  calculateAverageReceiptAmount(): number {
    const allReceipts = [...this.sampleReceipts, ...this.manualReceipts];
    if (allReceipts.length === 0) return 0;
    
    const total = this.calculateTotalSpent();
    return Math.round(total / allReceipts.length);
  }

  // Utility functions
  showForgotPassword() {
    this.showSuccessMessage('Un email de réinitialisation sera envoyé à votre adresse (fonctionnalité en développement).');
  }

  exportData() {
    this.showSuccessMessage('Export des données en cours...');
  }

  // Notification system
  showSuccessMessage(message: string) {
    this.notification = { show: true, message, type: 'success' };
    setTimeout(() => {
      this.notification.show = false;
    }, 4000);
  }

  showErrorMessage(message: string) {
    this.notification = { show: true, message, type: 'error' };
    setTimeout(() => {
      this.notification.show = false;
    }, 4000);
  }
}
