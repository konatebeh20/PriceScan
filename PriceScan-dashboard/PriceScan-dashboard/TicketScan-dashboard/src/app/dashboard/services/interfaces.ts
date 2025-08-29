// User interfaces
export interface User {
  id: string;
  username: string;
  email: string;
  accountType: 'particulier' | 'commerce';
  businessName?: string;
  businessAddress?: string;
  businessLocation?: string;
  createdAt: string;
  updatedAt: string;
}

// Product interfaces
export interface Product {
  id: string;
  name: string;
  description?: string;
  price: number;
  category: 'alimentation' | 'hygiene' | 'entretien' | 'autre';
  barcode?: string;
  isArchived: boolean;
  isFavorite: boolean;
  createdAt: string;
  updatedAt: string;
}

// Store interfaces
export interface Store {
  id: string;
  name: string;
  type: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre' | 'magasin';
  address: string;
  userId: string;
  isArchived: boolean;
  isFavorite: boolean;
  createdAt: string;
  updatedAt: string;
}

// Receipt interfaces
export interface ReceiptItem {
  name: string;
  price: number;
  quantity: number;
  total: number;
}

export interface Receipt {
  id: string;
  storeName: string;
  storeAddress: string;
  date: string;
  time: string;
  items: ReceiptItem[];
  total: number;
  type: 'scanned' | 'manual';
  isArchived: boolean;
  isFavorite: boolean;
  createdAt: string;
  updatedAt: string;
}

// Manual receipt interface
export interface ManualReceipt {
  storeName: string;
  storeAddress: string;
  date: string;
  time: string;
  items: ReceiptItem[];
  total: number;
}

// Barcode scanning interfaces
export interface ScannedProduct {
  barcode: string;
  name: string;
  price: number;
  quantity: number;
  totalPrice: number;
}

// Camera scanning interfaces
export interface CameraDevice {
  deviceId: string;
  label: string;
}

export interface ScanResult {
  success: boolean;
  barcode?: string;
  error?: string;
}
