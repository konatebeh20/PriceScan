import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { getApiConfig } from '../api/api.config';

export interface Category {
  id: number;
  cat_uid: string;
  cat_label: string;
  cat_description?: string;
  cat_is_featured: boolean;
  cat_banner?: string;
  cat_icon?: string;
  creation_date?: string;
  updated_on?: string;
}

@Injectable({
  providedIn: 'root'
})
export class CategoriesService {
  private readonly API_URL = getApiConfig().CATEGORIES.BASE;
  private categoriesSubject = new BehaviorSubject<Category[]>([]);
  public categories$ = this.categoriesSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadCategories();
  }

  private loadCategories(): void {
    this.http.get<any>(`${this.API_URL}`).subscribe({
      next: (response) => {
        if (response.response === 'success') {
          this.categoriesSubject.next(response.categories);
          console.log(' Catégories chargées:', response.categories.length);
        } else {
          console.error(' Erreur API catégories:', response.message);
        }
      },
      error: (error) => {
        console.error(' Erreur lors du chargement des catégories:', error);
      }
    });
  }

  getCategories(): Observable<Category[]> {
    return this.categories$;
  }

  getCurrentCategories(): Category[] {
    return this.categoriesSubject.value;
  }

  getCategoryById(id: number): Category | undefined {
    return this.getCurrentCategories().find(cat => cat.id === id);
  }

  refreshCategories(): void {
    this.loadCategories();
  }
}
