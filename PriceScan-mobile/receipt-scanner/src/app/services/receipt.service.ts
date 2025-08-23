import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { ApiService } from './api.service';
import { 
  Receipt, 
  ReceiptItem, 
  OCRData, 
  InsuranceDetails,
  ReceiptType,
  ReceiptStatus,
  ReceiptImage,
  ApiResponse 
} from './interfaces';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ReceiptService {
  private receiptsSubject = new BehaviorSubject<Receipt[]>([]);
  private currentReceiptSubject = new BehaviorSubject<Receipt | null>(null);

  public receipts$ = this.receiptsSubject.asObservable();
  public currentReceipt$ = this.currentReceiptSubject.asObservable();

  constructor(private apiService: ApiService) {
    this.loadReceiptsFromStorage();
  }

  // Load receipts from local storage
  private loadReceiptsFromStorage(): void {
    const stored = localStorage.getItem('receipts');
    if (stored) {
      const receipts = JSON.parse(stored).map((receipt: any) => ({
        ...receipt,
        purchaseDate: new Date(receipt.purchaseDate),
        createdAt: new Date(receipt.createdAt),
        updatedAt: new Date(receipt.updatedAt)
      }));
      this.receiptsSubject.next(receipts);
    }
  }

  // Save receipts to local storage
  private saveReceiptsToStorage(receipts: Receipt[]): void {
    localStorage.setItem('receipts', JSON.stringify(receipts));
  }

  // Scan receipt image with OCR
  scanReceiptImage(imageFile: File, additionalData?: any): Observable<OCRData> {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    if (additionalData) {
      Object.keys(additionalData).forEach(key => {
        formData.append(key, additionalData[key]);
      });
    }

    return this.apiService.uploadFile<OCRData>('/receipts/scan-ocr', imageFile, additionalData).pipe(
      map(response => response.data!)
    );
  }

  // Create new receipt
  createReceipt(receiptData: Partial<Receipt>): Observable<Receipt> {
    const receipt: Partial<Receipt> = {
      ...receiptData,
      id: this.generateId(),
      createdAt: new Date(),
      updatedAt: new Date(),
      status: 'pending' as ReceiptStatus,
      images: receiptData.images || []
    };

    return this.apiService.post<Receipt>('/receipts', receipt).pipe(
      map(response => response.data!),
      tap(newReceipt => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = [...currentReceipts, newReceipt];
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
      })
    );
  }

  // Create receipt from OCR data
  createReceiptFromOCR(ocrData: OCRData, imageFile?: File, additionalData?: any): Observable<Receipt> {
    const receiptType = this.detectReceiptType(ocrData);
    const receiptData: Partial<Receipt> = {
      userId: this.getCurrentUserId(),
      store: this.extractStoreFromOCR(ocrData),
      items: this.extractItemsFromOCR(ocrData),
      totalAmount: ocrData.extractedData.totalAmount || 0,
      taxAmount: ocrData.extractedData.taxAmount,
      discountAmount: ocrData.extractedData.discountAmount,
      paymentMethod: ocrData.extractedData.paymentMethod || 'cash',
      receiptNumber: ocrData.extractedData.receiptNumber || this.generateReceiptNumber(),
      purchaseDate: ocrData.extractedData.date || new Date(),
      scannedImage: imageFile ? URL.createObjectURL(imageFile) : undefined,
      ocrData: ocrData,
      isInsured: this.detectInsurance(ocrData),
      insuranceDetails: this.extractInsuranceDetails(ocrData),
      notes: additionalData?.notes || '',
      tags: additionalData?.tags || [],
      receiptType: receiptType,
      status: 'pending' as ReceiptStatus,
      images: []
    };

    return this.createReceipt(receiptData);
  }

  // Get receipt by ID
  getReceiptById(id: string): Observable<Receipt> {
    return this.apiService.get<Receipt>(`/receipts/${id}`).pipe(
      map(response => response.data!),
      tap(receipt => this.currentReceiptSubject.next(receipt))
    );
  }

  // Get all user receipts
  getUserReceipts(page: number = 1, limit: number = 20): Observable<Receipt[]> {
    const params = new URLSearchParams();
    params.set('page', page.toString());
    params.set('limit', limit.toString());

    return this.apiService.get<Receipt[]>(`/receipts?${params.toString()}`).pipe(
      map(response => response.data!),
      tap(receipts => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = [...currentReceipts, ...receipts];
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
      })
    );
  }

  // Get receipts by type
  getReceiptsByType(type: ReceiptType): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/type/${type}`).pipe(
      map(response => response.data!)
    );
  }

  // Get receipts by status
  getReceiptsByStatus(status: ReceiptStatus): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/status/${status}`).pipe(
      map(response => response.data!)
    );
  }

  // Update receipt
  updateReceipt(id: string, updates: Partial<Receipt>): Observable<Receipt> {
    const updateData = {
      ...updates,
      updatedAt: new Date()
    };

    return this.apiService.put<Receipt>(`/receipts/${id}`, updateData).pipe(
      map(response => response.data!),
      tap(updatedReceipt => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = currentReceipts.map(receipt => 
          receipt.id === id ? updatedReceipt : receipt
        );
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
        
        if (this.currentReceiptSubject.value?.id === id) {
          this.currentReceiptSubject.next(updatedReceipt);
        }
      })
    );
  }

  // Delete receipt
  deleteReceipt(id: string): Observable<any> {
    return this.apiService.delete<any>(`/receipts/${id}`).pipe(
      tap(() => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = currentReceipts.filter(receipt => receipt.id !== id);
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
        
        if (this.currentReceiptSubject.value?.id === id) {
          this.currentReceiptSubject.next(null);
        }
      })
    );
  }

  // Search receipts
  searchReceipts(query: string, filters?: any): Observable<Receipt[]> {
    const searchData = {
      query,
      filters: filters || {}
    };

    return this.apiService.post<Receipt[]>(`/receipts/search`, searchData).pipe(
      map(response => response.data!)
    );
  }

  // Get receipts by store
  getReceiptsByStore(storeId: string): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/store/${storeId}`).pipe(
      map(response => response.data!)
    );
  }

  // Get receipts by date range
  getReceiptsByDateRange(startDate: Date, endDate: Date): Observable<Receipt[]> {
    const params = new URLSearchParams();
    params.set('startDate', startDate.toISOString());
    params.set('endDate', endDate.toISOString());

    return this.apiService.get<Receipt[]>(`/receipts/date-range?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Get receipts by category
  getReceiptsByCategory(category: string): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/category/${category}`).pipe(
      map(response => response.data!)
    );
  }

  // Get insurance receipts
  getInsuranceReceipts(): Observable<Receipt[]> {
    return this.apiService.get<Receipt[]>(`/receipts/insurance`).pipe(
      map(response => response.data!)
    );
  }

  // Add receipt item
  addReceiptItem(receiptId: string, item: ReceiptItem): Observable<Receipt> {
    return this.apiService.post<Receipt>(`/receipts/${receiptId}/items`, item).pipe(
      map(response => response.data!),
      tap(updatedReceipt => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = currentReceipts.map(receipt => 
          receipt.id === receiptId ? updatedReceipt : receipt
        );
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
      })
    );
  }

  // Remove receipt item
  removeReceiptItem(receiptId: string, itemId: string): Observable<Receipt> {
    return this.apiService.delete<Receipt>(`/receipts/${receiptId}/items/${itemId}`).pipe(
      map(response => response.data!),
      tap(updatedReceipt => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = currentReceipts.map(receipt => 
          receipt.id === receiptId ? updatedReceipt : receipt
        );
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
      })
    );
  }

  // Add receipt image
  addReceiptImage(receiptId: string, image: ReceiptImage): Observable<Receipt> {
    return this.apiService.post<Receipt>(`/receipts/${receiptId}/images`, image).pipe(
      map(response => response.data!),
      tap(updatedReceipt => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = currentReceipts.map(receipt => 
          receipt.id === receiptId ? updatedReceipt : receipt
        );
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
      })
    );
  }

  // Remove receipt image
  removeReceiptImage(receiptId: string, imageId: string): Observable<Receipt> {
    return this.apiService.delete<Receipt>(`/receipts/${receiptId}/images/${imageId}`).pipe(
      map(response => response.data!),
      tap(updatedReceipt => {
        const currentReceipts = this.receiptsSubject.value;
        const updatedReceipts = currentReceipts.map(receipt => 
          receipt.id === receiptId ? updatedReceipt : receipt
        );
        this.receiptsSubject.next(updatedReceipts);
        this.saveReceiptsToStorage(updatedReceipts);
      })
    );
  }

  // Get current receipts
  getCurrentReceipts(): Receipt[] {
    return this.receiptsSubject.value;
  }

  // Get current receipt
  getCurrentReceipt(): Receipt | null {
    return this.currentReceiptSubject.value;
  }

  // Clear current receipt
  clearCurrentReceipt(): void {
    this.currentReceiptSubject.next(null);
  }

  // Helper methods
  private generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  private generateReceiptNumber(): string {
    return 'RCP-' + Date.now().toString(36).toUpperCase();
  }

  private getCurrentUserId(): string {
    // This should come from your auth service
    return 'user-' + Date.now();
  }

  private extractStoreFromOCR(ocrData: OCRData): any {
    // Extract store information from OCR data
    return {
      id: 'store-' + Date.now(),
      name: ocrData.extractedData.storeName || 'Store Unknown',
      type: 'other',
      address: {
        street: '',
        city: 'Abidjan',
        state: 'Abidjan',
        postalCode: '',
        country: 'CI'
      },
      isActive: true
    };
  }

  private extractItemsFromOCR(ocrData: OCRData): ReceiptItem[] {
    // Extract items from OCR data
    const items: ReceiptItem[] = [];
    if (ocrData.extractedData.items) {
      ocrData.extractedData.items.forEach((itemText, index) => {
        items.push({
          id: 'item-' + Date.now() + '-' + index,
          productName: itemText,
          quantity: 1,
          unitPrice: 0,
          totalPrice: 0
        });
      });
    }
    return items;
  }

  private detectReceiptType(ocrData: OCRData): ReceiptType {
    const text = ocrData.text.toLowerCase();
    
    // Check pharmacy keywords
    if (environment.receiptKeywords.pharmacy.some(keyword => text.includes(keyword))) {
      return 'pharmacy';
    }
    
    // Check supermarket keywords
    if (environment.receiptKeywords.supermarket.some(keyword => text.includes(keyword))) {
      return 'supermarket';
    }
    
    // Check electronics keywords
    if (environment.receiptKeywords.electronics.some(keyword => text.includes(keyword))) {
      return 'electronics';
    }
    
    // Check clothing keywords
    if (environment.receiptKeywords.clothing.some(keyword => text.includes(keyword))) {
      return 'clothing';
    }
    
    // Check restaurant keywords
    if (environment.receiptKeywords.restaurant.some(keyword => text.includes(keyword))) {
      return 'restaurant';
    }
    
    // Check fuel keywords
    if (environment.receiptKeywords.fuel.some(keyword => text.includes(keyword))) {
      return 'fuel';
    }
    
    // Check online keywords
    if (environment.receiptKeywords.online.some(keyword => text.includes(keyword))) {
      return 'online';
    }
    
    return 'other';
  }

  private detectInsurance(ocrData: OCRData): boolean {
    // Detect if receipt is for insurance purposes
    const insuranceKeywords = environment.receiptKeywords.pharmacy;
    const text = ocrData.text.toLowerCase();
    return insuranceKeywords.some(keyword => text.includes(keyword));
  }

  private extractInsuranceDetails(ocrData: OCRData): InsuranceDetails | undefined {
    if (!this.detectInsurance(ocrData)) return undefined;

    return {
      insuranceType: 'health',
      provider: 'Unknown',
      coverageAmount: 0,
      expiryDate: new Date()
    };
  }

  // Get receipt statistics
  getReceiptStatistics(): Observable<any> {
    return this.apiService.get<any>('/receipts/statistics').pipe(
      map(response => response.data!)
    );
  }

  // Export receipts to different formats
  exportReceipts(format: 'pdf' | 'csv' | 'excel', filters?: any): Observable<string> {
    const exportData = {
      format,
      filters: filters || {}
    };

    return this.apiService.post<{ downloadUrl: string }>('/receipts/export', exportData).pipe(
      map(response => response.data!.downloadUrl)
    );
  }

  // Bulk operations
  bulkUpdateReceipts(receiptIds: string[], updates: Partial<Receipt>): Observable<any> {
    const bulkData = {
      receiptIds,
      updates
    };

    return this.apiService.put<any>('/receipts/bulk-update', bulkData).pipe(
      map(response => response.data!)
    );
  }

  bulkDeleteReceipts(receiptIds: string[]): Observable<any> {
    const bulkData = {
      receiptIds
    };

    return this.apiService.post<any>('/receipts/bulk-delete', bulkData).pipe(
      map(response => response.data!)
    );
  }
}
