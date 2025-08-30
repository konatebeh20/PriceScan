import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Store {
  id: number;
  name: string;
  type: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre';
  address: string;
  city: string;
  phone?: string;
  email?: string;
  description?: string;
  status: 'active' | 'archived';
  isFavorite: boolean;
  receiptsCount: number;
  totalSpent: number;
  lastVisit: Date;
  createdAt: Date;
  updatedAt: Date;
}

@Component({
  selector: 'app-stores-favorie',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stores-favorie.html',
  styleUrls: ['./stores-favorie.scss']
})
export class StoresFavorieComponent implements OnInit {
  
  // Stores favoris
  favoriteStores: Store[] = [];

  constructor() { }

  ngOnInit(): void {
    this.loadFavoriteStores();
  }

  // Charger les magasins favoris (simulation pour l'instant)
  loadFavoriteStores(): void {
    // Données de test - à remplacer par l'API
    this.favoriteStores = [
      {
        id: 2,
        name: 'Pharmacie du Plateau',
        type: 'pharmacie',
        address: '456 Boulevard Roume',
        city: 'Abidjan',
        phone: '+225 27222555',
        email: 'info@pharmacie-plateau.ci',
        description: 'Pharmacie de quartier',
        status: 'active',
        isFavorite: true,
        receiptsCount: 23,
        totalSpent: 450000,
        lastVisit: new Date(),
        createdAt: new Date('2024-02-01'),
        updatedAt: new Date()
      }
    ];
  }

  // Retirer des favoris
  removeFromFavorites(store: Store): void {
    if (confirm(`Voulez-vous retirer "${store.name}" de vos favoris ?`)) {
      store.isFavorite = false;
      this.favoriteStores = this.favoriteStores.filter(s => s.id !== store.id);
      // TODO: Synchroniser avec la BDD
      console.log('Retiré des favoris:', store.name);
    }
  }

  // Voir les détails du magasin
  viewStoreDetails(store: Store): void {
    // TODO: Naviguer vers la page de détails
    console.log('Voir détails:', store.name);
  }

  // Helpers
  getStoreTypeIcon(type: string): string {
    switch (type) {
      case 'supermarche': return 'fa-shopping-basket';
      case 'pharmacie': return 'fa-medkit';
      case 'quincaillerie': return 'fa-wrench';
      case 'particulier': return 'fa-user';
      default: return 'fa-store';
    }
  }

  getStoreTypeLabel(type: string): string {
    switch (type) {
      case 'supermarche': return 'Supermarché';
      case 'pharmacie': return 'Pharmacie';
      case 'quincaillerie': return 'Quincaillerie';
      case 'particulier': return 'Particulier';
      default: return 'Autre';
    }
  }
}
