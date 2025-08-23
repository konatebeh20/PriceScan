// Product interfaces
export interface Product {
  id: string;
  name: string;
  barcode: string;
  qrCode?: string;
  description?: string;
  category: string;
  brand?: string;
  images: ProductImage[];
  price: number;
  originalPrice?: number;
  currency: string;
  seller: Store;
  rating?: number;
  reviews?: number;
  priceHistory?: PriceHistory[];
  inStock: boolean;
  specifications?: ProductSpecification[];
  tags?: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ProductImage {
  id: string;
  url: string;
  thumbnailUrl: string;
  altText?: string;
  isPrimary: boolean;
  order: number;
}

export interface ProductSpecification {
  name: string;
  value: string;
  unit?: string;
}

export interface PriceHistory {
  id: string;
  productId: string;
  price: number;
  date: Date;
  store: Store;
}

// Store interfaces
export interface Store {
  id: string;
  name: string;
  type: 'pharmacy' | 'supermarket' | 'electronics' | 'clothing' | 'restaurant' | 'fuel' | 'online' | 'hardware' | 'beauty' | 'sports' | 'books' | 'other';
  address: Address;
  phone?: string;
  email?: string;
  website?: string;
  openingHours?: OpeningHours[];
  rating?: number;
  reviews?: number;
  logo?: string;
  images?: string[];
  isActive: boolean;
  isOnline?: boolean;
  deliveryAvailable?: boolean;
  pickupAvailable?: boolean;
  paymentMethods?: string[];
  mobileMoneyProviders?: string[];
}

export interface Address {
  street: string;
  city: string;
  state: string;
  postalCode: string;
  country: string;
  coordinates?: {
    latitude: number;
    longitude: number;
  };
  neighborhood?: string;
  landmark?: string;
}

export interface OpeningHours {
  day: 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday' | 'saturday' | 'sunday';
  open: string;
  close: string;
  isClosed: boolean;
  breakStart?: string;
  breakEnd?: string;
}

// Receipt interfaces
export interface Receipt {
  id: string;
  userId: string;
  store: Store;
  items: ReceiptItem[];
  totalAmount: number;
  taxAmount?: number;
  discountAmount?: number;
  paymentMethod: string;
  receiptNumber: string;
  purchaseDate: Date;
  scannedImage?: string;
  ocrData?: OCRData;
  isInsured: boolean;
  insuranceDetails?: InsuranceDetails;
  notes?: string;
  tags?: string[];
  images: ReceiptImage[];
  receiptType: ReceiptType;
  status: ReceiptStatus;
  createdAt: Date;
  updatedAt: Date;
}

export interface ReceiptImage {
  id: string;
  url: string;
  thumbnailUrl: string;
  isPrimary: boolean;
  order: number;
  uploadedAt: Date;
}

export type ReceiptType = 'pharmacy' | 'supermarket' | 'electronics' | 'clothing' | 'restaurant' | 'fuel' | 'online' | 'other';
export type ReceiptStatus = 'pending' | 'processed' | 'verified' | 'archived';

export interface ReceiptItem {
  id: string;
  productId?: string;
  productName: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
  category?: string;
  barcode?: string;
  qrCode?: string;
  image?: string;
  description?: string;
  brand?: string;
  unit?: string;
  discount?: number;
}

export interface OCRData {
  text: string;
  confidence: number;
  extractedData: {
    storeName?: string;
    totalAmount?: number;
    date?: Date;
    items?: string[];
    taxAmount?: number;
    discountAmount?: number;
    paymentMethod?: string;
    receiptNumber?: string;
  };
  rawData?: any;
}

export interface InsuranceDetails {
  insuranceType: 'health' | 'pharmacy' | 'warranty' | 'other';
  policyNumber?: string;
  coverageAmount?: number;
  expiryDate?: Date;
  provider?: string;
  claimNumber?: string;
  status?: 'pending' | 'approved' | 'rejected';
}

// User interfaces
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  avatar?: string;
  preferences: UserPreferences;
  location?: UserLocation;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserLocation {
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  lastUpdated: Date;
}

export interface UserPreferences {
  language: string;
  currency: string;
  country: string;
  notifications: NotificationSettings;
  privacy: PrivacySettings;
  display: DisplaySettings;
}

export interface NotificationSettings {
  priceAlerts: boolean;
  receiptReminders: boolean;
  newFeatures: boolean;
  marketing: boolean;
  storeUpdates: boolean;
  priceDrops: boolean;
}

export interface PrivacySettings {
  shareData: boolean;
  analytics: boolean;
  locationServices: boolean;
  dataCollection: boolean;
}

export interface DisplaySettings {
  theme: 'light' | 'dark' | 'auto';
  fontSize: 'small' | 'medium' | 'large';
  compactMode: boolean;
  showImages: boolean;
  showPrices: boolean;
}

// Search and filter interfaces
export interface SearchFilters {
  category?: string;
  priceRange?: {
    min: number;
    max: number;
  };
  location?: {
    latitude: number;
    longitude: number;
    radius: number;
  };
  storeType?: string[];
  inStock?: boolean;
  rating?: number;
  brand?: string[];
  hasImages?: boolean;
  hasQRCode?: boolean;
}

export interface SearchResult {
  products: Product[];
  totalCount: number;
  page: number;
  pageSize: number;
  filters: SearchFilters;
}

// API Response interfaces
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  pagination?: {
    page: number;
    pageSize: number;
    totalPages: number;
    totalCount: number;
  };
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    page: number;
    pageSize: number;
    totalPages: number;
    totalCount: number;
  };
}

// Barcode scanning interfaces
export interface BarcodeScanResult {
  id: string;
  barcode: string;
  qrCode?: string;
  product?: Product;
  stores?: Store[];
  priceComparison?: PriceComparison[];
  scanDate: Date;
  location?: {
    latitude: number;
    longitude: number;
  };
  images?: string[];
  notes?: string;
  tags?: string[];
}

export interface PriceComparison {
  store: Store;
  price: number;
  distance?: number;
  inStock: boolean;
  lastUpdated: Date;
  availability?: 'in_stock' | 'low_stock' | 'out_of_stock' | 'pre_order';
}

// API Response interface for price comparison
export interface PriceComparisonResponse {
  product_id: string;
  comparison_data: Array<{
    store_info: {
      store_name: string;
      store_city?: string;
      store_address?: string;
    };
    price_amount: number;
    price_currency: string;
    price_is_promo: boolean;
  }>;
  best_price: number;
  best_store: any;
  price_range: { min: number; max: number };
  count: number;
}

// Storage interfaces
export interface LocalStorageData {
  user: User;
  favorites: string[];
  recentSearches: string[];
  scanHistory: BarcodeScanResult[];
  receipts: Receipt[];
  settings: UserPreferences;
  cachedProducts: CachedProduct[];
  cachedStores: CachedStore[];
}

export interface CachedProduct {
  id: string;
  data: Product;
  cachedAt: Date;
  expiresAt: Date;
}

export interface CachedStore {
  id: string;
  data: Store;
  cachedAt: Date;
  expiresAt: Date;
}

// Scraping interfaces
export interface ScrapingResult {
  success: boolean;
  data?: any;
  source: string;
  timestamp: Date;
  metadata?: {
    url?: string;
    title?: string;
    description?: string;
    images?: string[];
    price?: number;
    currency?: string;
    availability?: string;
  };
}

// QR Code interfaces
export interface QRCodeData {
  type: 'product' | 'store' | 'receipt' | 'payment' | 'other';
  content: string;
  metadata?: any;
  scannedAt: Date;
  location?: {
    latitude: number;
    longitude: number;
  };
}

// Payment interfaces
export interface PaymentMethod {
  id: string;
  type: 'cash' | 'card' | 'mobile_money' | 'bank_transfer' | 'check' | 'crypto';
  name: string;
  icon?: string;
  isAvailable: boolean;
}

export interface MobileMoneyProvider {
  id: string;
  name: string;
  code: string;
  country: string;
  logo?: string;
  isActive: boolean;
}
