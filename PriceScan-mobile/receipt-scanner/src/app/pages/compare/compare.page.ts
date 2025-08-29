import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon, IonGrid, IonRow, IonCol, IonBadge, IonSearchbar, IonCardSubtitle } from '@ionic/angular/standalone';

@Component({
  selector: 'app-compare',
  templateUrl: './compare.page.html',
  styleUrls: ['./compare.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, IonHeader, IonToolbar, IonTitle, IonContent,
    IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon,
    IonGrid, IonRow, IonCol, IonBadge, IonSearchbar, IonCardSubtitle
  ]
})
export class ComparePage {
  searchQuery = '';
  productsToCompare: any[] = [];
  comparisonResults: any[] = [];
  favorites: any[] = [];

  constructor() {}

  searchProducts() {
    if (this.searchQuery.trim()) {
      // Simuler la recherche de produits avec magasins ivoiriens
      const mockProducts = [
        {
          id: 1,
          name: this.searchQuery,
          price: 850000,
          store: 'Jumia CI',
          rating: 4.5,
          image: 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop'
        },
        {
          id: 2,
          name: this.searchQuery,
          price: 870000,
          store: 'Prosuma',
          rating: 4.2,
          image: 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400&h=400&fit=crop'
        },
        {
          id: 3,
          name: this.searchQuery,
          price: 890000,
          store: 'Place',
          rating: 4.0,
          image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop'
        },
        {
          id: 4,
          name: this.searchQuery,
          price: 920000,
          store: 'Carrefour CI',
          rating: 4.3,
          image: 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=400&fit=crop'
        }
      ];
      
      this.comparisonResults = mockProducts;
    }
  }

  addToComparison(product: any) {
    if (this.productsToCompare.length < 3) {
      this.productsToCompare.push(product);
    }
  }

  toggleFavorite(product: any) {
    const index = this.favorites.findIndex(f => f.id === product.id);
    if (index !== -1) {
      this.favorites.splice(index, 1);
    } else {
      this.favorites.push(product);
    }
  }

  isFavorite(product: any): boolean {
    return this.favorites.some(f => f.id === product.id);
  }

  removeFromComparison(index: number) {
    this.productsToCompare.splice(index, 1);
  }

  clearComparison() {
    this.productsToCompare = [];
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('fr-CI', {
      style: 'currency',
      currency: 'XOF',
      minimumFractionDigits: 0
    }).format(price);
  }
}
