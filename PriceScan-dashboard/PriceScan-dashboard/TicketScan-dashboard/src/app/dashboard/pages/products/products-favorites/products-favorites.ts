import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-products-favorites',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './products-favorites.html',
  styleUrls: ['./products-favorites.scss']
})
export class ProductsFavoritesComponent implements OnInit {
  
  // Products data
  favoriteProducts: any[] = [
    {
      id: 1,
      product_name: 'Produit Favori 1',
      product_description: 'Description du produit favori',
      product_barcode: '123456789',
      category_id: 1,
      store_id: 1,
      price_amount: 1500,
      product_unit: 'piece',
      product_image: '',
      isFavorite: true
    }
  ];
  filteredProducts: any[] = [...this.favoriteProducts];
  
  // Filter properties
  searchTerm: string = '';
  selectedCategory: string = '';
  selectedStore: string = '';
  
  // Loading state
  isLoading = false;

  constructor() { }

  ngOnInit(): void {
  }

  // Filter products
  filterProducts(): void {
    let filtered = [...this.favoriteProducts];

    // Search filter
    if (this.searchTerm) {
      const term = this.searchTerm.toLowerCase();
      filtered = filtered.filter(product =>
        product.product_name.toLowerCase().includes(term) ||
        product.product_description?.toLowerCase().includes(term) ||
        product.product_barcode?.toLowerCase().includes(term)
      );
    }

    // Category filter
    if (this.selectedCategory) {
      filtered = filtered.filter(product => 
        product.category_id === parseInt(this.selectedCategory)
      );
    }

    // Store filter
    if (this.selectedStore) {
      filtered = filtered.filter(product => 
        product.store_id === parseInt(this.selectedStore)
      );
    }

    this.filteredProducts = filtered;
  }

  // Reset filters
  resetFilters(): void {
    this.searchTerm = '';
    this.selectedCategory = '';
    this.selectedStore = '';
    this.filteredProducts = [...this.favoriteProducts];
  }

  // Remove from favorites
  removeFromFavorites(product: any): void {
    if (confirm(`Voulez-vous retirer "${product.product_name}" de vos favoris ?`)) {
      this.favoriteProducts = this.favoriteProducts.filter(p => p.id !== product.id);
      this.filteredProducts = this.filteredProducts.filter(p => p.id !== product.id);
      console.log(' Produit retiré des favoris:', product.product_name);
    }
  }

  // View product details
  viewProductDetails(product: any): void {
    console.log('Voir détails du produit:', product.product_name);
  }

  // Get category name
  getCategoryName(categoryId: number): string {
    const categories = {
      1: 'Alimentation',
      2: 'Électronique',
      3: 'Vêtements'
    };
    return categories[categoryId as keyof typeof categories] || `Catégorie ${categoryId}`;
  }

  // Get store name
  getStoreName(storeId: number): string {
    const stores = {
      1: 'Carrefour',
      2: 'Pharmacie',
      3: 'Boutique'
    };
    return stores[storeId as keyof typeof stores] || `Magasin ${storeId}`;
  }

  // Get price display
  getPriceDisplay(product: any): string {
    if (product.price_amount) {
      return `${product.price_amount} F CFA`;
    }
    return 'Prix non disponible';
  }
}
