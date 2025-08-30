import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductsService, Product } from '../../../services/products/products.service';

@Component({
  selector: 'app-products-archive',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './products-archive.html',
  styleUrls: ['./products-archive.scss']
})
export class ProductsArchiveComponent implements OnInit {
  archivedProducts: Product[] = [];
  filteredProducts: Product[] = [];
  searchTerm: string = '';
  selectedCategory: string = '';
  selectedStore: string = '';
  isLoading = false;

  constructor(private productsService: ProductsService) { }

  ngOnInit(): void {
    this.loadArchivedProducts();
  }

  loadArchivedProducts(): void {
    this.isLoading = true;
    this.productsService.getProducts().subscribe({
      next: (products) => {
        // Filter archived products using the correct property
        this.archivedProducts = products.filter(product => !product.product_is_active);
        this.filteredProducts = [...this.archivedProducts];
        this.isLoading = false;
        console.log('📦 Produits archivés chargés:', this.archivedProducts.length);
      },
      error: (error) => {
        console.error(' Erreur lors du chargement des produits archivés:', error);
        this.isLoading = false;
      }
    });
  }

  filterProducts(): void {
    if (!this.searchTerm && !this.selectedCategory && !this.selectedStore) {
      this.filteredProducts = [...this.archivedProducts];
      return;
    }

    this.filteredProducts = this.archivedProducts.filter(product => {
      const matchesSearch = !this.searchTerm || 
        product.product_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        (product.product_description && product.product_description.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
        (product.product_barcode && product.product_barcode.includes(this.searchTerm));

      const matchesCategory = !this.selectedCategory || 
        product.category_id.toString() === this.selectedCategory;

      const matchesStore = !this.selectedStore || 
        (product as any).store_id?.toString() === this.selectedStore;

      return matchesSearch && matchesCategory && matchesStore;
    });
  }

  resetFilters(): void {
    this.searchTerm = '';
    this.selectedCategory = '';
    this.selectedStore = '';
    this.filteredProducts = [...this.archivedProducts];
  }

  restoreProduct(product: Product): void {
    console.log('Produit restauré:', product.product_name);
    // TODO: Implement restore functionality
  }

  deletePermanently(product: Product): void {
    if (confirm(`Êtes-vous sûr de vouloir supprimer définitivement "${product.product_name}" ?`)) {
      this.productsService.deleteProduct(product.id).then((success: boolean) => {
        if (success) {
          // Remove from local arrays
          this.archivedProducts = this.archivedProducts.filter(p => p.id !== product.id);
          this.filteredProducts = this.filteredProducts.filter(p => p.id !== product.id);
          console.log(' Produit supprimé définitivement:', product.product_name);
        }
      }).catch((error: any) => {
        console.error(' Erreur lors de la suppression:', error);
        alert('Erreur lors de la suppression du produit');
      });
    }
  }

  viewProductDetails(product: Product): void {
    console.log('Voir détails du produit:', product.product_name);
  }

  getCategoryName(categoryId: number): string {
    return `Catégorie ${categoryId}`;
  }

  getStoreName(storeId: number | undefined): string {
    if (!storeId) return 'Magasin inconnu';
    return `Magasin ${storeId}`;
  }

  getPriceDisplay(product: Product): string {
    return `${product.price_amount} ${product.price_currency}`;
  }

  getArchiveDuration(product: Product): string {
    if (product.createdAt) {
      const now = new Date();
      const archiveDate = new Date(product.createdAt);
      const diffTime = Math.abs(now.getTime() - archiveDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) return '1 jour';
      if (diffDays < 7) return `${diffDays} jours`;
      if (diffDays < 30) return `${Math.ceil(diffDays / 7)} semaines`;
      return `${Math.ceil(diffDays / 30)} mois`;
    }
    return 'Date inconnue';
  }
}
