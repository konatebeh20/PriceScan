import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductsListComponent } from '../products-list/products-list';
import { ProductsAddComponent } from '../products-add/products-add';
import { ProductsArchiveComponent } from '../products-archive/products-archive';
import { ProductsFavoritesComponent } from '../products-favorites/products-favorites';

@Component({
  selector: 'app-products-main',
  standalone: true,
  imports: [
    CommonModule, 
    ProductsListComponent, 
    ProductsAddComponent, 
    ProductsArchiveComponent, 
    ProductsFavoritesComponent
  ],
  templateUrl: './products-main.html',
  styleUrls: ['./products-main.scss']
})
export class ProductsMainComponent implements OnInit {
  
  // Onglet actif
  activeTab: 'list' | 'add' | 'archive' | 'favorites' = 'list';

  constructor() { }

  ngOnInit(): void {
  }

  // Changer d'onglet actif
  setActiveTab(tab: 'list' | 'add' | 'archive' | 'favorites'): void {
    this.activeTab = tab;
  }

  // Obtenir la classe CSS pour l'onglet actif
  getTabClass(tab: 'list' | 'add' | 'archive' | 'favorites'): string {
    return this.activeTab === tab ? 'active' : '';
  }
}
