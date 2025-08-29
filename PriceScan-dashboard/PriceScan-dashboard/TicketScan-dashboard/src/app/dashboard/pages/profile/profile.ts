import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface UserProfile {
  username: string;
  email: string;
  accountType: 'particulier' | 'supermarché' | 'pharmacie' | 'quincaillerie' | 'autres';
  businessName?: string;
  businessActivity?: string;
  phone?: string;
  address?: string;
  createdAt: Date;
  lastLogin: Date;
}

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.html',
  styleUrls: ['./profile.scss']
})
export class ProfileComponent implements OnInit {
  
  userProfile: UserProfile = {
    username: 'utilisateur123',
    email: 'user@example.com',
    accountType: 'particulier',
    phone: '+225 0123456789',
    address: 'Abidjan, Côte d\'Ivoire',
    createdAt: new Date('2024-12-15'),
    lastLogin: new Date()
  };

  isEditing = false;
  accountTypes = [
    { value: 'particulier', label: 'Particulier', icon: 'fas fa-user' },
    { value: 'supermarché', label: 'Supermarché', icon: 'fas fa-shopping-cart' },
    { value: 'pharmacie', label: 'Pharmacie', icon: 'fas fa-pills' },
    { value: 'quincaillerie', label: 'Quincaillerie', icon: 'fas fa-tools' },
    { value: 'autres', label: 'Autres', icon: 'fas fa-building' }
  ];

  ngOnInit() {
    // Charger le profil utilisateur depuis le stockage local ou l'API
    this.loadUserProfile();
  }

  loadUserProfile() {
    // Simulation de chargement depuis le stockage local
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
      this.userProfile = { ...this.userProfile, ...JSON.parse(savedProfile) };
    }
  }

  saveProfile() {
    // Sauvegarder le profil
    localStorage.setItem('userProfile', JSON.stringify(this.userProfile));
    this.isEditing = false;
    
    // Vérifier si le type de compte est "autres" et rediriger vers la page de démo
    if (this.userProfile.accountType === 'autres') {
      // Rediriger vers la page de démo
      console.log('Redirection vers la page de démo...');
    }
  }

  cancelEdit() {
    this.isEditing = false;
    this.loadUserProfile(); // Restaurer les données originales
  }

  getAccountTypeIcon(accountType: string): string {
    const type = this.accountTypes.find(t => t.value === accountType);
    return type ? type.icon : 'fas fa-user';
  }

  getAccountTypeLabel(accountType: string): string {
    const type = this.accountTypes.find(t => t.value === accountType);
    return type ? type.label : 'Particulier';
  }

  formatDate(date: Date): string {
    return date.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  formatDateTime(date: Date): string {
    return date.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
}
