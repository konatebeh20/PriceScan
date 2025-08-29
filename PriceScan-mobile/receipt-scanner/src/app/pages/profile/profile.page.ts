import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon, IonList, IonItem, IonLabel, IonToggle, IonAvatar, IonBadge, IonChip, IonGrid, IonRow, IonCol } from '@ionic/angular/standalone';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.page.html',
  styleUrls: ['./profile.page.scss'],
  standalone: true,
  imports: [
    CommonModule, FormsModule, IonHeader, IonToolbar, IonTitle, IonContent,
    IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon,
    IonList, IonItem, IonLabel, IonToggle, IonAvatar, IonBadge, IonChip,
    IonGrid, IonRow, IonCol
  ]
})
export class ProfilePage {
  userProfile = {
    name: 'Utilisateur PriceScan',
    email: 'user@pricescan.com',
    phone: '+225 07 08 09 10 11',
    avatar: 'https://picsum.photos/100/100?random=10',
    memberSince: 'Janvier 2024',
    totalScans: 25,
    totalSavings: 150000
  };

  preferences = {
    notifications: true,
    darkMode: false,
    autoScan: true,
    priceAlerts: true,
    socialSharing: false
  };

  achievements = [
    { name: 'Premier Scan', description: 'Premier produit scanné', icon: 'scan', unlocked: true },
    { name: 'Économies', description: 'Économisé plus de 100 000 FCFA', icon: 'trending-down', unlocked: true },
    { name: 'Social', description: 'Partagé 5 bonnes affaires', icon: 'share', unlocked: false }
  ];

  // État initial des réalisations
  private initialAchievements = [
    { name: 'Premier Scan', description: 'Premier produit scanné', icon: 'scan', unlocked: false },
    { name: 'Économies', description: 'Économisé plus de 100 000 FCFA', icon: 'trending-down', unlocked: false },
    { name: 'Social', description: 'Partagé 5 bonnes affaires', icon: 'share', unlocked: false }
  ];

  isEditingProfile = false;
  editProfile = { ...this.userProfile };

  constructor() {}

  togglePreference(key: keyof typeof this.preferences) {
    this.preferences[key] = !this.preferences[key];
    
    // Gérer les réalisations basées sur les préférences
    if (key === 'socialSharing' && this.preferences.socialSharing) {
      const socialAchievement = this.achievements.find(a => a.name === 'Social');
      if (socialAchievement) {
        socialAchievement.unlocked = true;
      }
    }
    
    // Appliquer le mode sombre
    if (key === 'darkMode') {
      this.applyDarkMode();
      try { localStorage.setItem('ps_dark', this.preferences.darkMode ? 'true' : 'false'); } catch {}
    }
  }

  private applyDarkMode() {
    if (this.preferences.darkMode) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  startEditProfile() {
    this.editProfile = { ...this.userProfile };
    this.isEditingProfile = true;
  }

  saveProfile() {
    this.userProfile = { ...this.editProfile };
    this.isEditingProfile = false;
    console.log('Profil mis à jour:', this.userProfile);
  }

  cancelEdit() {
    this.isEditingProfile = false;
  }

  exportData(format: string) {
    switch(format) {
      case 'txt':
        this.exportToTXT();
        break;
      case 'pdf':
        this.exportToPDF();
        break;
    }
  }

  private exportToPDF() {
    // Simuler export PDF (en réalité, il faudrait une librairie comme jsPDF)
    console.log('Export PDF - fonctionnalité à implémenter avec librairie jsPDF');
    alert('Export PDF - fonctionnalité à implémenter');
  }

  private exportToTXT() {
    const content = `
PROFIL UTILISATEUR PRICESCAN
============================
Nom: ${this.userProfile.name}
Email: ${this.userProfile.email}
Téléphone: ${this.userProfile.phone}
Membre depuis: ${this.userProfile.memberSince}
Total scans: ${this.userProfile.totalScans}
Économies totales: ${this.userProfile.totalSavings} FCFA

PRÉFÉRENCES
===========
Notifications: ${this.preferences.notifications ? 'Activées' : 'Désactivées'}
Mode sombre: ${this.preferences.darkMode ? 'Activé' : 'Désactivé'}
Scan automatique: ${this.preferences.autoScan ? 'Activé' : 'Désactivé'}
Alertes de prix: ${this.preferences.priceAlerts ? 'Activées' : 'Désactivées'}
Partage social: ${this.preferences.socialSharing ? 'Activé' : 'Désactivé'}
    `;
    
    this.downloadFile(content, 'profile.txt', 'text/plain');
  }

  private exportToImage() {
    // Simuler export image (en réalité, il faudrait une librairie comme html2canvas)
    console.log('Export Image - fonctionnalité à implémenter avec html2canvas');
    alert('Export Image - fonctionnalité à implémenter');
  }

  private downloadFile(content: string, filename: string, mimeType: string) {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  clearData() {
    if (confirm('Êtes-vous sûr de vouloir effacer toutes vos données ? Cette action est irréversible.')) {
      // Remettre à l'état initial
      this.userProfile.totalScans = 0;
      this.userProfile.totalSavings = 0;
      this.achievements = [...this.initialAchievements];
      this.preferences = {
        notifications: true,
        darkMode: false,
        autoScan: true,
        priceAlerts: true,
        socialSharing: false
      };
      console.log('Données utilisateur remises à l\'état initial');
    }
  }

  logout() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
      // Remettre à l'état initial
      this.userProfile = {
        name: 'Utilisateur PriceScan',
        email: 'user@pricescan.com',
        phone: '+225 07 08 09 10 11',
        avatar: 'https://picsum.photos/100/100?random=10',
        memberSince: 'Janvier 2024',
        totalScans: 0,
        totalSavings: 0
      };
      this.achievements = [...this.initialAchievements];
      this.preferences = {
        notifications: true,
        darkMode: false,
        autoScan: true,
        priceAlerts: true,
        socialSharing: false
      };
      console.log('Utilisateur déconnecté');
    }
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('fr-CI', {
      style: 'currency',
      currency: 'XOF',
      minimumFractionDigits: 0
    }).format(price);
  }
}
