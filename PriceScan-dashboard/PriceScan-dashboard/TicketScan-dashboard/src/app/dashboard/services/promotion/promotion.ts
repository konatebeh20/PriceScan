import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of, catchError, tap, retry } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { ErrorHandlerService } from '../error-handler/error-handler.service';
import { ValidationService, PromotionData, ValidationResult } from '../validation/validation.service';

export interface Promotion {
  id?: number;
  title: string;
  description: string;
  discountType: 'percentage' | 'fixed';
  discountValue: number;
  startDate: Date;
  endDate: Date;
  minPurchase?: number;
  isActive: boolean;
  isFeatured: boolean;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface PromotionResponse {
  success: boolean;
  data?: Promotion | Promotion[];
  message?: string;
  errors?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class PromotionService {
  private apiUrl = API_CONFIG.PROMOTIONS.BASE;

  constructor(
    private http: HttpClient,
    private errorHandler: ErrorHandlerService,
    private validationService: ValidationService
  ) {}

  // Récupérer toutes les promotions
  getPromotions(): Observable<Promotion[]> {
    return this.http.get<Promotion[]>(this.apiUrl).pipe(
      retry(2),
      tap(promotions => {
        console.log('✅ Promotions récupérées:', promotions.length);
        // Sauvegarder dans le session storage
        sessionStorage.setItem('ticketscan_promotions', JSON.stringify(promotions));
      }),
      catchError(error => {
        console.error('❌ Erreur récupération promotions:', error);
        // Retourner les promotions du session storage en cas d'erreur
        const storedPromotions = sessionStorage.getItem('ticketscan_promotions');
        return of(storedPromotions ? JSON.parse(storedPromotions) : []);
      })
    );
  }

  // Récupérer les promotions actives
  getActivePromotions(): Observable<Promotion[]> {
    return this.http.get<Promotion[]>(`${API_CONFIG.PROMOTIONS.ACTIVE}`).pipe(
      retry(2),
      tap(promotions => {
        console.log('✅ Promotions actives récupérées:', promotions.length);
        sessionStorage.setItem('ticketscan_active_promotions', JSON.stringify(promotions));
      }),
      catchError(error => {
        console.error('❌ Erreur récupération promotions actives:', error);
        const storedPromotions = sessionStorage.getItem('ticketscan_active_promotions');
        return of(storedPromotions ? JSON.parse(storedPromotions) : []);
      })
    );
  }

  // Récupérer les promotions en vedette
  getFeaturedPromotions(): Observable<Promotion[]> {
    return this.http.get<Promotion[]>(`${API_CONFIG.PROMOTIONS.FEATURED}`).pipe(
      retry(2),
      tap(promotions => {
        console.log('✅ Promotions en vedette récupérées:', promotions.length);
        sessionStorage.setItem('ticketscan_featured_promotions', JSON.stringify(promotions));
      }),
      catchError(error => {
        console.error('❌ Erreur récupération promotions vedette:', error);
        const storedPromotions = sessionStorage.getItem('ticketscan_featured_promotions');
        return of(storedPromotions ? JSON.parse(storedPromotions) : []);
      })
    );
  }

  // Récupérer une promotion par ID
  getPromotionById(id: number): Observable<Promotion | null> {
    return this.http.get<Promotion>(`${API_CONFIG.PROMOTIONS.BY_ID(id)}`).pipe(
      retry(2),
      tap(promotion => console.log('✅ Promotion récupérée:', promotion.title)),
      catchError(error => {
        console.error(`❌ Erreur récupération promotion ${id}:`, error);
        // Chercher dans le session storage
        const storedPromotions = sessionStorage.getItem('ticketscan_promotions');
        if (storedPromotions) {
          const promotions = JSON.parse(storedPromotions);
          const found = promotions.find((p: Promotion) => p.id === id);
          if (found) return of(found);
        }
        return of(null);
      })
    );
  }

  // Créer une nouvelle promotion
  createPromotion(promotionData: PromotionData): Observable<PromotionResponse> {
    // Valider les données avant envoi
    const validation = this.validationService.validatePromotion(promotionData);
    if (!validation.isValid) {
      return of({
        success: false,
        message: 'Données invalides',
        errors: validation.errors
      });
    }

    return this.http.post<PromotionResponse>(this.apiUrl, promotionData).pipe(
      retry(2),
      tap(response => {
        if (response.success) {
          console.log('✅ Promotion créée avec succès');
          // Mettre à jour le session storage
          this.updatePromotionsInStorage(response.data as Promotion, 'add');
        }
      }),
      catchError(error => {
        console.error('❌ Erreur création promotion:', error);
        return of({
          success: false,
          message: 'Erreur lors de la création de la promotion',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Mettre à jour une promotion existante
  updatePromotion(id: number, promotionData: Partial<PromotionData>): Observable<PromotionResponse> {
    // Valider les données partielles
    const fullData = { ...promotionData, id } as PromotionData;
    const validation = this.validationService.validatePromotion(fullData);
    if (!validation.isValid) {
      return of({
        success: false,
        message: 'Données invalides',
        errors: validation.errors
      });
    }

    return this.http.patch<PromotionResponse>(`${API_CONFIG.PROMOTIONS.BY_ID(id)}`, promotionData).pipe(
      retry(2),
      tap(response => {
        if (response.success) {
          console.log('✅ Promotion mise à jour avec succès');
          // Mettre à jour le session storage
          this.updatePromotionsInStorage(response.data as Promotion, 'update');
        }
      }),
      catchError(error => {
        console.error(`❌ Erreur mise à jour promotion ${id}:`, error);
        return of({
          success: false,
          message: 'Erreur lors de la mise à jour de la promotion',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Supprimer une promotion
  deletePromotion(id: number): Observable<PromotionResponse> {
    return this.http.delete<PromotionResponse>(`${API_CONFIG.PROMOTIONS.BY_ID(id)}`).pipe(
      retry(2),
      tap(response => {
        if (response.success) {
          console.log('✅ Promotion supprimée avec succès');
          // Mettre à jour le session storage
          this.updatePromotionsInStorage({ id } as Promotion, 'delete');
        }
      }),
      catchError(error => {
        console.error(`❌ Erreur suppression promotion ${id}:`, error);
        return of({
          success: false,
          message: 'Erreur lors de la suppression de la promotion',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Rechercher des promotions
  searchPromotions(query: string): Observable<Promotion[]> {
    if (!query || query.trim().length < 2) {
      return of([]);
    }

    return this.http.get<Promotion[]>(`${this.apiUrl}/search?q=${encodeURIComponent(query)}`).pipe(
      retry(2),
      tap(promotions => console.log(`✅ Recherche promotions "${query}":`, promotions.length)),
      catchError(error => {
        console.error('❌ Erreur recherche promotions:', error);
        // Recherche locale dans le session storage
        return of(this.searchPromotionsInStorage(query));
      })
    );
  }

  // Recherche locale dans le session storage
  private searchPromotionsInStorage(query: string): Promotion[] {
    const storedPromotions = sessionStorage.getItem('ticketscan_promotions');
    if (!storedPromotions) return [];

    const promotions: Promotion[] = JSON.parse(storedPromotions);
    const searchTerm = query.toLowerCase();
    
    return promotions.filter(promotion => 
      promotion.title.toLowerCase().includes(searchTerm) ||
      promotion.description.toLowerCase().includes(searchTerm)
    );
  }

  // Mettre à jour le session storage après modification
  private updatePromotionsInStorage(promotion: Promotion, action: 'add' | 'update' | 'delete') {
    const storedPromotions = sessionStorage.getItem('ticketscan_promotions');
    let promotions: Promotion[] = storedPromotions ? JSON.parse(storedPromotions) : [];

    switch (action) {
      case 'add':
        if (promotion.id) {
          promotions.push(promotion);
        }
        break;
      case 'update':
        promotions = promotions.map(p => p.id === promotion.id ? { ...p, ...promotion } : p);
        break;
      case 'delete':
        promotions = promotions.filter(p => p.id !== promotion.id);
        break;
    }

    sessionStorage.setItem('ticketscan_promotions', JSON.stringify(promotions));
    console.log('💾 Session storage mis à jour pour les promotions');
  }

  // Obtenir les promotions du session storage
  getPromotionsFromStorage(): Promotion[] {
    const stored = sessionStorage.getItem('ticketscan_promotions');
    return stored ? JSON.parse(stored) : [];
  }

  // Vider le cache des promotions
  clearPromotionsCache(): void {
    sessionStorage.removeItem('ticketscan_promotions');
    sessionStorage.removeItem('ticketscan_active_promotions');
    sessionStorage.removeItem('ticketscan_featured_promotions');
    console.log('🧹 Cache des promotions vidé');
  }

  // Vérifier si une promotion est active
  isPromotionActive(promotion: Promotion): boolean {
    if (!promotion.isActive) return false;
    
    const now = new Date();
    const startDate = new Date(promotion.startDate);
    const endDate = new Date(promotion.endDate);
    
    return now >= startDate && now <= endDate;
  }

  // Calculer le prix final avec promotion
  calculateFinalPrice(originalPrice: number, promotion: Promotion): number {
    if (!this.isPromotionActive(promotion)) {
      return originalPrice;
    }

    if (promotion.discountType === 'percentage') {
      const discount = (originalPrice * promotion.discountValue) / 100;
      return Math.max(0, originalPrice - discount);
    } else {
      return Math.max(0, originalPrice - promotion.discountValue);
    }
  }

  // Obtenir les promotions applicables pour un montant d'achat
  getApplicablePromotions(purchaseAmount: number): Observable<Promotion[]> {
    return this.getActivePromotions().pipe(
      tap(promotions => {
        const applicable = promotions.filter(p => 
          !p.minPurchase || purchaseAmount >= p.minPurchase
        );
        console.log(`✅ Promotions applicables pour ${purchaseAmount} F CFA:`, applicable.length);
      })
    );
  }
}
