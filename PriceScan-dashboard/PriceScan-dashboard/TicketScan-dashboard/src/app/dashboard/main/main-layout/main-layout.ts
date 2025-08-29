import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './main-layout.html',
  styleUrls: ['./main-layout.scss']
})
export class MainLayoutComponent {
  @Input() isSidebarCollapsed: boolean = false;
  @Input() isDarkTheme: boolean = false;
  @Input() isUserMenuOpen: boolean = false;
  @Input() currentPage: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile' = 'dashboard';
  @Output() sidebarToggle = new EventEmitter<void>();
  @Output() themeToggle = new EventEmitter<void>();
  @Output() userMenuToggle = new EventEmitter<void>();
  @Output() logout = new EventEmitter<void>();
  @Output() showUserProfile = new EventEmitter<void>();

  toggleSidebar() {
    this.sidebarToggle.emit();
  }

  toggleTheme() {
    this.themeToggle.emit();
  }

  toggleUserMenu() {
    this.userMenuToggle.emit();
  }

  logoutUser() {
    this.logout.emit();
  }

  showUserProfileAction() {
    this.showUserProfile.emit();
  }

  getPageTitle(): string {
    const titles: { [key: string]: string } = {
      'dashboard': 'Dashboard',
      'receipts': 'Mes Reçus',
      'products': 'Produits',
      'stores': 'Magasins',
      'settings': 'Paramètres',
      'demo': 'Version Démo',
      'profile': 'Mon Profil'
    };
    return titles[this.currentPage] || 'TicketScan';
  }

  getUserDisplayName(): string {
    // Charger les informations utilisateur depuis le stockage local
    const savedUser = localStorage.getItem('userProfile');
    if (savedUser) {
      const user = JSON.parse(savedUser);
      if (user.accountType === 'autres' && user.businessName) {
        return `Bonjour, ${user.businessName} !`;
      }
      return `Bonjour, ${user.username} !`;
    }
    return 'Bonjour, Utilisateur !';
  }
}
