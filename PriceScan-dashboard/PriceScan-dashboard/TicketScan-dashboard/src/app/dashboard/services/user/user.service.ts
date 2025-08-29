import { Injectable } from '@angular/core';

export interface User {
  username: string;
  email: string;
  accountType: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre';
  businessName?: string;
  businessAddress?: string;
  businessLocation?: string;
  createdAt: Date;
  lastLogin: Date;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private currentUser: User | null = null;

  constructor() {
    this.loadCurrentUser();
  }

  loadCurrentUser(): User | null {
    const savedUser = sessionStorage.getItem('ticketscan_current_user');
    if (savedUser) {
      this.currentUser = JSON.parse(savedUser);
    }
    return this.currentUser;
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }

  updateUserProfile(userData: Partial<User>): void {
    if (this.currentUser) {
      this.currentUser = { ...this.currentUser, ...userData };
      sessionStorage.setItem('ticketscan_current_user', JSON.stringify(this.currentUser));
    }
  }

  isBusinessUser(): boolean {
    return this.currentUser?.accountType !== 'particulier';
  }

  getBusinessInfo(): { name: string; address: string } | null {
    if (!this.isBusinessUser()) {
      return null;
    }

    return {
      name: this.currentUser?.businessName || 'Commerce non spécifié',
      address: this.buildBusinessAddress()
    };
  }

  private buildBusinessAddress(): string {
    let address = '';
    if (this.currentUser?.businessAddress) {
      address += this.currentUser.businessAddress;
    }
    if (this.currentUser?.businessLocation) {
      if (address) address += ', ';
      address += this.currentUser.businessLocation;
    }
    return address || 'Adresse non spécifiée';
  }

  logout(): void {
    this.currentUser = null;
    sessionStorage.removeItem('ticketscan_current_user');
  }
}
