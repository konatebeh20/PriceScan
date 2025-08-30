import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StoresListComponent } from '../stores-list/stores-list';
import { StoresFavorieComponent } from '../stores-favorie/stores-favorie';
import { StoresAchiveComponent } from '../stores-achive/stores-achive';

@Component({
  selector: 'app-stores-main',
  standalone: true,
  imports: [CommonModule, StoresListComponent, StoresFavorieComponent, StoresAchiveComponent],
  templateUrl: './stores-main.html',
  styleUrls: ['./stores-main.scss']
})
export class StoresMainComponent implements OnInit {
  
  // Onglet actif
  activeTab: 'list' | 'favorie' | 'achive' = 'list';

  constructor() { }

  ngOnInit(): void {
  }

  // Changer d'onglet actif
  setActiveTab(tab: 'list' | 'favorie' | 'achive'): void {
    this.activeTab = tab;
  }

  // Obtenir la classe CSS pour l'onglet actif
  getTabClass(tab: 'list' | 'favorie' | 'achive'): string {
    return this.activeTab === tab ? 'active' : '';
  }
}
