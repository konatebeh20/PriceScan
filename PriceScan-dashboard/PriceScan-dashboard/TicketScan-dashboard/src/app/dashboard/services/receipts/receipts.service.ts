import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { getApiConfig } from '../api/api.config';

export interface ReceiptItem {
  name: string;
  qty: number;
  price: number;
}

export interface Receipt {
  id: string;
  store: string;
  address: string;
  date: string;
  time: string;
  ticketNumber: string;
  status: 'analyzed' | 'processing' | 'failed';
  items: ReceiptItem[];
  total: string;
  isFavorite: boolean;
  type: 'scanned' | 'manual' | 'archived';
  createdAt: Date;
  updatedAt: Date;
}

@Injectable({
  providedIn: 'root'
})
export class ReceiptsService {
  private readonly STORAGE_KEY = 'ticketscan_receipts';
  private readonly API_URL = getApiConfig().RECEIPTS.BASE;

  private receiptsSubject = new BehaviorSubject<Receipt[]>([]);
  public receipts$ = this.receiptsSubject.asObservable();

  constructor() {
    this.loadFromStorage();
    this.loadFromDatabase();
  }

  private loadFromStorage(): void {
    try {
      const stored = sessionStorage.getItem(this.STORAGE_KEY);
      if (stored) {
        const receipts = JSON.parse(stored).map((receipt: any) => ({
          ...receipt,
          createdAt: new Date(receipt.createdAt),
          updatedAt: new Date(receipt.updatedAt)
        }));
        this.receiptsSubject.next(receipts);
      }
    } catch (error) {
      console.error('Erreur lors du chargement depuis le stockage:', error);
    }
  }

  private saveToStorage(receipts: Receipt[]): void {
    try {
      sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(receipts));
    } catch (error) {
      console.error('Erreur lors de la sauvegarde dans le stockage:', error);
    }
  }

  getReceipts(): Observable<Receipt[]> {
    return this.receipts$;
  }

  getCurrentReceipts(): Receipt[] {
    return this.receiptsSubject.value;
  }

  addReceipt(receipt: Omit<Receipt, 'id' | 'createdAt' | 'updatedAt'>): Promise<Receipt> {
    return new Promise((resolve, reject) => {
      const newReceipt: Receipt = {
        ...receipt,
        id: this.generateId(),
        createdAt: new Date(),
        updatedAt: new Date()
      };

      const currentReceipts = this.receiptsSubject.value;
      const updatedReceipts = [...currentReceipts, newReceipt];
      
      this.receiptsSubject.next(updatedReceipts);
      this.saveToStorage(updatedReceipts);
      
      this.syncToDatabase(newReceipt, 'create')
        .then(() => resolve(newReceipt))
        .catch(reject);
    });
  }

  updateReceipt(id: string, updates: Partial<Receipt>): Promise<Receipt> {
    return new Promise((resolve, reject) => {
      const currentReceipts = this.receiptsSubject.value;
      const receiptIndex = currentReceipts.findIndex(r => r.id === id);
      
      if (receiptIndex === -1) {
        reject(new Error('Reçu non trouvé'));
        return;
      }

      const updatedReceipt = {
        ...currentReceipts[receiptIndex],
        ...updates,
        updatedAt: new Date()
      };

      const updatedReceipts = [...currentReceipts];
      updatedReceipts[receiptIndex] = updatedReceipt;
      
      this.receiptsSubject.next(updatedReceipts);
      this.saveToStorage(updatedReceipts);
      
      this.syncToDatabase(updatedReceipt, 'update')
        .then(() => resolve(updatedReceipt))
        .catch(reject);
    });
  }

  deleteReceipt(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const currentReceipts = this.receiptsSubject.value;
      const receiptToDelete = currentReceipts.find(r => r.id === id);
      
      if (!receiptToDelete) {
        reject(new Error('Reçu non trouvé'));
        return;
      }

      const updatedReceipts = currentReceipts.filter(r => r.id !== id);
      this.receiptsSubject.next(updatedReceipts);
      this.saveToStorage(updatedReceipts);
      
      this.syncToDatabase(receiptToDelete, 'delete')
        .then(() => resolve())
        .catch(reject);
    });
  }

  toggleFavorite(id: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const currentReceipts = this.receiptsSubject.value;
      const receiptIndex = currentReceipts.findIndex(r => r.id === id);
      
      if (receiptIndex === -1) {
        reject(new Error('Reçu non trouvé'));
        return;
      }

      const updatedReceipt = {
        ...currentReceipts[receiptIndex],
        isFavorite: !currentReceipts[receiptIndex].isFavorite,
        updatedAt: new Date()
      };

      const updatedReceipts = [...currentReceipts];
      updatedReceipts[receiptIndex] = updatedReceipt;
      
      this.receiptsSubject.next(updatedReceipts);
      this.saveToStorage(updatedReceipts);
      
      this.syncToDatabase(updatedReceipt, 'update')
        .then(() => resolve())
        .catch(reject);
    });
  }

  archiveReceipt(id: string): Promise<void> {
    return this.updateReceipt(id, { type: 'archived' }).then(() => {});
  }

  restoreReceipt(id: string): Promise<void> {
    return this.updateReceipt(id, { type: 'scanned' }).then(() => {});
  }

  getReceiptsByType(type: 'scanned' | 'manual' | 'archived'): Receipt[] {
    const receipts = this.receiptsSubject.value;
    return receipts.filter(receipt => receipt.type === type);
  }

  getFavoriteReceipts(): Receipt[] {
    const receipts = this.receiptsSubject.value;
    return receipts.filter(receipt => receipt.isFavorite);
  }

  getReceiptsByStore(storeName: string): Receipt[] {
    const receipts = this.receiptsSubject.value;
    return receipts.filter(receipt => 
      receipt.store.toLowerCase().includes(storeName.toLowerCase())
    );
  }

  getReceiptsByDateRange(startDate: string, endDate: string): Receipt[] {
    const receipts = this.receiptsSubject.value;
    return receipts.filter(receipt => {
      const receiptDate = new Date(receipt.date);
      const start = new Date(startDate);
      const end = new Date(endDate);
      return receiptDate >= start && receiptDate <= end;
    });
  }

  private generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  private async syncToDatabase(receipt: Receipt, action: 'create' | 'update' | 'delete'): Promise<void> {
    try {
      const url = action === 'delete' 
        ? `${this.API_URL}/${receipt.id}`
        : this.API_URL;

      const method = action === 'create' ? 'POST' : action === 'update' ? 'PUT' : 'DELETE';
      
      const response = await fetch(url, {
        method,
        headers: {
          ...getApiConfig().DEFAULT_HEADERS
        },
        body: action !== 'delete' ? JSON.stringify(receipt) : undefined
      });

      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }

      console.log(`Reçu ${action === 'create' ? 'créé' : action === 'update' ? 'mis à jour' : 'supprimé'} avec succès`);
    } catch (error) {
      console.error(`Erreur lors de la synchronisation avec la base de données (${action}):`, error);
      // Ne pas rejeter - on garde les données en local même si la sync échoue
    }
  }

  async loadFromDatabase(): Promise<void> {
    try {
      const response = await fetch(this.API_URL, {
        headers: getApiConfig().DEFAULT_HEADERS
      });

      if (response.ok) {
        const receipts = await response.json();
        const receiptsWithDates = receipts.map((receipt: any) => ({
          ...receipt,
          createdAt: new Date(receipt.createdAt),
          updatedAt: new Date(receipt.updatedAt)
        }));
        
        this.receiptsSubject.next(receiptsWithDates);
        this.saveToStorage(receiptsWithDates);
      }
    } catch (error) {
      console.error('Erreur lors du chargement depuis la base de données:', error);
    }
  }

  clearStorage(): void {
    sessionStorage.removeItem(this.STORAGE_KEY);
    this.receiptsSubject.next([]);
  }
}
