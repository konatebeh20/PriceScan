import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { ApiService } from './api.service';
import { 
  ProductImage, 
  ReceiptImage 
} from './interfaces';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  constructor(private apiService: ApiService) {}

  // Upload une image de produit
  uploadProductImage(productId: string, imageFile: File, isPrimary: boolean = false): Observable<ProductImage> {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('productId', productId);
    formData.append('isPrimary', isPrimary.toString());

    return this.apiService.uploadFile<ProductImage>('/images/product/upload', imageFile, {
      productId,
      isPrimary: isPrimary.toString()
    }).pipe(
      map(response => response.data!)
    );
  }

  // Upload une image de reçus
  uploadReceiptImage(receiptId: string, imageFile: File, isPrimary: boolean = false): Observable<ReceiptImage> {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('receiptId', receiptId);
    formData.append('isPrimary', isPrimary.toString());

    return this.apiService.uploadFile<ReceiptImage>('/images/receipt/upload', imageFile, {
      receiptId,
      isPrimary: isPrimary.toString()
    }).pipe(
      map(response => response.data!)
    );
  }

  // Upload plusieurs images de produit
  uploadMultipleProductImages(productId: string, imageFiles: File[]): Observable<ProductImage[]> {
    const formData = new FormData();
    imageFiles.forEach((file, index) => {
      formData.append('images', file);
    });
    formData.append('productId', productId);

    return this.apiService.uploadFile<ProductImage[]>('/images/product/upload-multiple', imageFiles[0], {
      productId,
      imageCount: imageFiles.length.toString()
    }).pipe(
      map(response => response.data!)
    );
  }

  // Upload plusieurs images de reçus
  uploadMultipleReceiptImages(receiptId: string, imageFiles: File[]): Observable<ReceiptImage[]> {
    const formData = new FormData();
    imageFiles.forEach((file, index) => {
      formData.append('images', file);
    });
    formData.append('receiptId', receiptId);

    return this.apiService.uploadFile<ReceiptImage[]>('/images/receipt/upload-multiple', imageFiles[0], {
      receiptId,
      imageCount: imageFiles.length.toString()
    }).pipe(
      map(response => response.data!)
    );
  }

  // Supprimer une image de produit
  deleteProductImage(imageId: string): Observable<any> {
    return this.apiService.delete<any>(`/images/product/${imageId}`).pipe(
      map(response => response.data!)
    );
  }

  // Supprimer une image de reçus
  deleteReceiptImage(imageId: string): Observable<any> {
    return this.apiService.delete<any>(`/images/receipt/${imageId}`).pipe(
      map(response => response.data!)
    );
  }

  // Mettre à jour l'ordre des images
  updateImageOrder(imageIds: string[], type: 'product' | 'receipt'): Observable<any> {
    const data = {
      imageIds,
      type
    };

    return this.apiService.put<any>(`/images/reorder`, data).pipe(
      map(response => response.data!)
    );
  }

  // Définir une image comme principale
  setPrimaryImage(imageId: string, type: 'product' | 'receipt'): Observable<any> {
    const data = {
      imageId,
      type
    };

    return this.apiService.put<any>(`/images/set-primary`, data).pipe(
      map(response => response.data!)
    );
  }

  // Redimensionner une image
  resizeImage(imageUrl: string, width: number, height: number): Observable<string> {
    const params = new URLSearchParams();
    params.set('url', imageUrl);
    params.set('width', width.toString());
    params.set('height', height.toString());

    return this.apiService.get<string>(`/images/resize?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Compresser une image
  compressImage(imageUrl: string, quality: number = 0.8): Observable<string> {
    const params = new URLSearchParams();
    params.set('url', imageUrl);
    params.set('quality', quality.toString());

    return this.apiService.get<string>(`/images/compress?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Convertir une image en format différent
  convertImageFormat(imageUrl: string, format: 'jpeg' | 'png' | 'webp'): Observable<string> {
    const params = new URLSearchParams();
    params.set('url', imageUrl);
    params.set('format', format);

    return this.apiService.get<string>(`/images/convert?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Extraire le texte d'une image (OCR)
  extractTextFromImage(imageFile: File): Observable<string> {
    return this.apiService.uploadFile<{ text: string }>('/images/ocr', imageFile).pipe(
      map(response => response.data!.text)
    );
  }

  // Détecter les objets dans une image
  detectObjectsInImage(imageFile: File): Observable<any[]> {
    return this.apiService.uploadFile<any[]>('/images/object-detection', imageFile).pipe(
      map(response => response.data!)
    );
  }

  // Détecter le texte dans une image (plus avancé que OCR)
  detectTextInImage(imageFile: File): Observable<any> {
    return this.apiService.uploadFile<any>('/images/text-detection', imageFile).pipe(
      map(response => response.data!)
    );
  }

  // Générer une miniature d'une image
  generateThumbnail(imageUrl: string, size: string = '150x150'): Observable<string> {
    const params = new URLSearchParams();
    params.set('url', imageUrl);
    params.set('size', size);

    return this.apiService.get<string>(`/images/thumbnail?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Obtenir les métadonnées d'une image
  getImageMetadata(imageUrl: string): Observable<any> {
    const params = new URLSearchParams();
    params.set('url', imageUrl);

    return this.apiService.get<any>(`/images/metadata?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Valider une image (format, taille, etc.)
  validateImage(imageFile: File): Observable<{ isValid: boolean; errors: string[] }> {
    const formData = new FormData();
    formData.append('image', imageFile);

    return this.apiService.uploadFile<{ isValid: boolean; errors: string[] }>('/images/validate', imageFile).pipe(
      map(response => response.data!)
    );
  }

  // Optimiser une image pour le web
  optimizeImageForWeb(imageFile: File): Observable<string> {
    return this.apiService.uploadFile<{ optimizedUrl: string }>('/images/optimize', imageFile).pipe(
      map(response => response.data!.optimizedUrl)
    );
  }

  // Créer une image de placeholder
  createPlaceholderImage(width: number, height: number, text?: string): Observable<string> {
    const data = {
      width,
      height,
      text: text || `${width}x${height}`
    };

    return this.apiService.post<{ placeholderUrl: string }>('/images/placeholder', data).pipe(
      map(response => response.data!.placeholderUrl)
    );
  }

  // Obtenir l'URL d'une image avec différentes tailles
  getImageUrl(imageUrl: string, size?: string): string {
    if (!size) return imageUrl;
    
    // Si l'image est déjà une URL complète, la retourner
    if (imageUrl.startsWith('http')) {
      return imageUrl;
    }
    
    // Sinon, construire l'URL avec la taille
    const baseUrl = environment.apiUrl.replace('/api', '');
    return `${baseUrl}/images/${size}/${imageUrl}`;
  }

  // Obtenir l'URL d'une miniature
  getThumbnailUrl(imageUrl: string): string {
    return this.getImageUrl(imageUrl, environment.productImages.thumbnailSize);
  }

  // Obtenir l'URL d'une image en taille complète
  getFullSizeUrl(imageUrl: string): string {
    return this.getImageUrl(imageUrl, environment.productImages.fullSize);
  }

  // Vérifier si une image existe
  checkImageExists(imageUrl: string): Observable<boolean> {
    return from(new Promise<boolean>((resolve) => {
      const img = new Image();
      img.onload = () => resolve(true);
      img.onerror = () => resolve(false);
      img.src = imageUrl;
    }));
  }

  // Précharger une image
  preloadImage(imageUrl: string): Observable<string> {
    return from(new Promise<string>((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(imageUrl);
      img.onerror = () => reject(new Error('Impossible de charger l\'image'));
      img.src = imageUrl;
    }));
  }

  // Obtenir la taille d'une image
  getImageDimensions(imageUrl: string): Observable<{ width: number; height: number }> {
    return from(new Promise<{ width: number; height: number }>((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve({ width: img.naturalWidth, height: img.naturalHeight });
      img.onerror = () => reject(new Error('Impossible de charger l\'image'));
      img.src = imageUrl;
    }));
  }
}
