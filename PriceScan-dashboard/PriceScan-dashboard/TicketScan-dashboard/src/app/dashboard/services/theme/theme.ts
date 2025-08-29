import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export type ThemeMode = 'light' | 'dark' | 'auto';

export interface ThemeColors {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  shadow: string;
  success: string;
  warning: string;
  error: string;
  info: string;
}

export interface ThemeConfig {
  mode: ThemeMode;
  colors: ThemeColors;
  fonts: {
    primary: string;
    secondary: string;
    size: {
      xs: string;
      sm: string;
      base: string;
      lg: string;
      xl: string;
      '2xl': string;
      '3xl': string;
    };
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
  };
  borderRadius: {
    sm: string;
    md: string;
    lg: string;
    xl: string;
    full: string;
  };
  shadows: {
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  transitions: {
    fast: string;
    normal: string;
    slow: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private currentTheme!: ThemeConfig;
  private themeSubject = new BehaviorSubject<ThemeConfig>(this.getDefaultTheme());
  private isDarkModeSubject = new BehaviorSubject<boolean>(false);

  constructor() {
    this.initializeTheme();
  }

  private initializeTheme() {
    // Charger le thème depuis le localStorage ou utiliser le thème par défaut
    const savedTheme = localStorage.getItem('app_theme');
    if (savedTheme) {
      try {
        this.currentTheme = JSON.parse(savedTheme);
      } catch (error) {
        console.error('Erreur lors du chargement du thème:', error);
        this.currentTheme = this.getDefaultTheme();
      }
    } else {
      this.currentTheme = this.getDefaultTheme();
    }

    // Appliquer le thème
    this.applyTheme();
    
    // Écouter les changements de préférences système
    this.listenToSystemThemeChanges();
  }

  private getDefaultTheme(): ThemeConfig {
    return {
      mode: 'light',
      colors: this.getThemeColors(false),
      fonts: {
        primary: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        secondary: 'Georgia, "Times New Roman", serif',
        size: {
          xs: '0.75rem',
          sm: '0.875rem',
          base: '1rem',
          lg: '1.125rem',
          xl: '1.25rem',
          '2xl': '1.5rem',
          '3xl': '1.875rem'
        }
      },
      spacing: {
        xs: '0.25rem',
        sm: '0.5rem',
        md: '1rem',
        lg: '1.5rem',
        xl: '2rem',
        '2xl': '3rem'
      },
      borderRadius: {
        sm: '0.125rem',
        md: '0.375rem',
        lg: '0.5rem',
        xl: '0.75rem',
        full: '9999px'
      },
      shadows: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
      },
      transitions: {
        fast: '150ms ease-in-out',
        normal: '300ms ease-in-out',
        slow: '500ms ease-in-out'
      }
    };
  }

  private getThemeColors(isDark: boolean): ThemeColors {
    if (isDark) {
      return {
        primary: '#3B82F6',
        secondary: '#6B7280',
        accent: '#F59E0B',
        background: '#111827',
        surface: '#1F2937',
        text: '#F9FAFB',
        textSecondary: '#D1D5DB',
        border: '#374151',
        shadow: 'rgba(0, 0, 0, 0.3)',
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
        info: '#3B82F6'
      };
    } else {
      return {
        primary: '#2563EB',
        secondary: '#6B7280',
        accent: '#F59E0B',
        background: '#FFFFFF',
        surface: '#F9FAFB',
        text: '#111827',
        textSecondary: '#6B7280',
        border: '#E5E7EB',
        shadow: 'rgba(0, 0, 0, 0.1)',
        success: '#059669',
        warning: '#D97706',
        error: '#DC2626',
        info: '#2563EB'
      };
    }
  }

  // Méthodes publiques
  getCurrentTheme(): Observable<ThemeConfig> {
    return this.themeSubject.asObservable();
  }

  getCurrentThemeColors(): ThemeColors {
    return this.getThemeColors(this.isDarkModeSubject.value);
  }

  isDarkMode(): Observable<boolean> {
    return this.isDarkModeSubject.asObservable();
  }

  // Changement de thème
  setThemeMode(mode: ThemeMode): void {
    this.currentTheme.mode = mode;
    this.applyTheme();
    this.saveTheme();
  }

  toggleTheme(): void {
    const newMode = this.currentTheme.mode === 'light' ? 'dark' : 'light';
    this.setThemeMode(newMode);
  }

  // Configuration des couleurs
  setPrimaryColor(color: string): void {
    this.currentTheme.colors.primary = color;
    this.applyTheme();
    this.saveTheme();
  }

  setAccentColor(color: string): void {
    this.currentTheme.colors.accent = color;
    this.applyTheme();
    this.saveTheme();
  }

  // Configuration des polices
  setPrimaryFont(font: string): void {
    this.currentTheme.fonts.primary = font;
    this.applyTheme();
    this.saveTheme();
  }

  setFontSize(size: keyof ThemeConfig['fonts']['size'], value: string): void {
    this.currentTheme.fonts.size[size] = value;
    this.applyTheme();
    this.saveTheme();
  }

  // Configuration de l'espacement
  setSpacing(size: keyof ThemeConfig['spacing'], value: string): void {
    this.currentTheme.spacing[size] = value;
    this.applyTheme();
    this.saveTheme();
  }

  // Configuration des bordures
  setBorderRadius(size: keyof ThemeConfig['borderRadius'], value: string): void {
    this.currentTheme.borderRadius[size] = value;
    this.applyTheme();
    this.saveTheme();
  }

  // Configuration des ombres
  setShadow(size: keyof ThemeConfig['shadows'], value: string): void {
    this.currentTheme.shadows[size] = value;
    this.applyTheme();
    this.saveTheme();
  }

  // Configuration des transitions
  setTransition(type: keyof ThemeConfig['transitions'], value: string): void {
    this.currentTheme.transitions[type] = value;
    this.applyTheme();
    this.saveTheme();
  }

  // Application du thème
  private applyTheme(): void {
    const isDark = this.shouldUseDarkMode();
    this.isDarkModeSubject.next(isDark);
    
    const colors = this.getThemeColors(isDark);
    const theme = { ...this.currentTheme, colors };
    
    // Mettre à jour le BehaviorSubject
    this.themeSubject.next(theme);
    
    // Appliquer les variables CSS
    this.applyCSSVariables(theme);
    
    // Appliquer les classes CSS
    this.applyCSSClasses(isDark);
  }

  private shouldUseDarkMode(): boolean {
    switch (this.currentTheme.mode) {
      case 'dark':
        return true;
      case 'light':
        return false;
      case 'auto':
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
      default:
        return false;
    }
  }

  private applyCSSVariables(theme: ThemeConfig): void {
    const root = document.documentElement;
    
    // Couleurs
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value);
    });
    
    // Polices
    root.style.setProperty('--font-primary', theme.fonts.primary);
    root.style.setProperty('--font-secondary', theme.fonts.secondary);
    
    Object.entries(theme.fonts.size).forEach(([key, value]) => {
      root.style.setProperty(`--font-size-${key}`, value);
    });
    
    // Espacement
    Object.entries(theme.spacing).forEach(([key, value]) => {
      root.style.setProperty(`--spacing-${key}`, value);
    });
    
    // Bordures
    Object.entries(theme.borderRadius).forEach(([key, value]) => {
      root.style.setProperty(`--border-radius-${key}`, value);
    });
    
    // Ombres
    Object.entries(theme.shadows).forEach(([key, value]) => {
      root.style.setProperty(`--shadow-${key}`, value);
    });
    
    // Transitions
    Object.entries(theme.transitions).forEach(([key, value]) => {
      root.style.setProperty(`--transition-${key}`, value);
    });
  }

  private applyCSSClasses(isDark: boolean): void {
    const body = document.body;
    
    // Supprimer les classes existantes
    body.classList.remove('theme-light', 'theme-dark');
    
    // Ajouter la nouvelle classe
    body.classList.add(`theme-${isDark ? 'dark' : 'light'}`);
  }

  // Écouter les changements de préférences système
  private listenToSystemThemeChanges(): void {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    mediaQuery.addEventListener('change', (e) => {
      if (this.currentTheme.mode === 'auto') {
        this.applyTheme();
      }
    });
  }

  // Persistance
  private saveTheme(): void {
    try {
      localStorage.setItem('app_theme', JSON.stringify(this.currentTheme));
    } catch (error) {
      console.error('Erreur lors de la sauvegarde du thème:', error);
    }
  }

  // Réinitialisation
  resetTheme(): void {
    this.currentTheme = this.getDefaultTheme();
    this.applyTheme();
    this.saveTheme();
  }

  // Export/Import
  exportTheme(): string {
    return JSON.stringify(this.currentTheme, null, 2);
  }

  importTheme(themeJson: string): boolean {
    try {
      const theme = JSON.parse(themeJson);
      this.currentTheme = theme;
      this.applyTheme();
      this.saveTheme();
      return true;
    } catch (error) {
      console.error('Erreur lors de l\'import du thème:', error);
      return false;
    }
  }

  // Méthodes utilitaires
  getThemePreview(isDark: boolean): ThemeConfig {
    return {
      ...this.currentTheme,
      colors: this.getThemeColors(isDark)
    };
  }

  // Méthodes de validation
  validateTheme(theme: any): boolean {
    // Validation basique de la structure du thème
    const requiredKeys = ['mode', 'colors', 'fonts', 'spacing', 'borderRadius', 'shadows', 'transitions'];
    return requiredKeys.every(key => theme.hasOwnProperty(key));
  }
}
