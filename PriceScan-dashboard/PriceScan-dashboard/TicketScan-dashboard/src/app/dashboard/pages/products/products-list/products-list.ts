import { Component, Output, EventEmitter, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

import { ProductsService } from '../../../services/products/products.service';
import { CategoriesService, Category } from '../../../services/categories/categories.service';
import { StoresService, Store } from '../../../services/stores/stores.service';

interface Product {
  id: string;
  product_name: string;
  product_barcode?: string;
  product_description?: string;
  product_brand?: string;
  category_id: number;
  category_name: string;
  store_id?: number;
  price_amount: number;
  price_currency: string;
  product_image?: string;
  product_is_active: boolean;
  isFavorite?: boolean;
  createdAt?: Date;
  updatedAt?: Date;
}

@Component({
  selector: 'app-products-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './products-list.html',
  styleUrls: ['./products-list.scss']
})
export class ProductsListComponent implements OnInit, OnDestroy {
  @Output() pageChange = new EventEmitter<'dashboard' | 'receipts' | 'products' | 'stores' | 'settings'>();

  // Filter properties
  searchTerm: string = '';
  selectedCategory: string = '';
  selectedStatus: string = '';
  selectedPrice: string = '';
  selectedFavorite: string = '';

  // Modal properties
  showModal: boolean = false;
  isEditing: boolean = false;
  editingProduct: Product = this.getEmptyProduct();

  // Service subscriptions
  private productsSubscription?: Subscription;
  private categoriesSubscription?: Subscription;
  private storesSubscription?: Subscription;

  // Data from services
  products: Product[] = [];
  categories: Category[] = [];
  stores: Store[] = [];

  // Liste affichée avec filtres
  filteredProducts: Product[] = [];

  // Statistiques des filtres
  filteredStats: {
    total: number;
    active: number;
    archived: number;
    favorites: number;
    byCategory: { [key: string]: number };
    byPrice: { [key: string]: number };
    byStatus: { [key: string]: number };
  } = {
    total: 0,
    active: 0,
    archived: 0,
    favorites: 0,
    byCategory: {},
    byPrice: { '0-1000': 0, '1000-5000': 0, '5000+': 0 },
    byStatus: { 'active': 0, 'archived': 0 }
  };

  // Suggestion de catégorie
  suggestedCategory: string = '';

  // Propriétés pour la comparaison des prix
  priceComparisons: any[] = [];
  averagePriceDifference: number = 0;
  totalStoresInComparison: number = 0;
  productsWithPriceVariation: number = 0;

  // Nouvelles propriétés pour le filtrage et tri des comparaisons
  comparisonFilter: string = '';
  comparisonSort: string = 'name';
  filteredComparisons: any[] = [];

  // Prévisualiser l'image
  previewImage: string = '';

  constructor(
    private productsService: ProductsService,
    private categoriesService: CategoriesService,
    private storesService: StoresService
  ) {}

  ngOnInit() {
    this.loadProducts();
    this.loadCategories();
    this.loadStores();
  }

  ngOnDestroy() {
    if (this.productsSubscription) {
      this.productsSubscription.unsubscribe();
    }
    if (this.categoriesSubscription) {
      this.categoriesSubscription.unsubscribe();
    }
    if (this.storesSubscription) {
      this.storesSubscription.unsubscribe();
    }
  }

  // Computed properties
  get totalProducts(): number {
    return this.products.length;
  }

  get activeProducts(): number {
    return this.products.filter(p => p.product_is_active).length;
  }

  get archivedProducts(): number {
    return this.products.filter(p => !p.product_is_active).length;
  }

  get favoriteProducts(): number {
    return this.products.filter(p => p.isFavorite).length;
  }

  // ========================================
  // 📦 GESTION GLOBALE DES PRODUITS
  // ========================================
  //  Chargement depuis le service global
  //  Synchronisation en temps réel
  //  Accessible partout dans le dashboard
  // ========================================

  // Charger les produits depuis le service
  loadProducts(): void {
    this.productsSubscription = this.productsService.getProducts().subscribe(
      (productsAny: any[]) => {
        // Adapter l'id string (service) -> number (local)
        this.products = (productsAny || []).map(p => ({
          ...p,
          id: Number(p.id)
        })) as Product[];
        this.filterProducts();
        // Charger la comparaison des prix si les magasins sont déjà chargés
        if (this.stores.length > 0) {
          this.loadPriceComparison();
        }
        console.log('Produits chargés:', this.products.length);
      },
      error => {
        console.error('Erreur lors du chargement des produits:', error);
      }
    );
  }

  // Charger les catégories depuis le service
  loadCategories(): void {
    this.categoriesSubscription = this.categoriesService.getCategories().subscribe(
      (categories: Category[]) => {
        this.categories = categories;
        console.log('Catégories chargées:', this.categories.length);
      },
      error => {
        console.error('Erreur lors du chargement des catégories:', error);
      }
    );
  }

  // Charger les magasins depuis le service
  loadStores(): void {
    this.storesSubscription = this.storesService.getStores().subscribe(
      (stores: Store[]) => {
        this.stores = stores;
        console.log('Magasins chargés:', this.stores.length);
        // Charger la comparaison des prix après avoir chargé les magasins
        this.loadPriceComparison();
      },
      error => {
        console.error('Erreur lors du chargement des magasins:', error);
      }
    );
  }

  // Charger la comparaison des prix depuis la base de données
  loadPriceComparison(): void {
    if (this.products.length === 0 || this.stores.length === 0) {
      console.log('Données insuffisantes pour la comparaison des prix');
      return;
    }

    console.log('🔄 Chargement de la comparaison des prix depuis la BDD...');
    console.log(`📊 Produits disponibles: ${this.products.length}`);
    console.log(`🏪 Magasins disponibles: ${this.stores.length}`);

    this.priceComparisons = [];
    let totalDifference = 0;
    let productsWithVariation = 0;
    const uniqueStores = new Set<number>();
    const storeNames = new Map<number, string>();

    // Créer un mapping des noms de magasins
    this.stores.forEach(store => {
      if (store.id !== undefined) {
        storeNames.set(store.id as number, store.store_name);
      }
    });

    // Grouper les produits UNIQUEMENT par nom (pas par code-barres)
    const productGroups = this.groupProductsByNameOnly();

    console.log(`🔍 Groupes de produits trouvés: ${productGroups.length}`);

    // Traiter TOUS les groupes de produits
    productGroups.forEach((group: any) => {
      // Inclure tous les produits, même ceux d'un seul magasin
      const validProducts = group.products.filter((p: Product) => p.price_amount && p.price_amount > 0);
      
      if (validProducts.length > 0) {
        const prices = validProducts.map((p: Product) => p.price_amount);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const averagePrice = prices.reduce((sum: number, price: number) => sum + price, 0) / prices.length;
        const priceDifference = validProducts.length > 1 ? maxPrice - minPrice : 0;
        const priceDifferencePercentage = validProducts.length > 1 && minPrice > 0 ? (priceDifference / minPrice) * 100 : 0;

        // Collecter les informations des magasins depuis la BDD
        const storeInfo = validProducts.map((p: Product) => ({
          storeId: p.store_id,
          storeName: p.store_id ? storeNames.get(p.store_id) || 'Magasin inconnu' : 'Magasin inconnu',
          price: p.price_amount,
          lastUpdate: p.updatedAt
        }));

        // Ajouter les magasins uniques
        validProducts.forEach((p: Product) => {
          if (p.store_id !== undefined) uniqueStores.add(p.store_id);
        });

        // Créer l'objet de comparaison avec toutes les données de la BDD
        const comparison = {
          product: group.products[0],
          minPrice,
          maxPrice,
          averagePrice,
          priceDifference,
          priceDifferencePercentage,
          storesCount: validProducts.length,
          trend: this.calculateTrend(validProducts),
          storeDetails: storeInfo, // Détails complets des magasins
          category: group.products[0].category_name,
          brand: group.products[0].product_brand,
          barcode: group.products[0].product_barcode,
          hasVariation: validProducts.length > 1
        };

        this.priceComparisons.push(comparison);

        totalDifference += priceDifferencePercentage;
        productsWithVariation++;

        console.log(`✅ Produit comparé: ${comparison.product.product_name} - ${validProducts.length} magasins, écart: ${priceDifferencePercentage.toFixed(1)}%`);
      }
    });

    // Calculer les statistiques globales depuis les données de la BDD
    this.averagePriceDifference = productsWithVariation > 0 ? totalDifference / productsWithVariation : 0;
    this.totalStoresInComparison = uniqueStores.size;
    this.productsWithPriceVariation = productsWithVariation;

    console.log(`📈 Statistiques calculées depuis la BDD:`);
    console.log(`   - Produits avec variation: ${this.productsWithPriceVariation}`);
    console.log(`   - Magasins analysés: ${this.totalStoresInComparison}`);
    console.log(`   - Écart moyen: ${this.averagePriceDifference.toFixed(1)}%`);
    console.log(`   - Comparaisons générées: ${this.priceComparisons.length}`);

    // Appliquer les filtres et le tri après chargement
    this.filterComparisons();
    this.sortComparisons();
  }

  // Grouper les produits UNIQUEMENT par nom (pas par code-barres)
  private groupProductsByNameOnly(): any[] {
    const groups: { [key: string]: any } = {};

    this.products.forEach(product => {
      const productName = product.product_name.toLowerCase().trim();
      if (!groups[productName]) {
        groups[productName] = {
          key: productName,
          products: []
        };
      }
      groups[productName].products.push(product);
    });

    return Object.values(groups);
  }

  // Grouper les produits par nom et code-barres
  private groupProductsByNameAndBarcode(): any[] {
    const groups: { [key: string]: any } = {};

    this.products.forEach(product => {
      const key = `${product.product_name}_${product.product_barcode || 'no_barcode'}`;
      if (!groups[key]) {
        groups[key] = {
          key,
          products: []
        };
      }
      groups[key].products.push(product);
    });

    return Object.values(groups);
  }

  // Calculer la tendance des prix
  private calculateTrend(products: Product[]): 'up' | 'down' | 'stable' {
    if (products.length < 2) return 'stable';

    const sortedProducts = products.sort((a, b) => {
      const dateA = a.updatedAt ? new Date(a.updatedAt) : new Date();
      const dateB = b.updatedAt ? new Date(b.updatedAt) : new Date();
      return dateA.getTime() - dateB.getTime();
    });

    const firstPrice = sortedProducts[0].price_amount;
    const lastPrice = sortedProducts[sortedProducts.length - 1].price_amount;

    if (lastPrice > firstPrice * 1.05) return 'up';
    if (lastPrice < firstPrice * 0.95) return 'down';
    return 'stable';
  }

  // Actualiser la comparaison des prix
  refreshPriceComparison(): void {
    this.loadPriceComparison();
  }

  // Obtenir l'icône de tendance
  getTrendIcon(trend: 'up' | 'down' | 'stable'): string {
    switch (trend) {
      case 'up': return 'fa-arrow-up';
      case 'down': return 'fa-arrow-down';
      default: return 'fa-minus';
    }
  }

  // Obtenir le texte de tendance
  getTrendText(trend: 'up' | 'down' | 'stable'): string {
    switch (trend) {
      case 'up': return 'Hausse';
      case 'down': return 'Baisse';
      default: return 'Stable';
    }
  }

  // Afficher les détails des magasins pour une comparaison
  showStoreDetails(comparison: any): void {
    if (!comparison.storeDetails || comparison.storeDetails.length === 0) {
      alert('Aucun détail de magasin disponible');
      return;
    }

    let detailsMessage = `Détails des prix pour: ${comparison.product.product_name}\n\n`;
    
    comparison.storeDetails.forEach((store: any, index: number) => {
      detailsMessage += `${index + 1}. ${store.storeName}\n`;
      detailsMessage += `   Prix: ${store.price.toLocaleString()} F CFA\n`;
      if (store.lastUpdate) {
        const updateDate = new Date(store.lastUpdate);
        detailsMessage += `   Dernière mise à jour: ${updateDate.toLocaleDateString()}\n`;
      }
      detailsMessage += '\n';
    });

    detailsMessage += `Écart total: ${comparison.priceDifference.toLocaleString()} F CFA (${comparison.priceDifferencePercentage.toFixed(1)}%)`;
    
    alert(detailsMessage);
  }

  // Filtrer les comparaisons
  filterComparisons(): void {
    if (!this.comparisonFilter || this.comparisonFilter === 'all') {
      this.filteredComparisons = [...this.priceComparisons];
    } else if (this.comparisonFilter === 'variation') {
      this.filteredComparisons = this.priceComparisons.filter(comparison => comparison.hasVariation);
    } else if (this.comparisonFilter === 'unique') {
      this.filteredComparisons = this.priceComparisons.filter(comparison => !comparison.hasVariation);
    }
  }

  // Trier les comparaisons
  sortComparisons(): void {
    switch (this.comparisonSort) {
      case 'name':
        this.filteredComparisons.sort((a, b) => a.product.product_name.localeCompare(b.product.product_name));
        break;
      case 'price':
        this.filteredComparisons.sort((a, b) => b.averagePrice - a.averagePrice);
        break;
      case 'variation':
        this.filteredComparisons.sort((a, b) => b.priceDifferencePercentage - a.priceDifferencePercentage);
        break;
      case 'stores':
        this.filteredComparisons.sort((a, b) => b.storesCount - a.storesCount);
        break;
      default:
        this.filteredComparisons.sort((a, b) => a.product.product_name.localeCompare(b.product.product_name));
    }
  }

  // Filter functions
  filterProducts() {
    this.filteredProducts = this.products.filter(product => {
      // Search term filter
      if (this.searchTerm && !product.product_name.toLowerCase().includes(this.searchTerm.toLowerCase()) && 
          !(product.product_description && product.product_description.toLowerCase().includes(this.searchTerm.toLowerCase()))) {
        return false;
      }

      // Category filter
      if (this.selectedCategory && product.category_name !== this.selectedCategory) {
        return false;
      }

      // Status filter
      if (this.selectedStatus && (this.selectedStatus === 'active' ? product.product_is_active : !product.product_is_active)) {
        return false;
      }

      // Price filter
      if (this.selectedPrice && product.price_amount) {
        switch (this.selectedPrice) {
          case '0-1000':
            if (product.price_amount >= 1000) return false;
            break;
          case '1000-5000':
            if (product.price_amount < 1000 || product.price_amount > 5000) return false;
            break;
          case '5000+':
            if (product.price_amount <= 5000) return false;
            break;
        }
      }

      // Favorite filter
      if (this.selectedFavorite) {
        if (this.selectedFavorite === 'favorite' && !product.isFavorite) return false;
        if (this.selectedFavorite === 'not-favorite' && product.isFavorite) return false;
      }

      return true;
    });

    // Mettre à jour les statistiques après filtrage
    this.updateFilterStats();
  }

  // Mettre à jour les statistiques des filtres
  updateFilterStats(): void {
    // Statistiques des produits filtrés
    this.filteredStats = {
      total: this.filteredProducts.length,
      active: this.filteredProducts.filter(p => p.product_is_active).length,
      archived: this.filteredProducts.filter(p => !p.product_is_active).length,
      favorites: this.filteredProducts.filter(p => p.isFavorite).length,
      byCategory: this.getCategoryStats(),
      byPrice: this.getPriceStats(),
      byStatus: this.getStatusStats()
    };
  }

  // Obtenir les statistiques par catégorie
  getCategoryStats(): { [key: string]: number } {
    const stats: { [key: string]: number } = {};
    this.filteredProducts.forEach(product => {
      const category = product.category_name;
      stats[category] = (stats[category] || 0) + 1;
    });
    return stats;
  }

  // Obtenir les statistiques par prix
  getPriceStats(): { [key: string]: number } {
    const stats = { '0-1000': 0, '1000-5000': 0, '5000+': 0 };
    this.filteredProducts.forEach(product => {
      const price = product.price_amount;
      if (price < 1000) stats['0-1000']++;
      else if (price <= 5000) stats['1000-5000']++;
      else stats['5000+']++;
    });
    return stats;
  }

  // Obtenir les statistiques par statut
  getStatusStats(): { [key: string]: number } {
    const stats = { 'active': 0, 'archived': 0 };
    this.filteredProducts.forEach(product => {
      if (product.product_is_active) stats['active']++;
      else stats['archived']++;
    });
    return stats;
  }

  // Recherche intelligente avec suggestions
  onSearchChange(): void {
    if (this.searchTerm && this.searchTerm.length > 0) {
      // Recherche en temps réel
      this.filterProducts();
      
      // Si un nom de produit est saisi, suggérer la catégorie
      this.suggestCategoryFromName();
    } else {
      // Réinitialiser les filtres si la recherche est vide
      this.resetFilters();
    }
  }

  // Suggérer automatiquement la catégorie basée sur le nom du produit
  suggestCategoryFromName(): void {
    if (!this.searchTerm) return;

    const searchLower = this.searchTerm.toLowerCase();
    
    // Mots-clés pour chaque catégorie
    const categoryKeywords: { [key: string]: string[] } = {
      'alimentaire': ['pain', 'lait', 'viande', 'poisson', 'légume', 'fruit', 'céréale', 'boisson', 'yaourt', 'fromage'],
      'hygiene': ['savon', 'shampooing', 'dentifrice', 'gel', 'crème', 'parfum', 'déodorant', 'papier', 'serviette'],
      'maison': ['nettoyant', 'détergent', 'éponge', 'balai', 'aspirateur', 'meuble', 'décoration', 'éclairage'],
      'sante': ['médicament', 'vitamine', 'complément', 'sirop', 'gélule', 'pansement', 'thermomètre'],
      'electronique': ['téléphone', 'ordinateur', 'écran', 'câble', 'chargeur', 'casque', 'haut-parleur'],
      'vetements': ['t-shirt', 'pantalon', 'robe', 'chaussure', 'sac', 'accessoire', 'bijou']
    };

    // Trouver la catégorie la plus probable
    let bestMatch = '';
    let bestScore = 0;

    for (const [category, keywords] of Object.entries(categoryKeywords)) {
      let score = 0;
      keywords.forEach(keyword => {
        if (searchLower.includes(keyword)) {
          score += keyword.length; // Plus le mot-clé est long, plus il est pertinent
        }
      });
      
      if (score > bestScore) {
        bestScore = score;
        bestMatch = category;
      }
    }

    // Si une catégorie est trouvée, la suggérer
    if (bestMatch && bestScore > 0) {
      this.suggestedCategory = bestMatch;
      console.log(`💡 Catégorie suggérée: ${bestMatch} pour "${this.searchTerm}"`);
    }
  }

  // Appliquer automatiquement la catégorie suggérée
  applySuggestedCategory(): void {
    if (this.suggestedCategory) {
      this.selectedCategory = this.suggestedCategory;
      this.filterProducts();
      this.suggestedCategory = ''; // Réinitialiser la suggestion
    }
  }

  // Vérifier s'il y a des filtres actifs
  hasActiveFilters(): boolean {
    return !!(this.searchTerm || this.selectedCategory || this.selectedStatus || 
             this.selectedPrice || this.selectedFavorite);
  }

  // Obtenir le libellé du prix
  getPriceLabel(priceRange: string): string {
    const labels: { [key: string]: string } = {
      '0-1000': '0 - 1000 F CFA',
      '1000-5000': '1000 - 5000 F CFA',
      '5000+': 'Plus de 5000 F CFA'
    };
    return labels[priceRange] || priceRange;
  }

  // Category functions
  getCategoryIcon(category: string): string {
    const icons: { [key: string]: string } = {
      'alimentaire': 'fa-utensils',
      'hygiene': 'fa-soap',
      'maison': 'fa-home',
      'sante': 'fa-heartbeat',
      'autre': 'fa-box'
    };
    return icons[category?.toLowerCase()] || 'fa-box';
  }

  getCategoryLabel(category: string): string {
    const labels: { [key: string]: string } = {
      'alimentaire': 'Alimentaire',
      'hygiene': 'Hygiène',
      'maison': 'Maison',
      'sante': 'Santé',
      'autre': 'Autre'
    };
    return labels[category?.toLowerCase()] || category;
  }

  getStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      'active': 'Actif',
      'archived': 'Archivé'
    };
    return labels[status] || status;
  }

  // Modal functions
  showAddProductModal() {
    this.isEditing = false;
    this.editingProduct = this.getEmptyProduct();
    this.showModal = true;
  }

  openAddModal() {
    this.showAddProductModal();
  }

  editProduct(product: Product) {
    this.isEditing = true;
    this.editingProduct = { ...product };
    this.showModal = true;
  }

  openEditModal(product: Product) {
    this.editProduct(product);
  }

  closeModal() {
    this.showModal = false;
    this.editingProduct = this.getEmptyProduct();
  }

  // Réinitialiser les filtres
  resetFilters(): void {
    this.searchTerm = '';
    this.selectedCategory = '';
    this.selectedStatus = '';
    this.selectedPrice = '';
    this.selectedFavorite = '';
    this.suggestedCategory = '';
    this.filteredProducts = [...this.products];
    this.updateFilterStats();
  }

  saveProduct() {
    if (this.isEditing) {
      this.productsService.updateProduct(this.editingProduct.id.toString(), this.editingProduct as any)
        .then(() => {
          this.closeModal();
          alert('Produit modifié avec succès !');
        })
        .catch((error: any) => {
          console.error('Erreur lors de la mise à jour:', error);
          alert('Erreur lors de la modification du produit');
        });
    } else {
      // Préparer les données pour l'API en respectant la nomenclature de la base
      const productData = {
        product_name: this.editingProduct.product_name,
        product_barcode: this.editingProduct.product_barcode,
        product_description: this.editingProduct.product_description,
        product_brand: this.editingProduct.product_brand,
        category_id: this.editingProduct.category_id,
        store_id: this.editingProduct.store_id || 1, // Utiliser le magasin sélectionné ou le premier par défaut
        price_amount: this.editingProduct.price_amount,
        price_currency: this.editingProduct.price_currency,
        product_image: this.editingProduct.product_image
      };
      
      this.productsService.addProduct(productData)
        .then(() => {
          this.closeModal();
          alert('Produit ajouté avec succès !');
        })
        .catch((error: any) => {
          console.error('Erreur lors de l\'ajout:', error);
          alert('Erreur lors de l\'ajout du produit');
        });
    }
  }

  getEmptyProduct(): Product {
    return {
      id: '0', // ID temporaire, sera généré par le backend
      product_name: '',
      product_barcode: '',
      product_description: '',
      product_brand: '',
      category_id: 1, // Default category
      category_name: '',
      store_id: 1, // Default store
      price_amount: 0,
      price_currency: 'CFA',
      product_image: '',
      product_is_active: true,
      isFavorite: false,
      createdAt: new Date(),
      updatedAt: new Date()
    };
  }

  // Product actions
  toggleFavorite(product: Product) {
    this.productsService.toggleFavorite(product.id.toString())
      .then(() => {
        // Mettre à jour le statut local
        if (product) {
          product.isFavorite = !product.isFavorite;
          // Rafraîchir la liste des produits
          this.loadProducts();
          console.log('Statut favori mis à jour:', product.isFavorite ? 'Ajouté aux favoris' : 'Retiré des favoris');
        }
      })
      .catch((error: any) => {
        console.error('Erreur lors du changement de favori:', error);
        alert('Erreur lors du changement de favori');
      });
  }

  // ========================================
  // 🖼️ GESTION DES IMAGES DE PRODUITS
  // ========================================
  //  Plusieurs options : PC local, réseau, en ligne
  //  Validation des formats
  //  Prévisualisation
  // ========================================

  // Ouvrir le sélecteur d'images
  openImageSelector(): void {
    // Créer un input file caché
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.style.display = 'none';
    
    fileInput.onchange = (event: any) => {
      const file = event.target.files[0];
      if (file) {
        this.handleLocalImage(file);
      }
    };
    
    document.body.appendChild(fileInput);
    fileInput.click();
    document.body.removeChild(fileInput);
  }

  // Gérer l'image locale
  handleLocalImage(file: File): void {
    if (file.size > 5 * 1024 * 1024) { // 5MB max
      alert('L\'image est trop volumineuse. Taille maximum : 5MB');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e: any) => {
      if (this.editingProduct && e.target?.result) {
        this.editingProduct.product_image = e.target.result;
        this.previewImage = e.target.result;
      }
    };
    reader.readAsDataURL(file);
  }

  // Ouvrir le sélecteur d'image réseau
  openNetworkImageSelector(): void {
    const networkPath = prompt('Entrez le chemin de l\'image réseau (ex: \\\\serveur\\images\\produit.jpg)');
    if (networkPath) {
      this.editingProduct.product_image = networkPath;
      this.previewImage = networkPath;
    }
  }

  // Ouvrir le sélecteur d'URL en ligne
  openOnlineImageSelector(): void {
    const imageUrl = prompt('Entrez l\'URL de l\'image en ligne');
    if (imageUrl) {
      // Valider l'URL
      if (this.isValidImageUrl(imageUrl)) {
        this.editingProduct.product_image = imageUrl;
        this.previewImage = imageUrl;
      } else {
        alert('URL d\'image invalide. Assurez-vous que l\'URL se termine par une extension d\'image valide (.jpg, .png, .gif, .webp)');
      }
    }
  }

  // Valider l'URL d'image
  isValidImageUrl(url: string): boolean {
    const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'];
    const lowerUrl = url.toLowerCase();
    return validExtensions.some(ext => lowerUrl.endsWith(ext));
  }

  // Supprimer l'image
  removeImage(): void {
    this.editingProduct.product_image = '';
    this.previewImage = '';
  }

  // Obtenir l'image d'affichage
  getDisplayImage(product: Product): string {
    if (product.product_image) {
      // Si c'est une image locale (base64)
      if (product.product_image.startsWith('data:image')) {
        return product.product_image;
      }
      // Si c'est une URL en ligne
      if (product.product_image.startsWith('http')) {
        return product.product_image;
      }
      // Si c'est un chemin réseau, essayer de le charger
      return product.product_image;
    }
    // Image par défaut
    return 'assets/img/products/product6.png';
  }

  // Gérer les erreurs de chargement d'images
  onImageError(event: any): void {
    if (event.target) {
      event.target.src = 'assets/img/products/product6.png';
    }
  }

  archiveProduct(product: Product) {
    if (confirm(`Voulez-vous archiver le produit "${product.product_name}" ?`)) {
      this.productsService.updateProduct(product.id.toString(), { product_is_active: false } as any)
        .then(() => {
          alert('Produit archivé avec succès !');
        })
        .catch((error: any) => {
          console.error('Erreur lors de l\'archivage:', error);
          alert('Erreur lors de l\'archivage du produit');
        });
    }
  }

  restoreProduct(product: Product) {
    if (confirm(`Voulez-vous restaurer le produit "${product.product_name}" ?`)) {
      this.productsService.updateProduct(product.id.toString(), { product_is_active: true } as any)
        .then(() => {
          alert('Produit restauré avec succès !');
        })
        .catch((error: any) => {
          console.error('Erreur lors de la restauration:', error);
          alert('Erreur lors de la restauration du produit');
        });
    }
  }

  deleteProduct(product: Product) {
    if (confirm(`Voulez-vous supprimer définitivement le produit "${product.product_name}" ?`)) {
      this.productsService.deleteProduct(product.id.toString())
        .then(() => {
          // Rafraîchir la liste des produits
          this.loadProducts();
          console.log('Produit supprimé avec succès:', product.product_name);
        })
        .catch((error: any) => {
          console.error('Erreur lors de la suppression:', error);
          alert('Erreur lors de la suppression du produit');
        });
    }
  }

  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings') {
    this.pageChange.emit(pageName);
  }
}
