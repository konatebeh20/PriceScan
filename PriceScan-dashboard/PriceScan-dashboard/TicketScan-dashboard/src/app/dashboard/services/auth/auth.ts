import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of, catchError, tap, retry, BehaviorSubject, map } from 'rxjs';
import { API_CONFIG } from '../api/api.config';
import { ErrorHandlerService } from '../error-handler/error-handler.service';
import { ValidationService } from '../validation/validation.service';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  firstname: string;
  lastname: string;
  accountType: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre';
  businessName?: string;
  businessAddress?: string;
  businessLocation?: string;
  phone?: string;
}

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  firstname: string;
  lastname: string;
  accountType: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre';
  businessName?: string;
  businessAddress?: string;
  businessLocation?: string;
  phone?: string;
  createdAt: Date;
  lastLogin: Date;
  isActive: boolean;
}

export interface AuthResponse {
  success: boolean;
  token?: string;
  user?: UserProfile;
  message?: string;
  errors?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = API_CONFIG.USERS.BASE;
  private currentUserSubject = new BehaviorSubject<UserProfile | null>(null);
  private tokenSubject = new BehaviorSubject<string | null>(null);

  constructor(
    private http: HttpClient,
    private errorHandler: ErrorHandlerService,
    private validationService: ValidationService
  ) {
    this.loadStoredAuth();
  }

  // Charger l'authentification stockée
  private loadStoredAuth() {
    const token = localStorage.getItem('ticketscan_token');
    const user = sessionStorage.getItem('ticketscan_current_user');
    
    if (token && user) {
      this.tokenSubject.next(token);
      this.currentUserSubject.next(JSON.parse(user));
    }
  }

  // Connexion utilisateur
  login(credentials: LoginCredentials): Observable<AuthResponse> {
    // Valider les données de connexion
    if (!this.validationService.validateEmail(credentials.email)) {
      return of({
        success: false,
        message: 'Email invalide',
        errors: ['Veuillez entrer une adresse email valide']
      });
    }

    if (!credentials.password || credentials.password.length < 6) {
      return of({
        success: false,
        message: 'Mot de passe invalide',
        errors: ['Le mot de passe doit contenir au moins 6 caractères']
      });
    }

    console.log(' Tentative de connexion avec:', credentials);
    
    // L'API PriceScan accepte soit username soit email
    // On envoie les deux pour être sûr
    const loginData = {
      username: credentials.email,
      password: credentials.password
    };
    
    return this.http.post<any>(`${API_CONFIG.USERS.LOGIN}`, loginData).pipe(
      retry(2),
      map(response => {
        console.log('📡 Réponse brute de l\'API (login):', response);
        // Adapter la réponse de l'API PriceScan au format attendu
        if (response.response === 'success' && response.admin_infos) {
          const user = response.admin_infos;
          const authResponse: AuthResponse = {
            success: true,
            message: 'Connexion réussie',
            token: user.u_uid, // Utiliser l'UID comme token temporaire
            user: {
              id: user.u_uid,
              username: user.u_username,
              email: user.u_email,
              firstname: user.u_firstname,
              lastname: user.u_lastname,
              accountType: 'particulier',
              createdAt: new Date(),
              lastLogin: new Date(),
              isActive: true
            }
          };
          
                    // Gérer la connexion réussie
          if (authResponse.token && authResponse.user) {
            this.handleSuccessfulLogin(authResponse.token, authResponse.user);
          }
          return authResponse;
        } else {
          return {
            success: false,
            message: 'Identifiants invalides',
            errors: ['Email ou mot de passe incorrect']
          };
        }
      }),
      catchError(error => {
        console.error(' Erreur de connexion:', error);
        return of({
          success: false,
          message: 'Erreur de connexion',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Inscription utilisateur
  register(data: RegisterData): Observable<AuthResponse> {
    // Valider les données d'inscription
    const validation = this.validationService.validateUserProfile(data);
    if (!validation.isValid) {
      return of({
        success: false,
        message: 'Données invalides',
        errors: validation.errors
      });
    }

    // Valider le mot de passe
    const passwordValidation = this.validationService.validatePassword(data.password);
    if (!passwordValidation.isValid) {
      return of({
        success: false,
        message: 'Mot de passe trop faible',
        errors: passwordValidation.suggestions
      });
    }

    console.log(' Tentative d\'inscription avec:', data);
    return this.http.post<any>(`${API_CONFIG.USERS.REGISTER}`, data).pipe(
      retry(2),
      map(response => {
        console.log('📡 Réponse brute de l\'API (register):', response);
        // Adapter la réponse de l'API PriceScan au format attendu
        if (response.response === 'success' && response.admin_infos) {
          const user = response.admin_infos;
          const authResponse: AuthResponse = {
            success: true,
            message: 'Inscription réussie',
            token: user.u_uid, // Utiliser l'UID comme token temporaire
            user: {
              id: user.u_uid,
              username: user.u_username,
              email: user.u_email,
              firstname: user.u_firstname,
              lastname: user.u_lastname,
              accountType: 'particulier',
              createdAt: new Date(),
              lastLogin: new Date(),
              isActive: true
            }
          };
          
          // Gérer la connexion réussie
          if (authResponse.token && authResponse.user) {
            this.handleSuccessfulLogin(authResponse.token, authResponse.user);
          }
          return authResponse;
        } else {
          return {
            success: false,
            message: 'Erreur d\'inscription',
            errors: ['Impossible de créer le compte']
          };
        }
      }),
      catchError(error => {
        console.error(' Erreur d\'inscription:', error);
        return of({
          success: false,
          message: 'Erreur d\'inscription',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Gérer une connexion réussie
  private handleSuccessfulLogin(token: string, user: UserProfile) {
    // Stocker le token
    localStorage.setItem('ticketscan_token', token);
    this.tokenSubject.next(token);

    // Stocker les informations utilisateur
    sessionStorage.setItem('ticketscan_current_user', JSON.stringify(user));
    this.currentUserSubject.next(user);

    // Mettre à jour la dernière connexion
    user.lastLogin = new Date();
    
    console.log(' Connexion réussie pour:', user.username);
  }

  // Déconnexion
  logout(): Observable<boolean> {
    const token = this.getToken();
    
    if (token) {
      // Appeler l'API de déconnexion (optionnel)
      this.http.post(`${this.apiUrl}/logout`, {}).pipe(
        catchError(() => of(null)) // Ignorer les erreurs de déconnexion
      ).subscribe();
    }

    // Nettoyer le stockage local
    this.clearAuthData();
    
    return of(true);
  }

  // Nettoyer les données d'authentification
  private clearAuthData() {
    localStorage.removeItem('ticketscan_token');
    sessionStorage.removeItem('ticketscan_current_user');
    
    this.tokenSubject.next(null);
    this.currentUserSubject.next(null);
    
    console.log('🧹 Données d\'authentification supprimées');
  }

  // Obtenir le token actuel
  getToken(): string | null {
    return this.tokenSubject.value;
  }

  // Obtenir l'utilisateur actuel
  getCurrentUser(): UserProfile | null {
    return this.currentUserSubject.value;
  }

  // Observable de l'utilisateur actuel
  getCurrentUserObservable(): Observable<UserProfile | null> {
    return this.currentUserSubject.asObservable();
  }

  // Vérifier si l'utilisateur est connecté
  isLoggedIn(): boolean {
    return !!this.getToken() && !!this.getCurrentUser();
  }

  // Vérifier si l'utilisateur est un compte professionnel
  isBusinessUser(): boolean {
    const user = this.getCurrentUser();
    return user ? user.accountType !== 'particulier' : false;
  }

  // Rafraîchir le profil utilisateur
  refreshUserProfile(): Observable<UserProfile | null> {
    if (!this.isLoggedIn()) {
      return of(null);
    }

    return this.http.get<UserProfile>(`${API_CONFIG.USERS.PROFILE}`).pipe(
      retry(2),
      tap(profile => {
        if (profile) {
          this.currentUserSubject.next(profile);
          sessionStorage.setItem('ticketscan_current_user', JSON.stringify(profile));
          console.log(' Profil utilisateur rafraîchi');
        }
      }),
      catchError(error => {
        console.error(' Erreur rafraîchissement profil:', error);
        return of(this.getCurrentUser());
      })
    );
  }

  // Mettre à jour le profil utilisateur
  updateUserProfile(profileData: Partial<UserProfile>): Observable<AuthResponse> {
    if (!this.isLoggedIn()) {
      return of({
        success: false,
        message: 'Utilisateur non connecté',
        errors: ['Vous devez être connecté pour modifier votre profil']
      });
    }

    return this.http.patch<AuthResponse>(`${API_CONFIG.USERS.PROFILE}`, profileData).pipe(
      retry(2),
      tap(response => {
        if (response.success && response.user) {
          this.currentUserSubject.next(response.user);
          sessionStorage.setItem('ticketscan_current_user', JSON.stringify(response.user));
          console.log(' Profil utilisateur mis à jour');
        }
      }),
      catchError(error => {
        console.error(' Erreur mise à jour profil:', error);
        return of({
          success: false,
          message: 'Erreur lors de la mise à jour du profil',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Changer le mot de passe
  changePassword(currentPassword: string, newPassword: string): Observable<AuthResponse> {
    if (!this.isLoggedIn()) {
      return of({
        success: false,
        message: 'Utilisateur non connecté',
        errors: ['Vous devez être connecté pour changer votre mot de passe']
      });
    }

    // Valider le nouveau mot de passe
    const passwordValidation = this.validationService.validatePassword(newPassword);
    if (!passwordValidation.isValid) {
      return of({
        success: false,
        message: 'Nouveau mot de passe trop faible',
        errors: passwordValidation.suggestions
      });
    }

    return this.http.post<AuthResponse>(`${this.apiUrl}/change-password`, {
      currentPassword,
      newPassword
    }).pipe(
      retry(2),
      tap(response => {
        if (response.success) {
          console.log(' Mot de passe changé avec succès');
        }
      }),
      catchError(error => {
        console.error(' Erreur changement mot de passe:', error);
        return of({
          success: false,
          message: 'Erreur lors du changement de mot de passe',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Demander une réinitialisation de mot de passe
  requestPasswordReset(email: string): Observable<AuthResponse> {
    if (!this.validationService.validateEmail(email)) {
      return of({
        success: false,
        message: 'Email invalide',
        errors: ['Veuillez entrer une adresse email valide']
      });
    }

    return this.http.post<AuthResponse>(`${this.apiUrl}/request-password-reset`, { email }).pipe(
      retry(2),
      tap(response => {
        if (response.success) {
          console.log(' Demande de réinitialisation envoyée');
        }
      }),
      catchError(error => {
        console.error(' Erreur demande réinitialisation:', error);
        return of({
          success: false,
          message: 'Erreur lors de la demande de réinitialisation',
          errors: [this.errorHandler.createUserFriendlyError(error)]
        });
      })
    );
  }

  // Vérifier si le token est expiré
  isTokenExpired(): boolean {
    const token = this.getToken();
    if (!token) return true;

    try {
      // Décoder le token JWT (base64)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expirationTime = payload.exp * 1000; // Convertir en millisecondes
      
      return Date.now() >= expirationTime;
    } catch {
      return true; // Token invalide
    }
  }

  // Vérifier les permissions utilisateur
  hasPermission(permission: string): boolean {
    const user = this.getCurrentUser();
    if (!user) return false;

    // Logique de vérification des permissions selon le type de compte
    switch (permission) {
      case 'manage_promotions':
        return user.accountType !== 'particulier';
      case 'view_reports':
        return user.accountType !== 'particulier';
      case 'manage_users':
        return user.accountType === 'supermarche';
      default:
        return false;
    }
  }

  // Obtenir les informations de l'entreprise
  getBusinessInfo(): { name: string; address: string } | null {
    const user = this.getCurrentUser();
    if (!user || user.accountType === 'particulier') {
      return null;
    }

    return {
      name: user.businessName || 'Commerce non spécifié',
      address: this.buildBusinessAddress(user)
    };
  }

  // Construire l'adresse de l'entreprise
  private buildBusinessAddress(user: UserProfile): string {
    let address = '';
    if (user.businessAddress) {
      address += user.businessAddress;
    }
    if (user.businessLocation) {
      if (address) address += ', ';
      address += user.businessLocation;
    }
    return address || 'Adresse non spécifiée';
  }
}
