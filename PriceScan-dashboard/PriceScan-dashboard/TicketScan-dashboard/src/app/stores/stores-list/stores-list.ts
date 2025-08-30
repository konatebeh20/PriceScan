import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { StoresService, Store, StoreFormData } from '../services/stores.service';

@Component({
  selector: 'app-stores-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './stores-list.html',
  styleUrls: ['./stores-list.scss']
})
export class StoresListComponent implements OnInit, OnDestroy {
  
  // Stores data - Initialiser avec des tableaux vides
  stores: Store[] = [];
  filteredStores: Store[] = [];

  // Filter properties
  searchTerm: string = '';
  selectedStatus: string = '';
  selectedCity: string = '';

  // Form properties
  showAddForm: boolean = false;
  editingStore: Store | null = null;
  isSubmitting: boolean = false;

  // Form data
  storeForm: StoreFormData = {
    store_name: '',
    store_address: '',
    store_city: '',
    store_country: 'Côte d\'Ivoire',
    store_phone: '',
    store_email: '',
    store_website: ''
  };

  // Subscription management
  private storesSubscription: Subscription = new Subscription();

  constructor(private storesService: StoresService) { }

  ngOnInit(): void {
    console.log(' StoresListComponent initialisé');
    // Initialiser avec des tableaux vides
    this.stores = [];
    this.filteredStores = [];
    this.loadStores();
    this.subscribeToStores();
  }

  ngOnDestroy(): void {
    if (this.storesSubscription) {
      this.storesSubscription.unsubscribe();
    }
  }

  // Charger les magasins depuis le service
  loadStores(): void {
    console.log(' Chargement des magasins...');
    this.storesService.loadStores().subscribe({
      next: (stores: Store[]) => {
        console.log(' Magasins chargés:', stores);
        // S'assurer que stores est un tableau
        if (Array.isArray(stores)) {
          this.stores = stores;
          this.filteredStores = [...stores];
          console.log(' Magasins disponibles:', this.stores.length);
        } else {
          console.warn(' Les données reçues ne sont pas un tableau:', stores);
          this.stores = [];
          this.filteredStores = [];
        }
      },
      error: (error) => {
        console.error(' Erreur lors du chargement des magasins:', error);
        this.stores = [];
        this.filteredStores = [];
      }
    });
  }

  // S'abonner aux changements des magasins
  private subscribeToStores(): void {
    this.storesSubscription = this.storesService.stores$.subscribe((stores: Store[]) => {
      console.log(' Mise à jour des magasins via subscription:', stores);
      // S'assurer que stores est un tableau
      if (Array.isArray(stores)) {
        this.stores = stores;
        this.filteredStores = [...stores];
        console.log(' Magasins mis à jour:', this.stores.length);
      } else {
        console.warn(' Les données de subscription ne sont pas un tableau:', stores);
        this.stores = [];
        this.filteredStores = [];
      }
    });
  }

  // ========================================
  //  FILTRAGE ET RECHERCHE
  // ========================================

  // Filtrer les magasins
  filterStores(): void {
    if (!this.stores || this.stores.length === 0) {
      this.filteredStores = [];
      return;
    }

    let filtered = [...this.stores];

    // Filtre par recherche
    if (this.searchTerm) {
      filtered = filtered.filter(store => 
        store.store_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        store.store_city.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    }

    // Filtre par statut
    if (this.selectedStatus) {
      filtered = filtered.filter(store => store.store_status === this.selectedStatus);
    }

    // Filtre par ville
    if (this.selectedCity) {
      filtered = filtered.filter(store => store.store_city === this.selectedCity);
    }

    this.filteredStores = filtered;
  }

  // Réinitialiser les filtres
  resetFilters(): void {
    this.searchTerm = '';
    this.selectedStatus = '';
    this.selectedCity = '';
    this.filteredStores = [...this.stores];
  }

  // Obtenir les villes uniques pour le filtre
  getUniqueCities(): string[] {
    if (!this.stores || this.stores.length === 0) return [];
    const cities = this.stores.map(store => store.store_city).filter(city => city);
    return [...new Set(cities)].sort();
  }

  // Voir les détails d'un magasin
  viewStoreDetails(store: Store): void {
    console.log(' Voir les détails du magasin:', store);
    alert(`Détails du magasin: ${store.store_name}\nVille: ${store.store_city}\nAdresse: ${store.store_address}`);
  }

  // ========================================
  //  GESTION DU FORMULAIRE
  // ========================================

  // Afficher le formulaire d'ajout
  showAddStoreForm(): void {
    console.log(' showAddStoreForm() appelé');
    console.log('showAddForm avant:', this.showAddForm);
    this.showAddForm = true;
    this.editingStore = null;
    this.resetForm();
    console.log('showAddForm après:', this.showAddForm);
    console.log('storeForm:', this.storeForm);
  }

  // Afficher le formulaire de modification
  showEditStoreForm(store: Store): void {
    console.log('✏️ Modification du magasin:', store);
    this.showAddForm = true;
    this.editingStore = store;
    this.populateForm(store);
  }

  // Masquer le formulaire
  hideForm(): void {
    console.log(' Masquage du formulaire');
    this.showAddForm = false;
    this.editingStore = null;
    this.resetForm();
  }

  // Réinitialiser le formulaire
  private resetForm(): void {
    this.storeForm = {
      store_name: '',
      store_address: '',
      store_city: '',
      store_country: 'Côte d\'Ivoire',
      store_phone: '',
      store_email: '',
      store_website: ''
    };
  }

  // Remplir le formulaire avec les données existantes
  private populateForm(store: Store): void {
    this.storeForm = {
      store_name: store.store_name,
      store_address: store.store_address,
      store_city: store.store_city,
      store_country: store.store_country,
      store_phone: store.store_phone || '',
      store_email: store.store_email || '',
      store_website: store.store_website || ''
    };
  }

  // Soumettre le formulaire
  onSubmit(): void {
    if (this.isSubmitting) return;

    console.log('📤 Soumission du formulaire:', this.storeForm);
    this.isSubmitting = true;

    if (this.editingStore) {
      // Mise à jour
      console.log(' Mise à jour du magasin:', this.editingStore.id);
      this.storesService.updateStore(this.editingStore.id, this.storeForm).subscribe({
        next: (updatedStore) => {
          if (updatedStore) {
            console.log(' Magasin mis à jour:', updatedStore);
            this.hideForm();
            this.showSuccessMessage('Magasin mis à jour avec succès !');
            this.loadStores(); // Recharger la liste
          } else {
            this.showErrorMessage('Erreur lors de la mise à jour du magasin');
          }
        },
        error: (error) => {
          console.error(' Erreur lors de la mise à jour:', error);
          this.showErrorMessage('Erreur lors de la mise à jour du magasin');
        },
        complete: () => {
          this.isSubmitting = false;
        }
      });
    } else {
      // Création
      console.log(' Création d\'un nouveau magasin');
      this.storesService.createStore(this.storeForm).subscribe({
        next: (newStore) => {
          if (newStore) {
            console.log(' Nouveau magasin créé:', newStore);
            this.hideForm();
            this.showSuccessMessage('Magasin créé avec succès !');
            this.loadStores(); // Recharger la liste
          } else {
            this.showErrorMessage('Erreur lors de la création du magasin');
          }
        },
        error: (error) => {
          console.error(' Erreur lors de la création:', error);
          this.showErrorMessage('Erreur lors de la création du magasin');
        },
        complete: () => {
          this.isSubmitting = false;
        }
      });
    }
  }

  // ========================================
  // ⭐ ACTIONS SUR LES MAGASINS
  // ========================================

  // Basculer le statut favori
  toggleFavorite(store: Store): void {
    console.log('⭐ Basculement du favori pour:', store.store_name);
    this.storesService.toggleFavorite(store.id).subscribe({
      next: (success) => {
        if (success) {
          console.log(' Statut favori basculé pour:', store.store_name);
          this.loadStores(); // Recharger la liste
        } else {
          console.error(' Erreur lors du basculement du favori');
        }
      },
      error: (error) => {
        console.error(' Erreur lors du basculement du favori:', error);
      }
    });
  }

  // Archiver un magasin
  archiveStore(store: Store): void {
    if (confirm(`Voulez-vous archiver le magasin "${store.store_name}" ?`)) {
      console.log('📁 Archivage du magasin:', store.store_name);
      this.storesService.archiveStore(store.id).subscribe({
        next: (success) => {
          if (success) {
            console.log(' Magasin archivé:', store.store_name);
            this.showSuccessMessage('Magasin archivé avec succès !');
            this.loadStores(); // Recharger la liste
          } else {
            this.showErrorMessage('Erreur lors de l\'archivage du magasin');
          }
        },
        error: (error) => {
          console.error(' Erreur lors de l\'archivage:', error);
          this.showErrorMessage('Erreur lors de l\'archivage du magasin');
        }
      });
    }
  }

  // Supprimer un magasin
  deleteStore(store: Store): void {
    if (confirm(`Voulez-vous supprimer définitivement le magasin "${store.store_name}" ?\n\nCette action est irréversible !`)) {
      console.log('🗑️ Suppression du magasin:', store.store_name);
      this.storesService.deleteStore(store.id).subscribe({
        next: (success) => {
          if (success) {
            console.log(' Magasin supprimé:', store.store_name);
            this.showSuccessMessage('Magasin supprimé avec succès !');
            this.loadStores(); // Recharger la liste
          } else {
            this.showErrorMessage('Erreur lors de la suppression du magasin');
          }
        },
        error: (error) => {
          console.error(' Erreur lors de la suppression:', error);
          this.showErrorMessage('Erreur lors de la suppression du magasin');
        }
      });
    }
  }

  // ========================================
  //  CALCULS ET GETTERS
  // ========================================

  // Computed properties - Utiliser les données locales du composant
  get totalStores(): number {
    return this.stores?.length || 0;
  }

  get activeStores(): number {
    return this.stores?.filter(store => store.store_status === 'active').length || 0;
  }

  get favoriteStores(): number {
    return this.stores?.filter(store => store.is_favorite).length || 0;
  }

  // ========================================
  // 🎨 HELPERS
  // ========================================

  // Obtenir l'icône du statut
  getStatusIcon(status: string | undefined): string {
    if (!status) return 'fa-circle';
    return status === 'active' ? 'fa-check-circle' : 'fa-archive';
  }

  // Obtenir le label du statut
  getStatusLabel(status: string | undefined): string {
    if (!status) return 'Inconnu';
    return status === 'active' ? 'Actif' : 'Archivé';
  }

  // Obtenir l'icône du type de magasin (remplacé par une icône générique)
  getStoreTypeIcon(type: string | undefined): string {
    return 'fa-store'; // Icône générique pour tous les magasins
  }

  // Obtenir le label du type de magasin (remplacé par un label générique)
  getStoreTypeLabel(type: string | undefined): string {
    return 'Magasin'; // Label générique pour tous les magasins
  }

  // ========================================
  // 💬 MESSAGES UTILISATEUR
  // ========================================

  private showSuccessMessage(message: string): void {
    console.log('', message);
    // TODO: Implémenter un système de notification
    alert(message);
  }

  private showErrorMessage(message: string): void {
    console.error('', message);
    // TODO: Implémenter un système de notification
    alert(message);
  }
}
