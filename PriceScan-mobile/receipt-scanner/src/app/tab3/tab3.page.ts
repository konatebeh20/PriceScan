import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
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
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule]
})
export class Tab3Page implements OnInit {
  favorites: Product[] = [];

  constructor(private router: Router) {}

  ngOnInit() {
    this.loadFavorites();
  }

  loadFavorites() {
    const stored = localStorage.getItem('favorites');
    if (stored) {
      const favoriteIds = JSON.parse(stored);
      // Load favorite products from mock data
      this.favorites = this.getFavoriteProducts(favoriteIds);
    }
  }

  getFavoriteProducts(favoriteIds: number[]): Product[] {
    // Mock product data
    const allProducts: Product[] = [
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
      },
      {
        id: 3,
        name: "4K Ultra HD Smart TV 55\"",
        price: 549.00,
        originalPrice: 699.99,
        description: "Immersive viewing experience with vibrant colors and smart features.",
        image: "tv",
        seller: "HomeTech",
        category: "TV & Video",
        rating: 4.7,
        reviews: 56,
        priceHistory: [699.99, 649.99, 599.99, 579.00, 549.00]
      },
      {
        id: 4,
        name: "Professional DSLR Camera",
        price: 899.00,
        originalPrice: 1099.99,
        description: "Capture stunning photos and videos with this professional-grade DSLR camera.",
        image: "camera",
        seller: "PhotoPro",
        category: "Cameras",
        rating: 4.8,
        reviews: 42,
        priceHistory: [1099.99, 999.99, 949.00, 919.00, 899.00]
      }
    ];

    return allProducts.filter(product => favoriteIds.includes(product.id));
  }

  showProductDetail(product: Product) {
    // Navigate to product detail or show modal
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

  removeFavorite(event: Event, productId: number) {
    event.stopPropagation();
    
    // Remove from favorites array
    this.favorites = this.favorites.filter(fav => fav.id !== productId);
    
    // Update localStorage
    const stored = localStorage.getItem('favorites');
    if (stored) {
      const favoriteIds = JSON.parse(stored);
      const updatedIds = favoriteIds.filter((id: number) => id !== productId);
      localStorage.setItem('favorites', JSON.stringify(updatedIds));
    }
  }
}
