import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { 
  IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, 
  IonCardTitle, IonCardContent, IonButton, IonIcon, IonList, IonItem,
  IonLabel, IonBadge, IonSegment, IonSegmentButton
} from '@ionic/angular/standalone';
import { FavoritesService, FavoriteProduct } from '../../services/favorites.service';

@Component({
  selector: 'app-history',
  templateUrl: './history.page.html',
  styleUrls: ['./history.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, IonHeader, IonToolbar, IonTitle, IonContent,
    IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon,
    IonList, IonItem, IonLabel, IonBadge, IonSegment, IonSegmentButton
  ]
})
export class HistoryPage implements OnInit, OnDestroy {
  selectedSegment = 'scans';
  scanHistory: any[] = [];
  priceHistory: any[] = [];
  searchHistory: any[] = [];
  favorites: FavoriteProduct[] = [];
  archives: any[] = [];
  private subscription = new Subscription();

  constructor(private favoritesService: FavoritesService) {}

  ngOnInit() {
    this.loadMockData();
    
    // S'abonner aux changements de favoris
    this.subscription.add(
      this.favoritesService.historyFavorites$.subscribe(favorites => {
        this.favorites = favorites;
      })
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  loadFavoritesFromStorage() {
    try {
      const storedFavorites = JSON.parse(localStorage.getItem('ps_history_favorites') || '[]');
      this.favorites = storedFavorites.map((fav: any) => ({
        ...fav,
        timestamp: new Date(fav.timestamp)
      }));
    } catch (error) {
      console.error('Erreur lors du chargement des favoris:', error);
    }
  }

  loadMockData() {
    // Historique des scans
    this.scanHistory = [
      {
        id: 1,
        product: 'iPhone 15 Pro',
        barcode: '1234567890123',
        timestamp: new Date('2024-01-15T10:30:00'),
        price: 850000,
        store: 'Jumia CI',
        isFavorite: false
      },
      {
        id: 2,
        product: 'Samsung Galaxy S24',
        barcode: '9876543210987',
        timestamp: new Date('2024-01-14T15:45:00'),
        price: 720000,
        store: 'Prosuma',
        isFavorite: false
      },
      {
        id: 3,
        product: 'MacBook Air M2',
        barcode: '4567891234567',
        timestamp: new Date('2024-01-13T09:20:00'),
        price: 1250000,
        store: 'Place',
        isFavorite: true
      }
    ];

    // Favoris
    this.favorites = [
      {
        id: 3,
        product: 'MacBook Air M2',
        barcode: '4567891234567',
        timestamp: new Date('2024-01-13T09:20:00').toISOString(),
        price: 1250000,
        store: 'Place',
        isFavorite: true
      }
    ];

    // Historique des prix
    this.priceHistory = [
      {
        id: 1,
        product: 'MacBook Air M2',
        priceChanges: [
          { date: new Date('2024-01-10'), price: 1350000, store: 'Place' },
          { date: new Date('2024-01-12'), price: 1300000, store: 'Place' },
          { date: new Date('2024-01-15'), price: 1250000, store: 'Place' }
        ],
        currentPrice: 1250000,
        bestPrice: 1250000,
        priceDrop: 100000
      },
      {
        id: 2,
        product: 'iPhone 15 Pro',
        priceChanges: [
          { date: new Date('2024-01-08'), price: 920000, store: 'Jumia CI' },
          { date: new Date('2024-01-12'), price: 880000, store: 'Jumia CI' },
          { date: new Date('2024-01-15'), price: 850000, store: 'Jumia CI' }
        ],
        currentPrice: 850000,
        bestPrice: 850000,
        priceDrop: 70000
      }
    ];

    // Historique des recherches
    this.searchHistory = [
      {
        id: 1,
        query: 'iPhone 15',
        timestamp: new Date('2024-01-15T09:00:00'),
        resultCount: 15
      },
      {
        id: 2,
        query: 'MacBook Pro',
        timestamp: new Date('2024-01-14T14:20:00'),
        resultCount: 8
      },
      {
        id: 3,
        query: 'Samsung Galaxy',
        timestamp: new Date('2024-01-13T11:30:00'),
        resultCount: 12
      }
    ];
  }

  segmentChanged(event: any) {
    this.selectedSegment = event.detail.value;
  }

  clearHistory(type: string) {
    switch(type) {
      case 'scans':
        // Déplacer vers les archives au lieu de supprimer
        this.archives.push(...this.scanHistory);
        this.scanHistory = [];
        break;
      case 'prices':
        this.archives.push(...this.priceHistory);
        this.priceHistory = [];
        break;
      case 'searches':
        this.archives.push(...this.searchHistory);
        this.searchHistory = [];
        break;
    }
  }

  toggleFavorite(item: any, type: string) {
    switch(type) {
      case 'scans':
        const scanIndex = this.scanHistory.findIndex(s => s.id === item.id);
        if (scanIndex !== -1) {
          this.scanHistory[scanIndex].isFavorite = !this.scanHistory[scanIndex].isFavorite;
          if (this.scanHistory[scanIndex].isFavorite) {
            this.favorites.push(this.scanHistory[scanIndex]);
          } else {
            this.favorites = this.favorites.filter(f => f.id !== item.id);
          }
        }
        break;
      case 'searches':
        const searchIndex = this.searchHistory.findIndex(s => s.id === item.id);
        if (searchIndex !== -1) {
          this.searchHistory[searchIndex].isFavorite = !this.searchHistory[searchIndex].isFavorite;
          if (this.searchHistory[searchIndex].isFavorite) {
            this.favorites.push(this.searchHistory[searchIndex]);
          } else {
            this.favorites = this.favorites.filter(f => f.id !== item.id);
          }
        }
        break;
    }
  }

  deleteItem(item: any, type: string) {
    switch(type) {
      case 'scans':
        const scanIndex = this.scanHistory.findIndex(s => s.id === item.id);
        if (scanIndex !== -1) {
          this.archives.push(this.scanHistory[scanIndex]);
          this.scanHistory.splice(scanIndex, 1);
        }
        break;
      case 'searches':
        const searchIndex = this.searchHistory.findIndex(s => s.id === item.id);
        if (searchIndex !== -1) {
          this.archives.push(this.searchHistory[searchIndex]);
          this.searchHistory.splice(searchIndex, 1);
        }
        break;
    }
  }

  removeFromFavorites(favorite: any) {
    // Utiliser le service pour retirer des favoris
    this.favoritesService.removeFromFavorites(favorite.id);
    this.favoritesService.removeFromHistoryFavorites(favorite.id);
  }
  

  deleteFavorite(favorite: any) {
    // Supprimer complètement le favori (déplacer vers les archives)
    this.archives.push({
      ...favorite,
      archivedAt: new Date().toISOString(),
      type: 'favorite'
    });
    
    // Retirer des favoris
    this.favoritesService.removeFromFavorites(favorite.id);
    this.favoritesService.removeFromHistoryFavorites(favorite.id);
  }

  getPriceTrend(priceChanges: any[]): string {
    if (priceChanges.length < 2) return 'stable';
    const first = priceChanges[0].price;
    const last = priceChanges[priceChanges.length - 1].price;
    return last < first ? 'down' : last > first ? 'up' : 'stable';
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('fr-CI', {
      style: 'currency',
      currency: 'XOF',
      minimumFractionDigits: 0
    }).format(price);
  }
}
