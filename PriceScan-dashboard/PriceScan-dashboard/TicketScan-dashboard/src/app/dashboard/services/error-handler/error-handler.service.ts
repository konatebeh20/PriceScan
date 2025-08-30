import { Injectable } from '@angular/core';
import { HttpErrorResponse, HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable, throwError, timer, of } from 'rxjs';
import { catchError, retryWhen, take, delay, mergeMap } from 'rxjs/operators';
import { API_CONFIG } from '../api/api.config';

export interface ErrorInfo {
  message: string;
  code: string;
  timestamp: Date;
  retryCount: number;
  maxRetries: number;
  isRetryable: boolean;
}

export interface RetryConfig {
  maxRetries: number;
  retryDelay: number;
  backoffMultiplier: number;
  retryableStatusCodes: number[];
}

@Injectable({
  providedIn: 'root'
})
export class ErrorHandlerService {
  private errorLog: ErrorInfo[] = [];
  private readonly DEFAULT_RETRY_CONFIG: RetryConfig = {
    maxRetries: 3,
    retryDelay: 1000,
    backoffMultiplier: 2,
    retryableStatusCodes: [408, 429, 500, 502, 503, 504]
  };

  constructor() {
    this.setupGlobalErrorHandling();
  }

  // Configuration globale de la gestion d'erreurs
  private setupGlobalErrorHandling() {
    // Intercepter les erreurs globales
    window.addEventListener('error', (event) => {
      this.logError({
        message: event.message,
        code: 'GLOBAL_ERROR',
        timestamp: new Date(),
        retryCount: 0,
        maxRetries: 0,
        isRetryable: false
      });
    });

    // Intercepter les promesses rejetées
    window.addEventListener('unhandledrejection', (event) => {
      this.logError({
        message: event.reason?.message || 'Promesse rejetée non gérée',
        code: 'UNHANDLED_PROMISE',
        timestamp: new Date(),
        retryCount: 0,
        maxRetries: 0,
        isRetryable: false
      });
    });
  }

  // Gérer les erreurs HTTP avec retry automatique
  handleHttpError(error: HttpErrorResponse, retryConfig?: Partial<RetryConfig>): Observable<any> {
    const config = { ...this.DEFAULT_RETRY_CONFIG, ...retryConfig };
    const errorInfo = this.createErrorInfo(error, config);

    this.logError(errorInfo);

    // Vérifier si l'erreur est retryable
    if (this.isRetryableError(error, config) && errorInfo.retryCount < config.maxRetries) {
      return this.retryWithBackoff(errorInfo, config);
    }

    // Si pas retryable ou max retries atteint, retourner l'erreur
    return throwError(() => this.createUserFriendlyError(error));
  }

  // Créer un objet d'information d'erreur
  private createErrorInfo(error: HttpErrorResponse, config: RetryConfig): ErrorInfo {
    return {
      message: error.message || 'Erreur inconnue',
      code: this.getErrorCode(error),
      timestamp: new Date(),
      retryCount: 0,
      maxRetries: config.maxRetries,
      isRetryable: this.isRetryableError(error, config)
    };
  }

  // Vérifier si une erreur est retryable
  private isRetryableError(error: HttpErrorResponse, config: RetryConfig): boolean {
    return config.retryableStatusCodes.includes(error.status) || 
           error.status === 0; // Erreur réseau
  }

  // Retry avec backoff exponentiel
  private retryWithBackoff(errorInfo: ErrorInfo, config: RetryConfig): Observable<any> {
    const retryCount = errorInfo.retryCount + 1;
    const delayTime = config.retryDelay * Math.pow(config.backoffMultiplier, retryCount - 1);

    console.log(` Tentative de retry ${retryCount}/${config.maxRetries} dans ${delayTime}ms`);

    return timer(delayTime).pipe(
      take(1),
      mergeMap(() => {
        // Mettre à jour le compteur de retry
        errorInfo.retryCount = retryCount;
        
        // Si c'est le dernier retry, retourner l'erreur
        if (retryCount >= config.maxRetries) {
          console.log(' Nombre maximum de retries atteint');
          return throwError(() => this.createUserFriendlyError(new HttpErrorResponse({
            error: 'Nombre maximum de tentatives atteint',
            status: 0
          })));
        }

        // Sinon, continuer avec le retry
        return of(null);
      })
    );
  }

  // Obtenir le code d'erreur
  private getErrorCode(error: HttpErrorResponse): string {
    if (error.status === 0) return 'NETWORK_ERROR';
    if (error.status === 401) return 'UNAUTHORIZED';
    if (error.status === 403) return 'FORBIDDEN';
    if (error.status === 404) return 'NOT_FOUND';
    if (error.status === 408) return 'TIMEOUT';
    if (error.status === 429) return 'RATE_LIMIT';
    if (error.status >= 500) return 'SERVER_ERROR';
    return `HTTP_${error.status}`;
  }

  // Créer un message d'erreur convivial pour l'utilisateur
  createUserFriendlyError(error: HttpErrorResponse): string {
    switch (error.status) {
      case 0:
        return 'Erreur de connexion. Vérifiez votre connexion internet.';
      case 401:
        return 'Session expirée. Veuillez vous reconnecter.';
      case 403:
        return 'Accès refusé. Vous n\'avez pas les permissions nécessaires.';
      case 404:
        return 'Ressource non trouvée.';
      case 408:
        return 'Délai d\'attente dépassé. Veuillez réessayer.';
      case 429:
        return 'Trop de requêtes. Veuillez patienter avant de réessayer.';
      case 500:
        return 'Erreur serveur. Veuillez réessayer plus tard.';
      case 502:
      case 503:
      case 504:
        return 'Service temporairement indisponible. Veuillez réessayer.';
      default:
        return 'Une erreur inattendue s\'est produite. Veuillez réessayer.';
    }
  }

  // Logger une erreur
  private logError(errorInfo: ErrorInfo) {
    this.errorLog.push(errorInfo);
    
    // Garder seulement les 100 dernières erreurs
    if (this.errorLog.length > 100) {
      this.errorLog = this.errorLog.slice(-100);
    }

    console.error('🚨 Erreur enregistrée:', errorInfo);
    
    // En production, vous pourriez envoyer l'erreur à un service de monitoring
    this.sendErrorToMonitoring(errorInfo);
  }

  // Envoyer l'erreur à un service de monitoring (exemple)
  private sendErrorToMonitoring(errorInfo: ErrorInfo) {
    // En production, implémenter l'envoi vers Sentry, LogRocket, etc.
    if (this.isProduction()) {
      // Exemple d'envoi vers un service externe
      // this.monitoringService.sendError(errorInfo);
    }
  }

  // Vérifier si on est en production
  private isProduction(): boolean {
    return window.location.hostname !== 'localhost' && 
           window.location.hostname !== '127.0.0.1';
  }

  // Obtenir le log des erreurs
  getErrorLog(): ErrorInfo[] {
    return [...this.errorLog];
  }

  // Nettoyer le log des erreurs
  clearErrorLog() {
    this.errorLog = [];
  }

  // Obtenir les erreurs récentes (dernières 24h)
  getRecentErrors(): ErrorInfo[] {
    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    return this.errorLog.filter(error => error.timestamp > oneDayAgo);
  }

  // Obtenir les erreurs par code
  getErrorsByCode(code: string): ErrorInfo[] {
    return this.errorLog.filter(error => error.code === code);
  }

  // Vérifier s'il y a des erreurs critiques récentes
  hasCriticalErrors(): boolean {
    const criticalCodes = ['NETWORK_ERROR', 'SERVER_ERROR', 'UNAUTHORIZED'];
    const recentErrors = this.getRecentErrors();
    return recentErrors.some(error => criticalCodes.includes(error.code));
  }

  // Créer un observable avec retry automatique
  createRetryableObservable<T>(
    source: Observable<T>, 
    retryConfig?: Partial<RetryConfig>
  ): Observable<T> {
    const config = { ...this.DEFAULT_RETRY_CONFIG, ...retryConfig };
    
    return source.pipe(
      retryWhen(errors => 
        errors.pipe(
          mergeMap((error, index) => {
            if (index >= config.maxRetries) {
              return throwError(() => error);
            }
            const delayTime = config.retryDelay * Math.pow(config.backoffMultiplier, index);
            console.log(` Retry automatique ${index + 1}/${config.maxRetries} dans ${delayTime}ms`);
            return timer(delayTime);
          })
        )
      ),
      catchError(error => {
        this.handleHttpError(error, config);
        return throwError(() => error);
      })
    );
  }
}
