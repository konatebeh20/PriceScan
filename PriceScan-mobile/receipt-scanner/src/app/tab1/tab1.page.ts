import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';

interface Product {
  id: number;
  name: string;
  price: number;
  originalPrice: number;
  description: string;
  image: string;
  seller: string;
  category: string;
  rating: number;
  reviews: number;
  priceHistory: number[];
}

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class Tab1Page implements OnInit {
  searchQuery: string = '';
  popularProducts: Product[] = [];
  favorites: number[] = [];
  
  // Propriétés pour le comparateur de prix
  searchResults: any[] = [];
  selectedProduct: any = null;
  priceComparison: any = null;
  isLoading: boolean = false;
  errorMessage: string = '';
  recentSearches: string[] = [];
  cachedComparisons: Map<string, any> = new Map();

  constructor(
    private router: Router
  ) {}

  ngOnInit() {
    this.loadPopularProducts();
    this.loadFavorites();
    this.loadRecentSearches();
    this.loadCachedComparisons();
  }

  loadRecentSearches() {
    this.recentSearches = ['test1', 'test2', 'test3'];
  }

  loadCachedComparisons() {
    this.cachedComparisons = new Map();
  }

  saveRecentSearch(query: string) {
    if (!this.recentSearches.includes(query)) {
      this.recentSearches.unshift(query);
      this.recentSearches = this.recentSearches.slice(0, 10);
    }
  }

  saveCachedComparison(productId: string, comparison: any) {
    this.cachedComparisons.set(productId, comparison);
  }

  loadPopularProducts() {
    // Mock product data
    this.popularProducts = [
      {
        id: 1,
        name: "Wireless Bluetooth Headphones",
        price: 89.99,
        originalPrice: 129.99,
        description: "High-quality wireless headphones with noise cancellation and 20-hour battery life.",
        image: "headphones",
        seller: "ElectroShop",
        category: "Electronics",
        rating: 4.5,
        reviews: 124,
        priceHistory: [129.99, 119.99, 109.99, 99.99, 89.99]
      },
      {
        id: 2,
        name: "Smart Fitness Tracker Watch",
        price: 59.95,
        originalPrice: 79.99,
        description: "Track your steps, heart rate, sleep patterns, and receive smartphone notifications.",
        image: "watch",
        seller: "FitGear",
        category: "Wearables",
        rating: 4.3,
        reviews: 89,
        priceHistory: [79.99, 75.99, 69.99, 64.95, 59.95]
      }
    ];
  }

  loadFavorites() {
    this.favorites = [1, 3];
  }

  async performSearch(query: string) {
    if (!query.trim()) return;
    this.isLoading = true;
    this.errorMessage = '';
    this.searchResults = [];
    this.selectedProduct = null;
    this.priceComparison = null;
    
    try {
      this.saveRecentSearch(query);
      // Mock search results
      this.searchResults = [
        { id: '1', name: 'Test Product 1', price: 100 },
        { id: '2', name: 'Test Product 2', price: 200 }
      ];
    } catch (error) {
      this.errorMessage = 'Erreur lors de la recherche.';
      console.error('Erreur recherche:', error);
    } finally {
      this.isLoading = false;
    }
  }

  async comparePrices(product: any) {
    this.selectedProduct = product;
    this.isLoading = true;
    this.errorMessage = '';
    this.priceComparison = null;
    
    try {
      const cached = this.cachedComparisons.get(product.id);
      if (cached) {
        this.priceComparison = cached;
        return;
      }
      
      // Mock comparison data
      this.priceComparison = {
        product_id: product.id,
        comparison_data: [
          {
            store_info: { store_name: 'Store 1', store_city: 'Abidjan' },
            price_amount: 100,
            price_currency: 'XOF',
            price_is_promo: false
          },
          {
            store_info: { store_name: 'Store 2', store_city: 'Abidjan' },
            price_amount: 95,
            price_currency: 'XOF',
            price_is_promo: true
          }
        ],
        best_price: 95,
        best_store: 'Store 2',
        price_range: { min: 95, max: 100 },
        count: 2
      };
      
      this.saveCachedComparison(product.id, this.priceComparison);
    } catch (error) {
      this.errorMessage = 'Erreur lors de la comparaison des prix.';
      console.error('Erreur comparaison:', error);
    } finally {
      this.isLoading = false;
    }
  }

  getBestPrice(): any {
    if (!this.priceComparison || !this.priceComparison.comparison_data) return null;
    
    const prices = this.priceComparison.comparison_data;
    if (prices.length === 0) return null;

    return prices.reduce((min: any, current: any) => 
      current.price_amount < min.price_amount ? current : min
    );
  }

  getPriceRange(): { min: number; max: number } | null {
    if (!this.priceComparison || !this.priceComparison.comparison_data) return null;
    
    const prices = this.priceComparison.comparison_data;
    if (prices.length === 0) return null;

    const amounts = prices.map((p: any) => p.price_amount);
    return {
      min: Math.min(...amounts),
      max: Math.max(...amounts)
    };
  }

  calculateSavings(): { amount: number; percentage: number } | null {
    const range = this.getPriceRange();
    if (!range || range.max <= range.min) return null;

    const savings = range.max - range.min;
    const percentage = (savings / range.max) * 100;

    return { amount: savings, percentage: Math.round(percentage * 10) / 10 };
  }

  clearSearch() {
    this.searchQuery = '';
    this.searchResults = [];
    this.selectedProduct = null;
    this.priceComparison = null;
    this.errorMessage = '';
  }

  getProductImage(product: any): string {
    if (product.images && product.images.length > 0) {
      return product.images[0].url;
    }
    return 'assets/images/default-product.svg';
  }

  goToScan() {
    this.router.navigate(['/scan']);
  }

  showProductDetail(product: Product) {
    console.log('Showing product:', product);
  }

  getProductIcon(imageType: string): string {
    const iconMap: { [key: string]: string } = {
      'headphones': 'headset',
      'watch': 'time',
      'tv': 'tv',
      'camera': 'camera',
      'laptop': 'laptop',
      'phone': 'phone-portrait',
      'charger': 'battery-charging',
      'earbuds': 'ear'
    };
    return iconMap[imageType] || 'cube';
  }

  isFavorite(productId: number): boolean {
    return this.favorites.includes(productId);
  }
}
