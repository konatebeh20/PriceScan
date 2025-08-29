import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-demo-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './demo-page.html',
  styleUrls: ['./demo-page.scss']
})
export class DemoPageComponent {
  
  // Informations de démonstration
  demoFeatures = [
    {
      title: 'Fonctionnalités de base',
      description: 'Accédez aux fonctionnalités essentielles de TicketScan',
      icon: 'fas fa-star',
      available: true
    },
    {
      title: 'Gestion des reçus',
      description: 'Scannez et gérez vos reçus de base',
      icon: 'fas fa-receipt',
      available: true
    },
    {
      title: 'Analyses avancées',
      description: 'Graphiques et analyses détaillées',
      icon: 'fas fa-chart-line',
      available: false
    },
    {
      title: 'Export complet',
      description: 'Export de toutes vos données',
      icon: 'fas fa-download',
      available: false
    }
  ];

  upgradeMessage = 'Pour accéder à toutes les fonctionnalités, contactez-nous pour un compte professionnel.';
}
