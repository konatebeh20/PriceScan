import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-tab4',
  templateUrl: 'tab4.page.html',
  styleUrls: ['tab4.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class Tab4Page implements OnInit {
  darkMode: boolean = false;

  constructor(private alertController: AlertController) {}

  ngOnInit() {
    this.loadDarkMode();
  }

  loadDarkMode() {
    const stored = localStorage.getItem('darkMode');
    this.darkMode = stored === 'true';
    this.applyDarkMode();
  }

  toggleDarkMode(event: any) {
    this.darkMode = event.detail.checked;
    localStorage.setItem('darkMode', this.darkMode.toString());
    this.applyDarkMode();
  }

  applyDarkMode() {
    if (this.darkMode) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  async clearAllData() {
    const alert = await this.alertController.create({
      header: 'Clear All Data',
      message: 'Are you sure you want to clear all favorites, scan history, and settings? This action cannot be undone.',
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel'
        },
        {
          text: 'Clear',
          role: 'destructive',
          handler: () => {
            this.performClearData();
          }
        }
      ]
    });

    await alert.present();
  }

  performClearData() {
    // Clear all stored data
    localStorage.removeItem('favorites');
    localStorage.removeItem('scanHistory');
    localStorage.removeItem('darkMode');
    
    // Reset dark mode
    this.darkMode = false;
    this.applyDarkMode();
    
    // Show confirmation
    this.showClearConfirmation();
  }

  async showClearConfirmation() {
    const alert = await this.alertController.create({
      header: 'Data Cleared',
      message: 'All data has been successfully cleared.',
      buttons: ['OK']
    });

    await alert.present();
  }
}
