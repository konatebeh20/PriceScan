import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { 
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonInput,
  IonLabel, IonItem, IonList, IonFab, IonFabButton,
  IonButtons, IonBackButton, IonSpinner, IonChip, IonBadge, IonCardSubtitle,
  IonGrid, IonRow, IonCol
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-scan',
  templateUrl: './scan.page.html',
  styleUrls: ['./scan.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, IonHeader, IonToolbar, IonTitle, IonContent,
    IonButton, IonIcon, IonCard, IonCardHeader, IonCardTitle, IonCardContent, 
    // IonModal, // IonInput, 
    IonLabel, IonItem, IonList, 
    //IonFab, IonFabButton,
    IonButtons, IonBackButton, IonSpinner, IonChip, IonBadge, IonCardSubtitle,
    IonGrid, IonRow, IonCol
  ]
})
export class ScanPage {
  scanResult: string = '';
  isScanning = false;
  manualInput = '';
  scanHistory: any[] = [];
  scannedProduct: any = null;
  scannedProducts: any[] = [];

  constructor() {}

  async startScan() {
    this.isScanning = true;
    console.log('Starting camera scan...');
    
    try {
      // Vérifier si la caméra est disponible
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Ouvrir la caméra
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { 
            facingMode: 'environment', // Caméra arrière sur mobile
            width: { ideal: 1280 },
            height: { ideal: 720 }
          } 
        });
        
        // Simuler la capture d'image (en réalité, on capturerait l'image)
        setTimeout(() => {
          this.scanResult = 'Photo capturée';
          this.isScanning = false;
          this.searchProductByImage();
          // Arrêter le stream de la caméra
          stream.getTracks().forEach(track => track.stop());
        }, 3000);
        
      } else {
        // Fallback si pas de caméra
        setTimeout(() => {
          this.scanResult = '1234567890123';
          this.isScanning = false;
          this.searchProduct(this.scanResult);
        }, 2000);
      }
    } catch (error) {
      console.error('Erreur caméra:', error);
      // Fallback en cas d'erreur
      setTimeout(() => {
        this.scanResult = '1234567890123';
        this.isScanning = false;
        this.searchProduct(this.scanResult);
      }, 2000);
    }
  }

  searchProductByImage() {
    // Simuler la recherche par image avec des produits variés
    const mockProducts = [
      {
        id: 1,
        name: 'iPhone 15 Pro 128GB',
        barcode: '1234567890123',
        description: 'Smartphone Apple avec puce A17 Pro, écran 6.1" Super Retina XDR',
        category: 'Smartphones',
        brand: 'Apple',
        stores: [
          { name: 'Jumia CI', price: 850000, location: 'Abidjan, Cocody', address: 'Rue des Jardins, Cocody', phone: '+225 27 22 49 49', rating: 4.5, inStock: true },
          { name: 'Prosuma', price: 870000, location: 'Abidjan, Plateau', address: 'Boulevard Roume, Plateau', phone: '+225 27 20 21 22', rating: 4.3, inStock: true },
          { name: 'Place', price: 890000, location: 'Abidjan, Marcory', address: 'Rue des Banques, Marcory', phone: '+225 27 22 30 40', rating: 4.1, inStock: false }
        ],
        image: 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop',
        specifications: { 'Écran': '6.1" Super Retina XDR', 'Processeur': 'A17 Pro', 'Stockage': '128GB', 'Caméra': 'Triple 48MP + 12MP + 12MP', 'Batterie': 'Jusqu\'à 23h' }
      },
      {
        id: 2,
        name: 'Samsung Galaxy S24 Ultra',
        barcode: '9876543210987',
        description: 'Smartphone Samsung avec S Pen intégré, écran 6.8" Dynamic AMOLED 2X',
        category: 'Smartphones',
        brand: 'Samsung',
        stores: [
          { name: 'Jumia CI', price: 950000, location: 'Abidjan, Cocody', address: 'Rue des Jardins, Cocody', phone: '+225 27 22 49 49', rating: 4.6, inStock: true },
          { name: 'Carrefour CI', price: 980000, location: 'Abidjan, Marcory', address: 'Rue des Banques, Marcory', phone: '+225 27 22 30 40', rating: 4.4, inStock: true }
        ],
        image: 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400&h=400&fit=crop',
        specifications: { 'Écran': '6.8" Dynamic AMOLED 2X', 'Processeur': 'Snapdragon 8 Gen 3', 'Stockage': '256GB', 'Caméra': 'Quad 200MP + 12MP + 50MP + 10MP', 'Batterie': '5000mAh' }
      }
    ];
    
    // Afficher tous les produits trouvés
    this.scannedProducts = mockProducts;
    
    // Ajouter à l'historique
    mockProducts.forEach(product => {
      this.scanHistory.unshift({
        barcode: product.barcode,
        timestamp: new Date(),
        product: product.name,
        price: this.getBestPrice(product.stores),
        type: 'image'
      });
    });
  }

  searchProduct(barcode: string) {
    // Simuler la recherche de produit avec données ivoiriennes
    const mockProduct = {
      id: 1,
      name: 'iPhone 15 Pro 128GB',
      barcode: barcode,
      description: 'Smartphone Apple avec puce A17 Pro, écran 6.1" Super Retina XDR',
      category: 'Smartphones',
      brand: 'Apple',
      stores: [
        {
          name: 'Jumia CI',
          price: 850000,
          location: 'Abidjan, Cocody',
          address: 'Rue des Jardins, Cocody',
          phone: '+225 27 22 49 49',
          rating: 4.5,
          inStock: true
        },
        {
          name: 'Prosuma',
          price: 870000,
          location: 'Abidjan, Plateau',
          address: 'Boulevard Roume, Plateau',
          phone: '+225 27 20 21 22',
          rating: 4.3,
          inStock: true
        },
        {
          name: 'Place',
          price: 890000,
          location: 'Abidjan, Marcory',
          address: 'Rue des Banques, Marcory',
          phone: '+225 27 22 30 40',
          rating: 4.1,
          inStock: false
        }
      ],
      image: 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop',
      specifications: {
        'Écran': '6.1" Super Retina XDR',
        'Processeur': 'A17 Pro',
        'Stockage': '128GB',
        'Caméra': 'Triple 48MP + 12MP + 12MP',
        'Batterie': 'Jusqu\'à 23h'
      }
    };
    
    this.scannedProduct = mockProduct;
    
    // Ajouter à l'historique
    this.scanHistory.unshift({
      barcode,
      timestamp: new Date(),
      product: mockProduct.name,
      price: Math.min(...mockProduct.stores.map(s => s.price))
    });
  }

  manualSearch() {
    if (this.manualInput.trim()) {
      this.searchProduct(this.manualInput.trim());
      this.manualInput = '';
    }
  }

  clearScan() {
    this.scanResult = '';
    this.isScanning = false;
    this.scannedProduct = null;
  }

  removeFromHistory(index: number) {
    this.scanHistory.splice(index, 1);
  }

  clearHistory() {
    this.scanHistory = [];
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('fr-CI', {
      style: 'currency',
      currency: 'XOF',
      minimumFractionDigits: 0
    }).format(price);
  }

  getBestPrice(stores: any[]): number {
    return Math.min(...stores.map(s => s.price));
  }

  viewProductDetails(product: any) {
    // Afficher les détails complets du produit
    this.scannedProduct = product;
    this.scannedProducts = []; // Masquer la liste des produits
  }
}
