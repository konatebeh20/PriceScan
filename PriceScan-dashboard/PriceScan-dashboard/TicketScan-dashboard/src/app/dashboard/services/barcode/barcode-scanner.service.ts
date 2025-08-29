import { Injectable } from '@angular/core';
import { ProductsService, Product } from '../products/products.service';

export interface ScannedProduct {
  barcode: string;
  name: string;
  price: number;
  category?: string;
  description?: string;
}

@Injectable({
  providedIn: 'root'
})
export class BarcodeScannerService {
  private isScanning = false;
  private hiddenInput: HTMLInputElement | null = null;

  // Base de données simulée des produits
  private productDatabase: { [key: string]: ScannedProduct } = {
    '1234567890123': { barcode: '1234567890123', name: 'Pain de mie', price: 1500, category: 'Boulangerie', description: 'Pain de mie frais 500g' },
    '2345678901234': { barcode: '2345678901234', name: 'Lait UHT 1L', price: 2250, category: 'Laitier', description: 'Lait UHT entier 1L' },
    '3456789012345': { barcode: '3456789012345', name: 'Yaourt nature', price: 800, category: 'Laitier', description: 'Yaourt nature 125g' },
    '4567890123456': { barcode: '4567890123456', name: 'Bananes 1kg', price: 1800, category: 'Fruits', description: 'Bananes fraîches 1kg' },
    '5678901234567': { barcode: '5678901234567', name: 'Riz parfumé 5kg', price: 9700, category: 'Céréales', description: 'Riz parfumé premium 5kg' },
    '6789012345678': { barcode: '6789012345678', name: 'Huile végétale 5L', price: 12000, category: 'Huiles', description: 'Huile végétale raffinée 5L' },
    '7890123456789': { barcode: '7890123456789', name: 'Sucre blanc 2kg', price: 4500, category: 'Sucre', description: 'Sucre blanc cristallisé 2kg' },
    '8901234567890': { barcode: '8901234567890', name: 'Farine de blé 2kg', price: 3200, category: 'Farines', description: 'Farine de blé T55 2kg' },
    '9012345678901': { barcode: '9012345678901', name: 'Tomates fraîches 2kg', price: 2800, category: 'Légumes', description: 'Tomates fraîches 2kg' },
    '0123456789012': { barcode: '0123456789012', name: 'Poulet entier', price: 10250, category: 'Viandes', description: 'Poulet frais entier 1.5kg' },
    '1111111111111': { barcode: '1111111111111', name: 'Eau minérale 1.5L', price: 600, category: 'Boissons', description: 'Eau minérale naturelle 1.5L' },
    '2222222222222': { barcode: '2222222222222', name: 'Biscuits digestifs', price: 1200, category: 'Biscuits', description: 'Biscuits digestifs 200g' },
    '3333333333333': { barcode: '3333333333333', name: 'Jus d\'orange 1L', price: 2200, category: 'Boissons', description: 'Jus d\'orange 100% naturel 1L' },
    '4444444444444': { barcode: '4444444444444', name: 'Paracétamol 500mg', price: 1400, category: 'Médicaments', description: 'Paracétamol 500mg 20 comprimés' },
    '5555555555555': { barcode: '5555555555555', name: 'Vitamine C', price: 4600, category: 'Médicaments', description: 'Vitamine C 1000mg 30 comprimés' }
  };

  constructor(private productsService: ProductsService) {}

  startScanner(): void {
    this.isScanning = true;
    this.setupHiddenInput();
  }

  stopScanner(): void {
    this.isScanning = false;
    this.cleanupHiddenInput();
  }

  isScannerActive(): boolean {
    return this.isScanning;
  }

  private setupHiddenInput(): void {
    // Créer un input caché pour capturer l'entrée du scanner
    this.hiddenInput = document.createElement('input');
    this.hiddenInput.type = 'text';
    this.hiddenInput.style.position = 'absolute';
    this.hiddenInput.style.left = '-9999px';
    this.hiddenInput.style.opacity = '0';
    this.hiddenInput.id = 'barcode-scanner-input';
    
    document.body.appendChild(this.hiddenInput);
    this.hiddenInput.focus();

    // Écouter l'entrée du scanner
    this.hiddenInput.addEventListener('input', (event) => {
      const target = event.target as HTMLInputElement;
      if (target.value.length > 0) {
        this.handleBarcodeInput(target.value);
        target.value = '';
      }
    });

    // Écouter la touche Entrée (le scanner envoie généralement cela)
    this.hiddenInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        if (this.hiddenInput && this.hiddenInput.value.length > 0) {
          this.handleBarcodeInput(this.hiddenInput.value);
          this.hiddenInput.value = '';
        }
      }
    });
  }

  private cleanupHiddenInput(): void {
    if (this.hiddenInput) {
      document.body.removeChild(this.hiddenInput);
      this.hiddenInput = null;
    }
  }

  private handleBarcodeInput(barcode: string): void {
    // Émettre un événement personnalisé pour informer les composants
    const event = new CustomEvent('barcodeScanned', { detail: { barcode } });
    document.dispatchEvent(event);
  }

  lookupProduct(barcode: string): ScannedProduct | null {
    return this.productDatabase[barcode] || null;
  }

  addProduct(barcode: string, name: string, price: number, category?: string): void {
    this.productDatabase[barcode] = {
      barcode,
      name,
      price,
      category,
      description: `${name} - ${category || 'Catégorie non spécifiée'}`
    };
  }

  searchProducts(query: string): ScannedProduct[] {
    const results: ScannedProduct[] = [];
    const searchTerm = query.toLowerCase();
    
    Object.values(this.productDatabase).forEach(product => {
      if (product.name.toLowerCase().includes(searchTerm) || 
          product.category?.toLowerCase().includes(searchTerm) ||
          product.barcode.includes(searchTerm)) {
        results.push(product);
      }
    });
    
    return results;
  }

  getProductCategories(): string[] {
    const categories = new Set<string>();
    Object.values(this.productDatabase).forEach(product => {
      if (product.category) {
        categories.add(product.category);
      }
    });
    return Array.from(categories).sort();
  }

  getProductsByCategory(category: string): ScannedProduct[] {
    return Object.values(this.productDatabase).filter(product => product.category === category);
  }
}
