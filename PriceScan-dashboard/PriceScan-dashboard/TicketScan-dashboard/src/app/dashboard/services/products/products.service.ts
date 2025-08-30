import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { getApiConfig } from '../api/api.config';

export interface Product {
  product_status: string;
  id: string;
  product_name: string;
  product_barcode?: string;
  product_description?: string;
  product_brand?: string;
  category_id: number;
  category_name: string;
  store_id?: number;
  price_amount: number;
  price_currency: string;
  product_unit?: string;
  product_image?: string;
  product_is_active: boolean;
  isFavorite?: boolean;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface ProductFormData {
  product_name: string;
  product_barcode?: string;
  product_description?: string;
  product_brand?: string;
  category_id: number;
  store_id: number;
  price_amount: number;
  price_currency?: string;
  product_image?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  private readonly STORAGE_KEY = 'ticketscan_products';
  private readonly API_URL = getApiConfig().PRODUCTS.BASE;
  
  private productsSubject = new BehaviorSubject<Product[]>([]);
  public products$ = this.productsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadProductsFromAPI();
  }

  // ========================================
  // 📦 GESTION GLOBALE DES PRODUITS
  // ========================================
  //  Synchronisation avec l'API PriceScan
  //  Stockage en session storage pour performance
  //  Accessible partout dans le dashboard
  // ========================================

  // Charger les produits depuis l'API
  private loadProductsFromAPI(): void {
    this.http.get<any>(`${this.API_URL}`).subscribe({
      next: (response) => {
        if (response.response === 'success') {
          const products = response.products.map((p: any) => ({
            ...p,
            id: p.id.toString(),
            createdAt: p.creation_date ? new Date(p.creation_date) : new Date(),
            updatedAt: p.updated_on ? new Date(p.updated_on) : new Date()
          }));
          
          this.productsSubject.next(products);
          this.saveToStorage(products);
          console.log(' Produits chargés depuis l\'API:', products.length);
        } else {
          console.error(' Erreur API:', response.message);
        }
      },
      error: (error) => {
        console.error(' Erreur lors du chargement des produits:', error);
        // En cas d'erreur, charger depuis le stockage local
        this.loadFromStorage();
      }
    });
  }

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
        console.log('📦 Produits chargés depuis le stockage local:', products.length);
      } catch (error) {
        console.error(' Erreur lors du chargement des produits depuis le stockage:', error);
      }
    }
  }

  // Sauvegarder les produits dans le stockage local
  private saveToStorage(products: Product[]): void {
    try {
      sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(products));
    } catch (error) {
      console.error(' Erreur lors de la sauvegarde des produits:', error);
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
  addProduct(productData: ProductFormData): Promise<Product> {
    return new Promise((resolve, reject) => {
      this.http.post<any>(`${this.API_URL}`, productData).subscribe({
        next: (response) => {
          if (response.response === 'success') {
            const newProduct: Product = {
              ...response.product,
              id: response.product.id.toString(),
              createdAt: new Date(),
              updatedAt: new Date()
            };

            const currentProducts = this.getCurrentProducts();
            const updatedProducts = [...currentProducts, newProduct];
            
            this.productsSubject.next(updatedProducts);
            this.saveToStorage(updatedProducts);
            
            console.log(' Produit ajouté avec succès:', newProduct);
            resolve(newProduct);
          } else {
            reject(new Error(response.message || 'Erreur lors de l\'ajout du produit'));
          }
        },
        error: (error) => {
          console.error(' Erreur lors de l\'ajout du produit:', error);
          reject(error);
        }
      });
    });
  }

  // Mettre à jour un produit
  updateProduct(productId: string, updates: Partial<Product>): Promise<Product> {
    return new Promise((resolve, reject) => {
      this.http.put<any>(`${this.API_URL}/${productId}`, updates).subscribe({
        next: (response) => {
          if (response.response === 'success') {
            const updatedProduct: Product = {
              ...response.product,
              id: response.product.id.toString(),
              updatedAt: new Date()
            };

            const currentProducts = this.getCurrentProducts();
            const updatedProducts = currentProducts.map(p => 
              p.id === productId ? updatedProduct : p
            );
            
            this.productsSubject.next(updatedProducts);
            this.saveToStorage(updatedProducts);
            
            console.log(' Produit mis à jour avec succès:', updatedProduct);
            resolve(updatedProduct);
          } else {
            reject(new Error(response.message || 'Erreur lors de la mise à jour du produit'));
          }
        },
        error: (error) => {
          console.error(' Erreur lors de la mise à jour du produit:', error);
          reject(error);
        }
      });
    });
  }

  // Supprimer un produit
  deleteProduct(productId: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      try {
        const currentProducts = this.getCurrentProducts();
        const updatedProducts = currentProducts.filter(p => p.id !== productId);
        
        this.productsSubject.next(updatedProducts);
        this.saveToStorage(updatedProducts);
        
        console.log(' Produit supprimé localement');
        resolve(true);
        
        // TODO: Réactiver l'API quand elle sera disponible
        /*
        this.http.delete<any>(`${this.API_URL}/${productId}`).subscribe({
          next: (response) => {
            if (response.response === 'success') {
              const currentProducts = this.getCurrentProducts();
              const updatedProducts = currentProducts.filter(p => p.id !== productId);
              
              this.productsSubject.next(updatedProducts);
              this.saveToStorage(updatedProducts);
              
              console.log(' Produit supprimé avec succès');
              resolve(true);
            } else {
              reject(new Error(response.message || 'Erreur lors de la suppression du produit'));
            }
          },
          error: (error) => {
            console.error(' Erreur lors de la suppression du produit:', error);
            reject(error);
          }
        });
        */
      } catch (error) {
        console.error(' Erreur lors de la suppression du produit:', error);
        reject(error);
      }
    });
  }

  // Rechercher des produits
  searchProducts(query: string, categoryId?: number): Observable<Product[]> {
    // Pour l'instant, recherche locale - peut être étendue avec l'API
    const currentProducts = this.getCurrentProducts();
    
    let filtered = currentProducts;
    
    if (query) {
      filtered = filtered.filter(p => 
        p.product_name.toLowerCase().includes(query.toLowerCase()) ||
        (p.product_barcode && p.product_barcode.includes(query))
      );
    }
    
    if (categoryId) {
      filtered = filtered.filter(p => p.category_id === categoryId);
    }
    
    return of(filtered);
  }

  // Basculer le statut favori - synchronisé avec la BDD
  toggleFavorite(productId: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        const currentProducts = this.getCurrentProducts();
        const product = currentProducts.find(p => p.id === productId);
        
        if (!product) {
          reject(new Error('Produit non trouvé'));
          return;
        }

        const newFavoriteStatus = !product.isFavorite;
        
        // Mettre à jour localement (temporairement sans API)
        const updatedProducts = currentProducts.map(p => 
          p.id === productId ? { ...p, isFavorite: newFavoriteStatus } : p
        );
        
        this.productsSubject.next(updatedProducts);
        this.saveToStorage(updatedProducts);
        
        console.log(' Statut favori mis à jour localement:', newFavoriteStatus);
        resolve();
        
        // TODO: Réactiver l'API quand elle sera disponible
        /*
        this.http.patch<any>(`${this.API_URL}/${productId}`, { 
          isFavorite: newFavoriteStatus 
        }).subscribe({
          next: (response) => {
            if (response.response === 'success') {
              // Mettre à jour localement
              const updatedProducts = currentProducts.map(p => 
                p.id === productId ? { ...p, isFavorite: newFavoriteStatus } : p
              );
              
              this.productsSubject.next(updatedProducts);
              this.saveToStorage(updatedProducts);
              
              console.log(' Statut favori mis à jour dans la BDD:', newFavoriteStatus);
              resolve();
            } else {
              reject(new Error(response.message || 'Erreur lors de la mise à jour du favori'));
            }
          },
          error: (error) => {
            console.error(' Erreur lors de la mise à jour du favori:', error);
            reject(error);
          }
        });
        */
      } catch (error) {
        console.error(' Erreur lors de la mise à jour du favori:', error);
        reject(error);
      }
    });
  }

  // Rafraîchir les produits depuis l'API
  refreshProducts(): void {
    this.loadProductsFromAPI();
  }

  // Obtenir un produit par ID
  getProductById(productId: string): Product | undefined {
    return this.getCurrentProducts().find(p => p.id === productId);
  }

  // Obtenir les produits par catégorie
  getProductsByCategory(categoryId: number): Product[] {
    return this.getCurrentProducts().filter(p => p.category_id === categoryId);
  }

  // Obtenir les produits actifs
  getActiveProducts(): Product[] {
    return this.getCurrentProducts().filter(p => p.product_is_active);
  }

  // Obtenir les produits archivés
  getArchivedProducts(): Product[] {
    return this.getCurrentProducts().filter(p => !p.product_is_active);
  }

  // Rechercher un produit par code-barres
  searchProductsByBarcode(barcode: string): Product | undefined {
    const currentProducts = this.getCurrentProducts();
    return currentProducts.find(p => p.product_barcode === barcode);
  }
}
