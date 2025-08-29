import { Component } from '@angular/core';
import { IonApp, IonRouterOutlet } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  standalone: true,
  imports: [IonApp, IonRouterOutlet, CommonModule],
})
export class AppComponent {
  constructor() {
    // Initialize dark mode from storage
    try {
      const enabled = localStorage.getItem('ps_dark') === 'true';
      document.body.classList.toggle('dark-theme', enabled);
    } catch {}
  }
}
