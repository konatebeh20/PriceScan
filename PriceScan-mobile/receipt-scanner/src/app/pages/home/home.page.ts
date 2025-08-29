import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { 
  IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, 
  IonCardTitle, IonCardContent, IonButton, IonIcon,
  IonGrid, IonRow, IonCol, IonBadge, IonSearchbar
} from '@ionic/angular/standalone';
import { FavoritesService } from '../../services/favorites.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, IonHeader, IonToolbar, IonTitle, IonContent,
    IonCard, IonCardHeader, IonCardTitle, IonCardContent,
    IonButton, IonIcon, IonGrid, IonRow, IonCol, IonBadge, IonSearchbar
  ]
})
export class HomePage implements OnInit, OnDestroy {
  searchQuery = '';
  featuredProducts = [
    {
      id: 1,
      name: 'iPhone 15 Pro',
      currentPrice: 850000,
      oldPrice: 920000,
      store: 'Jumia CI',
      discount: 8,
      trend: 'down',
      image: 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop'
    },
    {
      id: 2,
      name: 'Samsung Galaxy S24',
      currentPrice: 720000,
      oldPrice: 780000,
      store: 'Prosuma',
      discount: 8,
      trend: 'down',
      image: 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400&h=400&fit=crop'
    },
    {
      id: 3,
      name: 'MacBook Air M2',
      currentPrice: 1250000,
      oldPrice: 1350000,
      store: 'Place',
      discount: 7,
      trend: 'down',
      image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop'
    },
    {
      id: 4,
      name: 'AirPods Pro 2',
      currentPrice: 180000,
      oldPrice: 200000,
      store: 'Jumia CI',
      discount: 10,
      trend: 'down',
      image: 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=400&fit=crop'
    }
  ];

  priceAlerts = [
    { product: 'MacBook Air', price: 1250000, store: 'Place' },
    { product: 'AirPods Pro', price: 180000, store: 'Jumia CI' }
  ];

  private favoriteIds: number[] = [];
  private subscription = new Subscription();

  constructor(
    private router: Router,
    private favoritesService: FavoritesService
  ) {}

  ngOnInit() {
    // S'abonner aux changements de favoris
    this.subscription.add(
      this.favoritesService.favorites$.subscribe(favorites => {
        this.favoriteIds = favorites;
      })
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  onSearch(event: any) {
    this.searchQuery = event.detail.value;
    // Implement search functionality
  }

  shareDeal(product: any) {
    // Implement social sharing
    console.log('Sharing deal:', product);
  }

  setPriceAlert(product: any) {
    // Placeholder for nicely formatted alert creation UI
    alert(`Alerte de prix créée pour ${product.name}`);
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('fr-CI', {
      style: 'currency',
      currency: 'XOF',
      minimumFractionDigits: 0
    }).format(price);
  }

  isFavorite(product: any): boolean {
    return this.favoriteIds.includes(product.id);
  }

  toggleFavorite(product: any) {
    if (this.isFavorite(product)) {
      this.favoritesService.removeFromFavorites(product.id);
      this.favoritesService.removeFromHistoryFavorites(product.id);
    } else {
      this.favoritesService.addToFavorites(product.id);
      this.favoritesService.addToHistoryFavorites(product);
    }
  }

  navigateToScan() {
    this.router.navigate(['/tabs/scan']);
  }

  navigateToCompare() {
    this.router.navigate(['/tabs/compare']);
  }
}
