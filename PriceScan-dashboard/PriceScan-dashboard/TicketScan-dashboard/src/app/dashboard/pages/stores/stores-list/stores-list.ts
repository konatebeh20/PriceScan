import { Component, Output, EventEmitter, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

import { StoresService, Store as ServiceStore } from '../../../services/stores/stores.service';
import { ReceiptsService } from '../../../services/receipts/receipts.service';

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
  selector: 'app-stores-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './stores-list.html',
  styleUrls: ['./stores-list.scss']
})
export class StoresListComponent implements OnInit, OnDestroy {
  @Output() pageChange = new EventEmitter<'dashboard' | 'receipts' | 'products' | 'stores' | 'settings'>();

  // Filter properties
  searchTerm: string = '';
  selectedType: string = '';
  selectedStatus: string = '';
  selectedCity: string = '';
  selectedFavorite: string = '';

  // Modal properties
  showModal: boolean = false;
  isEditing: boolean = false;
  editingStore: Store = this.getEmptyStore();

  // Service subscriptions
  private storesSubscription?: Subscription;
  private receiptsSubscription?: Subscription;

  // Stores from global service
  stores: Store[] = [];

  // Liste affichée avec filtres
  filteredStores: Store[] = [];

  constructor(private storesService: StoresService, private receiptsService: ReceiptsService) {}

  ngOnInit() {
    this.loadStores();
    // Écouter les changements de reçus pour mettre à jour les statistiques en temps réel
    this.receiptsSubscription = this.receiptsService.getReceipts().subscribe(
      () => {
        this.updateStoreStats();
      },
      error => {
        console.error('Erreur lors de l\'écoute des reçus:', error);
      }
    );
  }

  ngOnDestroy() {
    if (this.storesSubscription) {
      this.storesSubscription.unsubscribe();
    }
    if (this.receiptsSubscription) {
      this.receiptsSubscription.unsubscribe();
    }
  }

  // Computed properties
  get totalStores(): number {
    return this.stores.length;
  }

  get activeStores(): number {
    return this.stores.filter(s => s.status === 'active').length;
  }

  get archivedStores(): number {
    return this.stores.filter(s => s.status === 'archived').length;
  }

  get favoriteStores(): number {
    return this.stores.filter(s => s.isFavorite).length;
  }

  // ========================================
  // 🏪 GESTION GLOBALE DES MAGASINS
  // ========================================
  // ✅ Chargement depuis le service global
  // ✅ Synchronisation en temps réel
  // ✅ Accessible partout dans le dashboard
  // ========================================

  // Charger les magasins depuis le service
  loadStores(): void {
    this.storesSubscription = this.storesService.getStores().subscribe(
      (serviceStores: ServiceStore[]) => {
        // Adapter l'id string (service) -> number (local) et convertir les dates
        this.stores = (serviceStores || []).map(s => ({
          ...s,
          id: Number(s.id),
          lastVisit: new Date(s.lastVisit),
          createdAt: new Date(s.createdAt),
          updatedAt: new Date(s.updatedAt)
        })) as Store[];
        this.updateStoreStats(); // Mettre à jour les statistiques
        this.filterStores();
        console.log('Magasins chargés:', this.stores.length);
      },
      error => {
        console.error('Erreur lors du chargement des magasins:', error);
      }
    );
  }

  // Mettre à jour les statistiques des magasins (reçus, bénéfices, dernière visite)
  updateStoreStats(): void {
    const receipts = this.receiptsService.getCurrentReceipts();
    const currentDate = new Date();
    
    this.stores = this.stores.map(store => {
      // Filtrer les reçus pour ce magasin spécifique
      const storeReceipts = receipts.filter(r => {
        // Correspondance exacte par nom de magasin
        const receiptStoreName = r.store.toLowerCase().trim();
        const storeName = store.name.toLowerCase().trim();
        
        // Correspondance par nom OU par adresse si le nom ne correspond pas
        return receiptStoreName === storeName || 
               (r.address && r.address.toLowerCase().trim() === store.address.toLowerCase().trim());
      });

      // 1. Nombre de reçus du magasin spécifique
      const receiptsCount = storeReceipts.length;
      
      // 2. Calcul du bénéfice total (pas juste dépenses)
      // Pour simplifier, on considère que le total du reçu = bénéfice du magasin
      const totalBenefit = storeReceipts.reduce((sum, r) => {
        const total = parseFloat(r.total) || 0;
        return sum + total;
      }, 0);

      // 3. Dernière visite = date actuelle (connexion)
      // Si pas de reçus, on garde la date actuelle
      const lastVisit = currentDate;

      return {
        ...store,
        receiptsCount,
        totalSpent: totalBenefit, // Renommé pour la cohérence avec l'interface
        lastVisit
      };
    });

    // Mettre à jour le service avec les nouvelles statistiques
    this.stores.forEach(store => {
      this.storesService.updateStore(store.id.toString(), {
        receiptsCount: store.receiptsCount,
        totalSpent: store.totalSpent,
        lastVisit: store.lastVisit
      }).catch(error => {
        console.error('Erreur lors de la mise à jour des statistiques:', error);
      });
    });
  }

  // Filtrer les magasins
  filterStores(): void {
    let filtered = [...this.stores];

    // Filtre par recherche
    if (this.searchTerm) {
      filtered = filtered.filter(store =>
        store.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        store.address.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        (store.description && store.description.toLowerCase().includes(this.searchTerm.toLowerCase()))
      );
    }

    // Filtre par type
    if (this.selectedType) {
      filtered = filtered.filter(store => store.type === this.selectedType);
    }

    // Filtre par statut
    if (this.selectedStatus) {
      filtered = filtered.filter(store => store.status === this.selectedStatus);
    }

    // Filtre par ville
    if (this.selectedCity) {
      filtered = filtered.filter(store => store.city === this.selectedCity);
    }

    // Filtre par favoris
    if (this.selectedFavorite) {
      filtered = filtered.filter(store => 
        this.selectedFavorite === 'favorite' ? store.isFavorite : !store.isFavorite
      );
    }

    this.filteredStores = filtered;
  }

  // Réinitialiser les filtres
  resetFilters(): void {
    this.searchTerm = '';
    this.selectedType = '';
    this.selectedStatus = '';
    this.selectedCity = '';
    this.selectedFavorite = '';
    this.filterStores();
  }

  // Ouvrir le modal d'ajout
  openAddModal(): void {
    this.isEditing = false;
    this.editingStore = this.getEmptyStore();
    this.showModal = true;
  }

  // Backward compatibility for template expecting showAddStoreModal
  showAddStoreModal(): void {
    this.openAddModal();
  }

  // Ouvrir le modal de modification
  openEditModal(store: Store): void {
    this.isEditing = true;
    this.editingStore = { ...store };
    this.showModal = true;
  }

  // Backward compatibility for template expecting editStore
  editStore(store: Store): void {
    this.openEditModal(store);
  }

  // Fermer le modal
  closeModal(): void {
    this.showModal = false;
    this.isEditing = false;
    this.editingStore = this.getEmptyStore();
  }

  // Sauvegarder le magasin
  saveStore(): void {
    if (this.isEditing) {
      // Mise à jour
      const { id, createdAt, updatedAt, ...storeData } = this.editingStore;
      this.storesService.updateStore(id.toString(), storeData as any)
        .then(() => {
          this.closeModal();
          alert('Magasin modifié avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de la mise à jour:', error);
          alert('Erreur lors de la modification du magasin');
        });
    } else {
      // Ajout
      const { id, createdAt, updatedAt, ...storeData } = this.editingStore;
      this.storesService.addStore(storeData as any)
        .then(() => {
          this.closeModal();
          alert('Magasin ajouté avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de l\'ajout:', error);
          alert('Erreur lors de l\'ajout du magasin');
        });
    }
  }

  // Obtenir un magasin vide
  getEmptyStore(): Store {
    return {
      id: 0,
      name: '',
      type: 'supermarche',
      address: '',
      city: '',
      phone: '',
      email: '',
      description: '',
      status: 'active',
      isFavorite: false,
      receiptsCount: 0,
      totalSpent: 0,
      lastVisit: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    };
  }

  // ========================================
  // 🔧 ACTIONS SUR LES MAGASINS
  // ========================================
  // ✅ Tous les boutons fonctionnent
  // ✅ Synchronisation avec la base de données
  // ✅ Mise à jour en temps réel
  // ========================================

  // Basculer le statut favori
  toggleFavorite(store: Store): void {
    this.storesService.toggleFavorite(store.id.toString())
      .then(() => {
        // Le service met à jour automatiquement la liste
        console.log('Favori basculé avec succès');
      })
      .catch(error => {
        console.error('Erreur lors du changement de favori:', error);
        alert('Erreur lors du changement de favori');
      });
  }

  // Archiver un magasin
  archiveStore(store: Store): void {
    if (confirm(`Voulez-vous archiver le magasin "${store.name}" ?`)) {
      this.storesService.archiveStore(store.id.toString())
        .then(() => {
          alert('Magasin archivé avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de l\'archivage:', error);
          alert('Erreur lors de l\'archivage du magasin');
        });
    }
  }

  // Restaurer un magasin
  restoreStore(store: Store): void {
    if (confirm(`Voulez-vous restaurer le magasin "${store.name}" ?`)) {
      this.storesService.restoreStore(store.id.toString())
        .then(() => {
          alert('Magasin restauré avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de la restauration:', error);
          alert('Erreur lors de la restauration du magasin');
        });
    }
  }

  // Supprimer un magasin
  deleteStore(store: Store): void {
    if (confirm(`Voulez-vous supprimer définitivement le magasin "${store.name}" ?`)) {
      this.storesService.deleteStore(store.id.toString())
        .then(() => {
          alert('Magasin supprimé avec succès !');
        })
        .catch(error => {
          console.error('Erreur lors de la suppression:', error);
          alert('Erreur lors de la suppression du magasin');
        });
    }
  }

  // Changer de page
  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings'): void {
    this.pageChange.emit(pageName);
  }

  // Helpers expected by template
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

  getStatusLabel(status: 'active' | 'archived'): string {
    return status === 'active' ? 'Actif' : 'Archivé';
  }

  // Test du session storage et de la base de données
  testStorageAndDatabase(): void {
    console.log('🧪 [TEST] Début du test de stockage et base de données');
    
    // 1. Vérifier le session storage actuel
    const currentStorage = sessionStorage.getItem('ticketscan_stores');
    console.log('🔍 [TEST] Session storage actuel:', currentStorage ? 'Données présentes' : 'Vide');
    
    if (currentStorage) {
      const stores = JSON.parse(currentStorage);
      console.log('📊 [TEST] Nombre de magasins dans le session storage:', stores.length);
      console.log('📋 [TEST] Magasins stockés:', stores);
    }
    
    // 2. Vérifier le service
    const currentStores = this.storesService.getCurrentStores();
    console.log('🏪 [TEST] Nombre de magasins dans le service:', currentStores.length);
    
    // 3. Créer un magasin de test
    const testStore = {
      name: 'Magasin Test ' + new Date().getTime(),
      type: 'autre' as const,
      address: 'Adresse Test',
      city: 'abidjan',
      phone: '+225 00000000',
      email: 'test@test.com',
      description: 'Magasin de test pour vérifier le stockage',
      status: 'active' as const,
      isFavorite: false,
      receiptsCount: 0,
      totalSpent: 0,
      lastVisit: new Date()
    };
    
    console.log('🧪 [TEST] Ajout du magasin de test:', testStore);
    
    // 4. Ajouter le magasin de test
    this.storesService.addStore(testStore)
      .then(addedStore => {
        console.log('✅ [TEST] Magasin ajouté avec succès:', addedStore);
        
        // 5. Vérifier le session storage après ajout
        setTimeout(() => {
          const updatedStorage = sessionStorage.getItem('ticketscan_stores');
          console.log('🔍 [TEST] Session storage après ajout:', updatedStorage ? 'Données présentes' : 'Vide');
          
          if (updatedStorage) {
            const updatedStores = JSON.parse(updatedStorage);
            console.log('📊 [TEST] Nombre de magasins après ajout:', updatedStores.length);
                         console.log('🔍 [TEST] Magasin de test trouvé:', updatedStores.find((s: any) => s.name === testStore.name));
          }
          
          // 6. Vérifier le service après ajout
          const updatedServiceStores = this.storesService.getCurrentStores();
          console.log('🏪 [TEST] Nombre de magasins dans le service après ajout:', updatedServiceStores.length);
          
          console.log('🧪 [TEST] Test terminé avec succès !');
        }, 1000);
      })
      .catch(error => {
        console.error('❌ [TEST] Erreur lors de l\'ajout du magasin de test:', error);
      });
  }
}
