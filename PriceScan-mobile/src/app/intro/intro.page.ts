import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-intro',
  templateUrl: './intro.page.html',
  styleUrls: ['./intro.page.scss'],
  standalone: true,
  imports: [CommonModule, IonicModule]
})
export class IntroPage {
  
  constructor(private router: Router) {}

  // Aller à la page d'authentification
  goToAuth() {
    this.router.navigate(['/auth']);
  }

  // Aller directement à l'application (pour les tests)
  skipIntro() {
    this.router.navigate(['/user']);
  }
}
