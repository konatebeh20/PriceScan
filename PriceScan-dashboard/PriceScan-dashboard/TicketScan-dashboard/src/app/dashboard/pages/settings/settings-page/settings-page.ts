import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

interface User {
  username: string;
  email: string;
  accountType: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre';
  createdAt: Date;
  lastLogin: Date;
}

interface ImportSummary {
  receipts: number;
  products: number;
  stores: number;
  errors: number;
}

@Component({
  selector: 'app-settings-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './settings-page.html',
  styleUrls: ['./settings-page.scss']
})
export class SettingsPageComponent implements OnInit {
  @Output() pageChange = new EventEmitter<'dashboard' | 'receipts' | 'products' | 'stores' | 'settings'>();

  // Settings properties
  emailNotifications: boolean = true;
  pushNotifications: boolean = true;
  darkTheme: boolean = false;
  autoBackup: boolean = true;
  language: string = 'fr';

  // Import properties
  showImportModal: boolean = false;
  importProgress: number = 0;
  importStatus: string = '';
  importComplete: boolean = false;
  selectedFileName: string = '';
  selectedFile: File | null = null;
  importSummary: ImportSummary = {
    receipts: 0,
    products: 0,
    stores: 0,
    errors: 0
  };

  // Sample user data
  currentUser: User = {
    username: 'utilisateur123',
    email: 'user@example.com',
    accountType: 'particulier',
    createdAt: new Date('2024-12-15'),
    lastLogin: new Date()
  };

  constructor(private router: Router) {}

  ngOnInit() {
    this.loadSettings();
    this.loadCurrentUser();
  }

  // Load settings from sessionStorage
  loadSettings() {
    const savedSettings = sessionStorage.getItem('ticketscan_settings');
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      this.emailNotifications = settings.emailNotifications ?? true;
      this.pushNotifications = settings.pushNotifications ?? true;
      this.darkTheme = settings.darkTheme ?? false;
      this.autoBackup = settings.autoBackup ?? true;
      this.language = settings.language ?? 'fr';
    }
  }

  // Load current user from sessionStorage
  loadCurrentUser() {
    const savedUser = sessionStorage.getItem('ticketscan_current_user');
    if (savedUser) {
      const user = JSON.parse(savedUser);
      this.currentUser = { ...this.currentUser, ...user };
    }
  }

  // Save settings to sessionStorage
  saveSettings() {
    const settings = {
      emailNotifications: this.emailNotifications,
      pushNotifications: this.pushNotifications,
      darkTheme: this.darkTheme,
      autoBackup: this.autoBackup,
      language: this.language
    };
    sessionStorage.setItem('ticketscan_settings', JSON.stringify(settings));
  }

  // Toggle setting
  toggleSetting(setting: 'emailNotifications' | 'pushNotifications' | 'darkTheme' | 'autoBackup' | 'language') {
    if (setting === 'darkTheme') {
      this.toggleTheme();
    } else {
      (this as any)[setting] = !(this as any)[setting];
      this.saveSettings();
    }
  }

  // Toggle theme
  toggleTheme() {
    this.darkTheme = !this.darkTheme;
    this.saveSettings();
    
    if (this.darkTheme) {
      document.body.setAttribute('data-theme', 'dark');
    } else {
      document.body.removeAttribute('data-theme');
    }
    
    console.log('Theme changed to:', this.darkTheme ? 'dark' : 'light');
  }

  // Export data in different formats
  exportData(format: 'excel' | 'csv' | 'pdf' | 'txt') {
    console.log(`Exporting data in ${format.toUpperCase()} format...`);
    
    // Simulate export process
    setTimeout(() => {
      switch (format) {
        case 'excel':
          this.downloadFile('ticketscan_data.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
          break;
        case 'csv':
          this.downloadFile('ticketscan_data.csv', 'text/csv');
          break;
        case 'pdf':
          this.downloadFile('ticketscan_data.pdf', 'application/pdf');
          break;
        case 'txt':
          this.downloadFile('ticketscan_data.txt', 'text/plain');
          break;
      }
      
      alert(`Données exportées en ${format.toUpperCase()} avec succès !`);
    }, 1000);
  }

  // Download file helper
  downloadFile(filename: string, mimeType: string) {
    const content = `TicketScan - Export des données\nDate: ${new Date().toLocaleString()}\n\nCe fichier contient toutes vos données exportées.`;
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  // File selection for import
  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFileName = file.name;
      this.selectedFile = file;
    }
  }

  // Start import process
  startImport() {
    if (!this.selectedFile) {
      alert('Veuillez sélectionner un fichier à importer.');
      return;
    }

    this.showImportModal = true;
    this.importProgress = 0;
    this.importStatus = 'Préparation de l\'import...';
    this.importComplete = false;
    
    // Simulate import process
    const interval = setInterval(() => {
      this.importProgress += 10;
      
      if (this.importProgress <= 30) {
        this.importStatus = 'Lecture du fichier...';
      } else if (this.importProgress <= 60) {
        this.importStatus = 'Validation des données...';
      } else if (this.importProgress <= 90) {
        this.importStatus = 'Import en cours...';
      } else {
        this.importProgress = 100;
        this.importStatus = 'Import terminé !';
        this.importComplete = true;
        this.importSummary = {
          receipts: Math.floor(Math.random() * 50) + 10,
          products: Math.floor(Math.random() * 100) + 20,
          stores: Math.floor(Math.random() * 20) + 5,
          errors: Math.floor(Math.random() * 5)
        };
        clearInterval(interval);
      }
    }, 200);
  }

  // Close import modal
  closeImportModal() {
    this.showImportModal = false;
    this.selectedFileName = '';
    this.selectedFile = null;
    this.importProgress = 0;
    this.importStatus = '';
    this.importComplete = false;
  }

  // Reset all data
  resetAllData() {
    if (confirm('ATTENTION: Cette action est irréversible !\n\nVoulez-vous vraiment supprimer TOUTES vos données ?\n\n- Tous vos reçus\n- Tous vos produits\n- Tous vos magasins\n- Tous vos paramètres\n\nCette action ne peut pas être annulée.')) {
      if (confirm('DERNIÈRE CONFIRMATION:\n\nÊtes-vous ABSOLUMENT sûr de vouloir supprimer toutes vos données ?\n\nTapez "SUPPRIMER" pour confirmer.')) {
        // Clear all data
        sessionStorage.clear();
        localStorage.clear();
        
        // Reset component data
        this.currentUser = {
          username: '',
          email: '',
          accountType: 'particulier',
          createdAt: new Date(),
          lastLogin: new Date()
        };
        
        alert('Toutes les données ont été supprimées. Vous allez être redirigé vers la page de connexion.');
        
        // Redirect to auth page
        setTimeout(() => {
          this.router.navigate(['/auth']);
        }, 2000);
      }
    }
  }

  // Get account type label
  getAccountTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      'particulier': 'Particulier',
      'supermarche': 'Supermarché',
      'pharmacie': 'Pharmacie',
      'quincaillerie': 'Quincaillerie',
      'autre': 'Autre'
    };
    return labels[type] || type;
  }

  // Help & Support functions
  showUserGuide() {
    alert('Guide utilisateur TicketScan\n\nCette fonctionnalité sera bientôt disponible.\n\nEn attendant, vous pouvez consulter la documentation en ligne ou contacter le support.');
  }

  reportIssue() {
    alert('Signaler un problème\n\nCette fonctionnalité sera bientôt disponible.\n\nEn attendant, vous pouvez envoyer un email à support@ticketscan.com avec la description du problème.');
  }

  contactSupport() {
    alert('Contacter le support\n\nEmail: support@ticketscan.com\nTéléphone: +225 27 22 00 00\n\nHoraires: Lundi - Vendredi, 8h - 18h');
  }

  // Account actions
  editProfile() {
    alert('Modifier le profil\n\nCette fonctionnalité sera bientôt disponible.\n\nVous pourrez modifier vos informations personnelles, votre photo de profil et vos paramètres de sécurité.');
  }

  changePassword() {
    alert('Changer le mot de passe\n\nCette fonctionnalité sera bientôt disponible.\n\nVous pourrez modifier votre mot de passe en toute sécurité avec vérification de l\'ancien mot de passe.');
  }

  logout() {
    if (confirm('Voulez-vous vraiment vous déconnecter ?')) {
      sessionStorage.removeItem('ticketscan_current_user');
      this.router.navigate(['/auth']);
    }
  }

  showPage(pageName: 'dashboard' | 'receipts' | 'products' | 'stores' | 'settings') {
    this.pageChange.emit(pageName);
  }
}
