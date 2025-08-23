import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';

export interface Receipt {
  id?: string;
  userId: string;
  storeName: string;
  totalAmount: number;
  date: string;
  items: ReceiptItem[];
  imageUrl?: string;
  scannedText?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface ReceiptItem {
  id?: string;
  name: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
  category?: string;
}

export interface ReceiptScanResult {
  success: boolean;
  data?: Receipt;
  error?: string;
  confidence?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ReceiptService {
  constructor(private apiService: ApiService) { }

  // Scanner un reçu (envoi de l'image au backend pour OCR)
  scanReceipt(imageFile: File): Observable<ReceiptScanResult> {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    return this.apiService.post<ReceiptScanResult>('/receipts/scan', formData);
  }

  // Sauvegarder un reçu
  saveReceipt(receipt: Receipt): Observable<Receipt> {
    return this.apiService.post<Receipt>('/receipts', receipt);
  }

  // Récupérer tous les reçus d'un utilisateur
  getUserReceipts(userId: string): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/user/${userId}`);
  }

  // Récupérer un reçu par ID
  getReceiptById(receiptId: string): Observable<Receipt> {
    return this.apiService.get<Receipt>(`/receipts/${receiptId}`);
  }

  // Mettre à jour un reçu
  updateReceipt(receiptId: string, receipt: Partial<Receipt>): Observable<Receipt> {
    return this.apiService.put<Receipt>(`/receipts/${receiptId}`, receipt);
  }

  // Supprimer un reçu
  deleteReceipt(receiptId: string): Observable<any> {
    return this.apiService.delete<any>(`/receipts/${receiptId}`);
  }

  // Analyser les habitudes d'achat
  analyzePurchaseHabits(userId: string): Observable<any> {
    return this.apiService.get<any>(`/receipts/analysis/${userId}`);
  }

  // Rechercher des reçus par date
  searchReceiptsByDate(userId: string, startDate: string, endDate: string): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/search/${userId}?startDate=${startDate}&endDate=${endDate}`);
  }

  // Rechercher des reçus par magasin
  searchReceiptsByStore(userId: string, storeName: string): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/store/${userId}?storeName=${storeName}`);
  }
}
