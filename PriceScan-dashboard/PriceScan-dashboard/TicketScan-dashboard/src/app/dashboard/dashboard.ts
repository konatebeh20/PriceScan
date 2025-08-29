import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from './includes/sidebar/sidebar';
import { MainLayoutComponent } from './main/main-layout/main-layout';
import { MainContentComponent } from './main/main-content/main-content';

interface User {
  username: string;
  accountType: 'particulier' | 'supermarché' | 'pharmacie' | 'quincaillerie' | 'autres';
  businessName?: string;
  businessActivity?: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, SidebarComponent, MainLayoutComponent, MainContentComponent],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.scss']
})
export class DashboardComponent implements OnInit {
  isSidebarCollapsed = false;
  isDarkTheme = false;
  isUserMenuOpen = false;
  currentPage: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile' = 'dashboard';
  
  // Informations utilisateur
  currentUser: User = {
    username: 'utilisateur123',
    accountType: 'particulier'
  };

  constructor() {
    console.log('DashboardComponent constructor - currentPage:', this.currentPage);
  }

  ngOnInit() {
    console.log('DashboardComponent ngOnInit - currentPage avant:', this.currentPage);
    // Charger les informations utilisateur depuis le stockage local
    this.loadUserInfo();
    
    // Vérifier le type de compte et rediriger si nécessaire
    this.checkAccountTypeAndRedirect();
    console.log('DashboardComponent ngOnInit - currentPage après:', this.currentPage);
  }

  private loadUserInfo() {
    const savedUser = localStorage.getItem('userProfile');
    if (savedUser) {
      this.currentUser = { ...this.currentUser, ...JSON.parse(savedUser) };
      console.log('Utilisateur chargé:', this.currentUser);
    } else {
      console.log('Aucun profil utilisateur trouvé, utilisation des valeurs par défaut');
    }
  }

  private checkAccountTypeAndRedirect() {
    console.log('Vérification du type de compte:', this.currentUser.accountType);
    // Si le type de compte est "autres", rediriger vers la page de démo
    if (this.currentUser.accountType === 'autres') {
      console.log('Redirection vers la page demo');
      this.currentPage = 'demo';
    } else {
      console.log('Type de compte valide, page dashboard autorisée');
      this.currentPage = 'dashboard';
    }
  }

  toggleSidebar() {
    this.isSidebarCollapsed = !this.isSidebarCollapsed;
  }

  toggleTheme() {
    this.isDarkTheme = !this.isDarkTheme;
    document.body.setAttribute('data-theme', this.isDarkTheme ? 'dark' : 'light');
  }

  toggleUserMenu() {
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }

  logout() {
    // Logique de déconnexion
    console.log('Déconnexion...');
    // Rediriger vers la page d'authentification
    window.location.href = '/auth';
  }

  showUserProfile() {
    this.currentPage = 'profile';
    this.isUserMenuOpen = false;
  }

  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings' | 'demo' | 'profile') {
    console.log('showPage appelé avec:', pageName);
    // Vérifier si l'utilisateur peut accéder à cette page
    if (this.currentUser.accountType === 'autres' && pageName !== 'demo' && pageName !== 'profile') {
      // Rediriger vers la page de démo si c'est un compte "autres"
      console.log('Accès refusé, redirection vers demo');
      this.currentPage = 'demo';
      return;
    }
    
    console.log('Changement de page vers:', pageName);
    this.currentPage = pageName;
    this.isUserMenuOpen = false;
  }

  getUserDisplayName(): string {
    if (this.currentUser.accountType === 'autres' && this.currentUser.businessName) {
      return `Bonjour, ${this.currentUser.businessName} !`;
    }
    return `Bonjour, ${this.currentUser.username} !`;
  }
}
