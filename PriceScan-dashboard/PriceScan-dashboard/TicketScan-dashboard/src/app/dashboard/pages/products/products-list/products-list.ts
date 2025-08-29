import { Component, Output, EventEmitter, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

import { ProductsService } from '../../../services/products/products.service';

interface Product {
  id: number;
  name: string;
  barcode?: string;
  description?: string;
  category: 'alimentaire' | 'hygiene' | 'maison' | 'sante' | 'autre';
  price?: number;
  unit?: string;
  status: 'active' | 'archived';
  isFavorite: boolean;
  createdAt: Date;
  updatedAt: Date;
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

  // Service subscription
  private productsSubscription?: Subscription;

  // Products from global service
  products: Product[] = [];

  // Liste affichée avec filtres
  filteredProducts: Product[] = [];

  constructor(private productsService: ProductsService) {}

  ngOnInit() {
    this.loadProducts();
  }

  ngOnDestroy() {
    if (this.productsSubscription) {
      this.productsSubscription.unsubscribe();
    }
  }

  // Computed properties
  get totalProducts(): number {
    return this.products.length;
  }

  get activeProducts(): number {
    return this.products.filter(p => p.status === 'active').length;
  }

  get archivedProducts(): number {
    return this.products.filter(p => p.status === 'archived').length;
  }

  get favoriteProducts(): number {
    return this.products.filter(p => p.isFavorite).length;
  }

  // ========================================
  // 📦 GESTION GLOBALE DES PRODUITS
  // ========================================
  // ✅ Chargement depuis le service global
  // ✅ Synchronisation en temps réel
  // ✅ Accessible partout dans le dashboard
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
        console.log('Produits chargés:', this.products.length);
      },
      error => {
        console.error('Erreur lors du chargement des produits:', error);
      }
    );
  }

  // Filter functions
  filterProducts() {
    this.filteredProducts = this.products.filter(product => {
      // Search term filter
      if (this.searchTerm && !product.name.toLowerCase().includes(this.searchTerm.toLowerCase()) && 
          !(product.description && product.description.toLowerCase().includes(this.searchTerm.toLowerCase()))) {
        return false;
      }

      // Category filter
      if (this.selectedCategory && product.category !== this.selectedCategory) {
        return false;
      }

      // Status filter
      if (this.selectedStatus && product.status !== this.selectedStatus) {
        return false;
      }

      // Price filter
      if (this.selectedPrice && product.price) {
        switch (this.selectedPrice) {
          case 'low':
            if (product.price < 1000) return false;
            break;
          case 'medium':
            if (product.price < 1000 || product.price > 5000) return false;
            break;
          case 'high':
            if (product.price <= 5000) return false;
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
    return icons[category] || 'fa-box';
  }

  getCategoryLabel(category: string): string {
    const labels: { [key: string]: string } = {
      'alimentaire': 'Alimentaire',
      'hygiene': 'Hygiène',
      'maison': 'Maison',
      'sante': 'Santé',
      'autre': 'Autre'
    };
    return labels[category] || category;
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
    this.filterProducts();
  }

  saveProduct() {
    if (this.isEditing) {
      this.productsService.updateProduct(this.editingProduct.id.toString(), this.editingProduct as any)
        .then(() => {
          this.closeModal();
          alert('Produit modifié avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de la mise à jour:', error);
          alert('Erreur lors de la modification du produit');
        });
    } else {
      const { id, createdAt, updatedAt, ...productData } = this.editingProduct as any;
      this.productsService.addProduct(productData)
        .then(() => {
          this.closeModal();
          alert('Produit ajouté avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de l\'ajout:', error);
          alert('Erreur lors de l\'ajout du produit');
        });
    }
  }

  getEmptyProduct(): Product {
    return {
      id: 0,
      name: '',
      barcode: '',
      description: '',
      category: 'alimentaire',
      price: 0,
      unit: 'pièce',
      status: 'active',
      isFavorite: false,
      createdAt: new Date(),
      updatedAt: new Date()
    };
  }

  // Product actions
  toggleFavorite(product: Product) {
    this.productsService.toggleFavorite(product.id.toString())
      .then(() => {
        alert(product.isFavorite ? 'Retiré des favoris !' : 'Ajouté aux favoris !');
      })
      .catch(error => {
        console.error('Erreur lors du changement de favori:', error);
        alert('Erreur lors du changement de favori');
      });
  }

  archiveProduct(product: Product) {
    if (confirm(`Voulez-vous archiver le produit "${product.name}" ?`)) {
      this.productsService.updateProduct(product.id.toString(), { status: 'archived' } as any)
        .then(() => {
          alert('Produit archivé avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de l\'archivage:', error);
          alert('Erreur lors de l\'archivage du produit');
        });
    }
  }

  restoreProduct(product: Product) {
    if (confirm(`Voulez-vous restaurer le produit "${product.name}" ?`)) {
      this.productsService.updateProduct(product.id.toString(), { status: 'active' } as any)
        .then(() => {
          alert('Produit restauré avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de la restauration:', error);
          alert('Erreur lors de la restauration du produit');
        });
    }
  }

  deleteProduct(product: Product) {
    if (confirm(`Voulez-vous supprimer définitivement le produit "${product.name}" ?`)) {
      this.productsService.deleteProduct(product.id.toString())
        .then(() => {
          alert('Produit supprimé avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de la suppression:', error);
          alert('Erreur lors de la suppression du produit');
        });
    }
  }

  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings') {
    this.pageChange.emit(pageName);
  }
}
