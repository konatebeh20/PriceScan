import { Component, OnInit } from '@angular/core';
import { ProductService, Product, PriceComparison, SearchFilters } from '../../services/product.service';
import { StorageService } from '../../services/storage.service';
import { ReceiptService } from '../../services/receipt.service';
import { LoadingController, ToastController, AlertController } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-price-comparison',
  templateUrl: './price-comparison.component.html',
  styleUrls: ['./price-comparison.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ]
})
export class PriceComparisonComponent implements OnInit {
  // État de l'application
  currentProduct: Product | null = null;
  favorites: string[] = [];
  priceAlerts: any[] = [];
  darkMode = false;
  
  // Données des produits
  products: Product[] = [];
  searchResults: Product[] = [];
  popularProducts: Product[] = [];
  
  // Filtres de recherche
  searchFilters: SearchFilters = {};
  
  // Navigation
  currentPage = 'home-page';
  
  // Recherche
  searchQuery = '';
  
  // Utilisateur
  userId = 'user123'; // À remplacer par l'ID utilisateur réel

  constructor(
    private productService: ProductService,
    private storageService: StorageService,
    private receiptService: ReceiptService,
    private loadingController: LoadingController,
    private toastController: ToastController,
    private alertController: AlertController
  ) {}

  ngOnInit() {
    this.initializeApp();
  }

  async initializeApp() {
    // Charger les préférences utilisateur
    await this.loadUserPreferences();
    
    // Charger les produits populaires
    await this.loadPopularProducts();
    
    // Charger les favoris
    await this.loadFavorites();
    
    // Charger les alertes de prix
    await this.loadPriceAlerts();
  }

  // Charger les préférences utilisateur
  async loadUserPreferences() {
    try {
      const settings = await this.storageService.getUserSettings();
      this.darkMode = settings.darkMode || false;
      this.applyTheme();
    } catch (error) {
      console.error('Erreur lors du chargement des préférences:', error);
    }
  }

  // Charger les produits populaires
  async loadPopularProducts() {
    try {
      const loading = await this.loadingController.create({
        message: 'Chargement des produits populaires...'
      });
      await loading.present();

      this.productService.getPopularProducts(8).subscribe({
        next: (products) => {
          this.popularProducts = products;
          this.products = products; // Pour la compatibilité avec le code existant
        },
        error: (error) => {
          console.error('Erreur lors du chargement des produits populaires:', error);
          this.showToast('Erreur lors du chargement des produits', 'danger');
        },
        complete: () => {
          loading.dismiss();
        }
      });
    } catch (error) {
      console.error('Erreur lors du chargement des produits populaires:', error);
    }
  }

  // Charger les favoris
  async loadFavorites() {
    try {
      this.favorites = await this.storageService.getFavorites();
    } catch (error) {
      console.error('Erreur lors du chargement des favoris:', error);
    }
  }

  // Charger les alertes de prix
  async loadPriceAlerts() {
    try {
      this.priceAlerts = await this.storageService.getPriceAlerts();
    } catch (error) {
      console.error('Erreur lors du chargement des alertes:', error);
    }
  }

  // Navigation entre les pages
  navigateTo(pageId: string) {
    this.currentPage = pageId;
    
    // Charger les données spécifiques à la page
    if (pageId === 'favorites-page') {
      this.loadFavoritesPage();
    } else if (pageId === 'home-page') {
      this.loadPopularProducts();
    }
  }

  // Charger la page des favoris
  async loadFavoritesPage() {
    try {
      const favoriteProducts: Product[] = [];
      
      for (const productId of this.favorites) {
        const product = await this.storageService.getProductById(productId);
        if (product) {
          favoriteProducts.push(product);
        }
      }
      
      this.products = favoriteProducts;
    } catch (error) {
      console.error('Erreur lors du chargement des favoris:', error);
    }
  }

  // Effectuer une recherche
  async performSearch(query: string) {
    if (!query.trim()) return;
    
    this.navigateTo('search-page');
    
    try {
      const loading = await this.loadingController.create({
        message: 'Recherche en cours...'
      });
      await loading.present();

      this.productService.searchProducts(query, this.searchFilters).subscribe({
        next: (results) => {
          this.searchResults = results;
          this.products = results;
        },
        error: (error) => {
          console.error('Erreur lors de la recherche:', error);
          this.showToast('Erreur lors de la recherche', 'danger');
        },
        complete: () => {
          loading.dismiss();
        }
      });
    } catch (error) {
      console.error('Erreur lors de la recherche:', error);
    }
  }

  // Afficher les détails d'un produit
  async showProductDetail(product: Product) {
    this.currentProduct = product;
    this.navigateTo('detail-page');
    
    // Charger la comparaison de prix
    await this.loadPriceComparison(product.id!);
  }

  // Charger la comparaison de prix
  async loadPriceComparison(productId: string) {
    try {
      const loading = await this.loadingController.create({
        message: 'Chargement des prix...'
      });
      await loading.present();

      this.productService.getPriceComparison(productId).subscribe({
        next: (comparison) => {
          // Traiter la comparaison de prix
          console.log('Comparaison de prix:', comparison);
        },
        error: (error) => {
          console.error('Erreur lors du chargement des prix:', error);
        },
        complete: () => {
          loading.dismiss();
        }
      });
    } catch (error) {
      console.error('Erreur lors du chargement des prix:', error);
    }
  }

  // Basculer le statut favori
  async toggleFavorite(event: Event, productId: string) {
    event.stopPropagation();
    
    try {
      const isFavorite = this.favorites.includes(productId);
      
      if (isFavorite) {
        await this.storageService.removeFromFavorites(productId);
        this.favorites = this.favorites.filter(id => id !== productId);
      } else {
        await this.storageService.addToFavorites(productId);
        this.favorites.push(productId);
      }
      
      // Mettre à jour l'interface
      this.updateFavoriteUI(productId, !isFavorite);
      
      // Synchroniser avec le serveur
      if (isFavorite) {
        this.productService.removeFromFavorites(productId, this.userId).subscribe();
      } else {
        this.productService.addToFavorites(productId, this.userId).subscribe();
      }
    } catch (error) {
      console.error('Erreur lors de la modification des favoris:', error);
      this.showToast('Erreur lors de la modification des favoris', 'danger');
    }
  }

  // Mettre à jour l'interface des favoris
  updateFavoriteUI(productId: string, isFavorite: boolean) {
    const heartIcons = document.querySelectorAll(`[data-product-id="${productId}"] .product-favorite`);
    heartIcons.forEach(icon => {
      if (isFavorite) {
        icon.classList.add('active');
      } else {
        icon.classList.remove('active');
      }
    });
  }

  // Définir une alerte de prix
  async setPriceAlert(productId: string) {
    const alert = await this.alertController.create({
      header: 'Alerte de Prix',
      inputs: [
        {
          name: 'targetPrice',
          type: 'number',
          placeholder: 'Prix cible',
          min: 0
        }
      ],
      buttons: [
        {
          text: 'Annuler',
          role: 'cancel'
        },
        {
          text: 'Définir',
          handler: (data) => {
            if (data.targetPrice && data.targetPrice > 0) {
              this.createPriceAlert(productId, parseFloat(data.targetPrice));
            }
          }
        }
      ]
    });
    
    await alert.present();
  }

  // Créer une alerte de prix
  async createPriceAlert(productId: string, targetPrice: number) {
    try {
      const alert = {
        id: Date.now().toString(),
        productId,
        userId: this.userId,
        targetPrice,
        createdAt: new Date().toISOString()
      };
      
      // Sauvegarder localement
      await this.storageService.savePriceAlert(alert);
      this.priceAlerts.push(alert);
      
      // Sauvegarder sur le serveur
      this.productService.setPriceAlert(productId, this.userId, targetPrice).subscribe();
      
      this.showToast('Alerte de prix définie avec succès!', 'success');
    } catch (error) {
      console.error('Erreur lors de la création de l\'alerte:', error);
      this.showToast('Erreur lors de la création de l\'alerte', 'danger');
    }
  }

  // Simuler un scan de code-barres
  async simulateBarcodeScan() {
    if (this.popularProducts.length > 0) {
      const randomProduct = this.popularProducts[Math.floor(Math.random() * this.popularProducts.length)];
      this.showProductDetail(randomProduct);
    }
  }

  // Basculer le mode sombre
  async toggleDarkMode(enabled: boolean) {
    this.darkMode = enabled;
    
    try {
      await this.storageService.saveUserSettings({ darkMode: enabled });
      this.applyTheme();
    } catch (error) {
      console.error('Erreur lors de la sauvegarde des préférences:', error);
    }
  }

  // Appliquer le thème
  applyTheme() {
    if (this.darkMode) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  // Afficher un toast
  async showToast(message: string, color: string = 'primary') {
    const toast = await this.toastController.create({
      message,
      duration: 3000,
      color,
      position: 'bottom'
    });
    await toast.present();
  }

  // Retour à la page précédente
  goBack() {
    if (this.currentPage === 'detail-page') {
      this.navigateTo('home-page');
    } else if (this.currentPage === 'search-page') {
      this.navigateTo('home-page');
    }
  }
}
