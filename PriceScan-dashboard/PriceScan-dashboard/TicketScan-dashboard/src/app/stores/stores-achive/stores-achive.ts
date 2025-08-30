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
  selector: 'app-stores-achive',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stores-achive.html',
  styleUrls: ['./stores-achive.scss']
})
export class StoresAchiveComponent implements OnInit {
  
  // Stores archivés
  archivedStores: Store[] = [];

  constructor() { }

  ngOnInit(): void {
    this.loadArchivedStores();
  }

  // Charger les magasins archivés (simulation pour l'instant)
  loadArchivedStores(): void {
    // Données de test - à remplacer par l'API
    this.archivedStores = [
      {
        id: 4,
        name: 'Boutique Ancienne',
        type: 'autre',
        address: '321 Rue de l\'Ancien',
        city: 'Abidjan',
        phone: '+225 27222777',
        email: 'ancienne@boutique.ci',
        description: 'Boutique fermée',
        status: 'archived',
        isFavorite: false,
        receiptsCount: 8,
        totalSpent: 150000,
        lastVisit: new Date('2023-12-01'),
        createdAt: new Date('2023-01-01'),
        updatedAt: new Date('2023-12-01')
      }
    ];
  }

  // Restaurer un magasin
  restoreStore(store: Store): void {
    if (confirm(`Voulez-vous restaurer le magasin "${store.name}" ?`)) {
      store.status = 'active';
      this.archivedStores = this.archivedStores.filter(s => s.id !== store.id);
      // TODO: Synchroniser avec la BDD
      console.log('Magasin restauré:', store.name);
    }
  }

  // Supprimer définitivement un magasin
  deletePermanently(store: Store): void {
    if (confirm(`ATTENTION ! Voulez-vous supprimer définitivement le magasin "${store.name}" ?\n\nCette action est irréversible !`)) {
      this.archivedStores = this.archivedStores.filter(s => s.id !== store.id);
      // TODO: Synchroniser avec la BDD
      console.log('Magasin supprimé définitivement:', store.name);
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

  // Calculer la durée depuis l'archivage
  getArchiveDuration(store: Store): string {
    const archiveDate = store.updatedAt;
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - archiveDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return '1 jour';
    if (diffDays < 30) return `${diffDays} jours`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} mois`;
    return `${Math.floor(diffDays / 365)} an(s)`;
  }
}
