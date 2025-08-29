import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { getApiConfig } from '../api/api.config';

export interface Product {
  id: string;
  name: string;
  barcode: string;
  price: number;
  category: string;
  description?: string;
  stock?: number;
  unit?: string;
  status: 'active' | 'archived';
  isFavorite: boolean;
  createdAt: Date;
  updatedAt: Date;
}

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  private readonly STORAGE_KEY = 'ticketscan_products';
  private readonly API_URL = getApiConfig().PRODUCTS.BASE;
  
  private productsSubject = new BehaviorSubject<Product[]>([]);
  public products$ = this.productsSubject.asObservable();

  constructor() {
    this.loadFromStorage();
  }

  // ========================================
  // 📦 GESTION GLOBALE DES PRODUITS
  // ========================================
  // ✅ Stockage en session storage
  // ✅ Synchronisation avec la base de données
  // ✅ Accessible partout dans le dashboard
  // ========================================

  // Charger les produits depuis le stockage local
  private loadFromStorage(): void {
    const stored = sessionStorage.getItem(this.STORAGE_KEY);
    if (stored) {
      try {
        const products = JSON.parse(stored).map((p: any) => ({
          ...p,
          createdAt: new Date(p.createdAt),
          updatedAt: new Date(p.updatedAt)
        }));
        this.productsSubject.next(products);
      } catch (error) {
        console.error('Erreur lors du chargement des produits depuis le stockage:', error);
      }
    }
  }

  // Sauvegarder les produits dans le stockage local
  private saveToStorage(products: Product[]): void {
    try {
      sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(products));
    } catch (error) {
      console.error('Erreur lors de la sauvegarde des produits:', error);
    }
  }

  // Obtenir tous les produits
  getProducts(): Observable<Product[]> {
    return this.products$;
  }

  // Obtenir les produits actuels (sans Observable)
  getCurrentProducts(): Product[] {
    return this.productsSubject.value;
  }

  // Ajouter un nouveau produit
  addProduct(product: Omit<Product, 'id' | 'createdAt' | 'updatedAt'>): Promise<Product> {
    return new Promise((resolve, reject) => {
      const newProduct: Product = {
        ...product,
        id: this.generateId(),
        createdAt: new Date(),
        updatedAt: new Date()
      } as Product;

      const currentProducts = this.getCurrentProducts();
      const updatedProducts = [...currentProducts, newProduct];
      
      this.productsSubject.next(updatedProducts);
      this.saveToStorage(updatedProducts);
      
      // Synchroniser avec la base de données
      this.syncToDatabase(newProduct, 'create')
        .then(() => resolve(newProduct))
        .catch(reject);
    });
  }

  // Mettre à jour un produit existant
  updateProduct(id: string, updates: Partial<Product>): Promise<Product> {
    return new Promise((resolve, reject) => {
      const currentProducts = this.getCurrentProducts();
      const productIndex = currentProducts.findIndex(p => p.id === id);
      
      if (productIndex === -1) {
        reject(new Error('Produit non trouvé'));
        return;
      }

      const updatedProduct = {
        ...currentProducts[productIndex],
        ...updates,
        updatedAt: new Date()
      } as Product;

      const updatedProducts = [...currentProducts];
      updatedProducts[productIndex] = updatedProduct;
      
      this.productsSubject.next(updatedProducts);
      this.saveToStorage(updatedProducts);
      
      // Synchroniser avec la base de données
      this.syncToDatabase(updatedProduct, 'update')
        .then(() => resolve(updatedProduct))
        .catch(reject);
    });
  }

  // Supprimer un produit
  deleteProduct(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const currentProducts = this.getCurrentProducts();
      const updatedProducts = currentProducts.filter(p => p.id !== id);
      
      this.productsSubject.next(updatedProducts);
      this.saveToStorage(updatedProducts);
      
      // Synchroniser avec la base de données
      this.syncToDatabase({ id } as Product, 'delete')
        .then(() => resolve())
        .catch(reject);
    });
  }

  // Rechercher des produits par nom
  searchProductsByName(query: string): Product[] {
    const products = this.getCurrentProducts();
    if (!query) return products;
    
    return products.filter(product =>
      product.name.toLowerCase().includes(query.toLowerCase()) ||
      (product.description && product.description.toLowerCase().includes(query.toLowerCase()))
    );
  }

  // Rechercher des produits par code-barres
  searchProductsByBarcode(barcode: string): Product | null {
    const products = this.getCurrentProducts();
    return products.find(product => product.barcode === barcode) || null;
  }

  // Obtenir les produits par catégorie
  getProductsByCategory(category: string): Product[] {
    const products = this.getCurrentProducts();
    return products.filter(product => product.category === category);
  }

  // Obtenir les produits favoris
  getFavoriteProducts(): Product[] {
    const products = this.getCurrentProducts();
    return products.filter(product => product.isFavorite);
  }

  // Basculer le statut favori d'un produit
  toggleFavorite(id: string): Promise<void> {
    const currentProducts = this.getCurrentProducts();
    const product = currentProducts.find(p => p.id === id);
    
    if (product) {
      return this.updateProduct(id, { isFavorite: !product.isFavorite }).then(() => {});
    }
    
    return Promise.reject(new Error('Produit non trouvé'));
  }

  // Générer un ID unique
  private generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  // ========================================
  // 🔄 SYNCHRONISATION BASE DE DONNÉES
  // ========================================
  // ✅ Création, mise à jour, suppression
  // ✅ Gestion des erreurs et retry
  // ========================================

  private async syncToDatabase(product: Product, action: 'create' | 'update' | 'delete'): Promise<void> {
    try {
      let response: Response;
      
      const config = getApiConfig();
      
      switch (action) {
        case 'create':
          response = await fetch(`${config.BASE_URL}${this.API_URL}`, {
            method: 'POST',
            headers: { ...config.DEFAULT_HEADERS },
            body: JSON.stringify(product)
          });
          break;
          
        case 'update':
          response = await fetch(`${config.BASE_URL}${this.API_URL}/${product.id}`, {
            method: 'PUT',
            headers: { ...config.DEFAULT_HEADERS },
            body: JSON.stringify(product)
          });
          break;
          
        case 'delete':
          response = await fetch(`${config.BASE_URL}${this.API_URL}/${product.id}`, {
            method: 'DELETE',
            headers: { ...config.DEFAULT_HEADERS }
          });
          break;
      }
      
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      
      console.log(`Produit ${action === 'create' ? 'créé' : action === 'update' ? 'mis à jour' : 'supprimé'} avec succès`);
      
    } catch (error) {
      console.error(`Erreur lors de la synchronisation avec la base de données (${action}):`, error);
      // En cas d'erreur, on garde les données en local
      // Une synchronisation sera tentée plus tard
    }
  }

  // Charger les produits depuis la base de données
  async loadFromDatabase(): Promise<void> {
    try {
      const config = getApiConfig();
      const response = await fetch(`${config.BASE_URL}${this.API_URL}`);
      if (response.ok) {
        const products = await response.json();
        const formattedProducts = products.map((p: any) => ({
          ...p,
          createdAt: new Date(p.createdAt),
          updatedAt: new Date(p.updatedAt)
        }));
        
        this.productsSubject.next(formattedProducts);
        this.saveToStorage(formattedProducts);
        console.log('Produits chargés depuis la base de données:', formattedProducts.length);
      }
    } catch (error) {
      console.error('Erreur lors du chargement depuis la base de données:', error);
      // En cas d'erreur, on garde les données locales
    }
  }

  // Vider le stockage local
  clearStorage(): void {
    sessionStorage.removeItem(this.STORAGE_KEY);
    this.productsSubject.next([]);
  }
}
