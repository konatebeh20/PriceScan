import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, from } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { ApiService } from './api.service';
import { Store, Address } from './interfaces';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class LocationService {
  private currentLocationSubject = new BehaviorSubject<{ latitude: number; longitude: number } | null>(null);
  private nearbyStoresSubject = new BehaviorSubject<Store[]>([]);
  private locationPermissionSubject = new BehaviorSubject<boolean>(false);

  public currentLocation$ = this.currentLocationSubject.asObservable();
  public nearbyStores$ = this.nearbyStoresSubject.asObservable();
  public locationPermission$ = this.locationPermissionSubject.asObservable();

  constructor(private apiService: ApiService) {
    this.checkLocationPermission();
  }

  // Check location permission
  async checkLocationPermission(): Promise<boolean> {
    if ('geolocation' in navigator) {
      try {
        const permission = await navigator.permissions.query({ name: 'geolocation' as PermissionName });
        this.locationPermissionSubject.next(permission.state === 'granted');
        return permission.state === 'granted';
      } catch (error) {
        console.warn('Permission API not supported, trying direct geolocation');
        return false;
      }
    }
    return false;
  }

  // Request location permission and get current location
  async getCurrentLocation(): Promise<{ latitude: number; longitude: number }> {
    return new Promise((resolve, reject) => {
      if (!('geolocation' in navigator)) {
        reject(new Error('Geolocation not supported'));
        return;
      }

      const options = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000 // 1 minute cache
      };

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          this.currentLocationSubject.next(location);
          this.locationPermissionSubject.next(true);
          resolve(location);
        },
        (error) => {
          console.error('Geolocation error:', error);
          this.locationPermissionSubject.next(false);
          reject(error);
        },
        options
      );
    });
  }

  // Watch location changes
  watchLocation(): Observable<{ latitude: number; longitude: number }> {
    return new Observable(observer => {
      if (!('geolocation' in navigator)) {
        observer.error(new Error('Geolocation not supported'));
        return;
      }

      const options = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000
      };

      const watchId = navigator.geolocation.watchPosition(
        (position) => {
          const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          this.currentLocationSubject.next(location);
          observer.next(location);
        },
        (error) => {
          console.error('Location watch error:', error);
          observer.error(error);
        },
        options
      );

      // Return cleanup function
      return () => {
        navigator.geolocation.clearWatch(watchId);
      };
    });
  }

  // Get nearby stores
  getNearbyStores(latitude: number, longitude: number, radius: number = 10, storeType?: string[]): Observable<Store[]> {
    const params = new URLSearchParams();
    params.set('lat', latitude.toString());
    params.set('lng', longitude.toString());
    params.set('radius', radius.toString());
    if (storeType && storeType.length > 0) {
      params.set('type', storeType.join(','));
    }

    return this.apiService.get<Store[]>(`/stores/nearby?${params.toString()}`).pipe(
      map(response => response.data!),
      map(stores => this.sortStoresByDistance(stores, latitude, longitude)),
      tap(stores => this.nearbyStoresSubject.next(stores))
    );
  }

  // Get stores by product and location
  getStoresByProduct(productId: string, latitude: number, longitude: number, radius: number = 10): Observable<Store[]> {
    const params = new URLSearchParams();
    params.set('lat', latitude.toString());
    params.set('lng', longitude.toString());
    params.set('radius', radius.toString());

    return this.apiService.get<Store[]>(`/products/${productId}/stores/nearby?${params.toString()}`).pipe(
      map(response => response.data!),
      map(stores => this.sortStoresByDistance(stores, latitude, longitude))
    );
  }

  // Search stores by name or address
  searchStores(query: string, latitude?: number, longitude?: number, radius?: number): Observable<Store[]> {
    const params = new URLSearchParams();
    params.set('q', query);
    if (latitude && longitude && radius) {
      params.set('lat', latitude.toString());
      params.set('lng', longitude.toString());
      params.set('radius', radius.toString());
    }

    return this.apiService.get<Store[]>(`/stores/search?${params.toString()}`).pipe(
      map(response => response.data!)
    );
  }

  // Get store details
  getStoreDetails(storeId: string): Observable<Store> {
    return this.apiService.get<Store>(`/stores/${storeId}`).pipe(
      map(response => response.data!)
    );
  }

  // Calculate distance between two points (Haversine formula)
  calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
    const R = 6371; // Earth's radius in kilometers
    const dLat = this.deg2rad(lat2 - lat1);
    const dLon = this.deg2rad(lon2 - lon1);
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c; // Distance in kilometers
    return distance;
  }

  // Convert degrees to radians
  private deg2rad(deg: number): number {
    return deg * (Math.PI/180);
  }

  // Sort stores by distance
  private sortStoresByDistance(stores: Store[], userLat: number, userLon: number): Store[] {
    return stores.map(store => ({
      ...store,
      distance: this.calculateDistance(
        userLat, 
        userLon, 
        store.address.coordinates?.latitude || 0, 
        store.address.coordinates?.longitude || 0
      )
    })).sort((a, b) => (a.distance || 0) - (b.distance || 0));
  }

  // Get stores by category near location
  getStoresByCategory(category: string, latitude: number, longitude: number, radius: number = 10): Observable<Store[]> {
    const params = new URLSearchParams();
    params.set('category', category);
    params.set('lat', latitude.toString());
    params.set('lng', longitude.toString());
    params.set('radius', radius.toString());

    return this.apiService.get<Store[]>(`/stores/category?${params.toString()}`).pipe(
      map(response => response.data!),
      map(stores => this.sortStoresByDistance(stores, latitude, longitude))
    );
  }

  // Get pharmacy stores (for insurance purposes)
  getPharmacyStores(latitude: number, longitude: number, radius: number = 10): Observable<Store[]> {
    return this.getStoresByCategory('pharmacy', latitude, longitude, radius);
  }

  // Get supermarket stores
  getSupermarketStores(latitude: number, longitude: number, radius: number = 10): Observable<Store[]> {
    return this.getStoresByCategory('supermarket', latitude, longitude, radius);
  }

  // Get electronics stores
  getElectronicsStores(latitude: number, longitude: number, radius: number = 10): Observable<Store[]> {
    return this.getStoresByCategory('electronics', latitude, longitude, radius);
  }

  // Get current location from subject
  getCurrentLocation(): { latitude: number; longitude: number } | null {
    return this.currentLocationSubject.value;
  }

  // Get nearby stores from subject
  getNearbyStores(): Store[] {
    return this.nearbyStoresSubject.value;
  }

  // Get location permission status
  getLocationPermission(): boolean {
    return this.locationPermissionSubject.value;
  }

  // Format distance for display
  formatDistance(distance: number): string {
    if (distance < 1) {
      return `${Math.round(distance * 1000)}m`;
    } else if (distance < 10) {
      return `${distance.toFixed(1)}km`;
    } else {
      return `${Math.round(distance)}km`;
    }
  }

  // Get address string from address object
  formatAddress(address: Address): string {
    const parts = [address.street, address.city, address.state, address.postalCode, address.country];
    return parts.filter(part => part && part.trim()).join(', ');
  }

  // Check if location is within radius
  isWithinRadius(
    userLat: number, 
    userLon: number, 
    targetLat: number, 
    targetLon: number, 
    radius: number
  ): boolean {
    const distance = this.calculateDistance(userLat, userLon, targetLat, targetLon);
    return distance <= radius;
  }

  // Get stores with opening hours
  getStoresWithOpeningHours(latitude: number, longitude: number, radius: number = 10): Observable<Store[]> {
    return this.getNearbyStores(latitude, longitude, radius).pipe(
      map(stores => stores.filter(store => store.openingHours && store.openingHours.length > 0))
    );
  }

  // Check if store is currently open
  isStoreOpen(store: Store): boolean {
    if (!store.openingHours || store.openingHours.length === 0) {
      return true; // Assume open if no hours specified
    }

    const now = new Date();
    const currentDay = now.toLocaleDateString('en-US', { weekday: 'lowercase' }) as any;
    const currentTime = now.toLocaleTimeString('en-US', { hour12: false });

    const todayHours = store.openingHours.find(hours => hours.day === currentDay);
    if (!todayHours || todayHours.isClosed) {
      return false;
    }

    return currentTime >= todayHours.open && currentTime <= todayHours.close;
  }
}
