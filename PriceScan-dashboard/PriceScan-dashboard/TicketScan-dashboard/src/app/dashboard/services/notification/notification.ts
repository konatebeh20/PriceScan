import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

export interface Notification {
  id: number;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  category: 'system' | 'user' | 'receipt' | 'product' | 'store' | 'general';
  isRead: boolean;
  isFavorite: boolean;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  actionUrl?: string;
  actionText?: string;
  expiresAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface NotificationOptions {
  duration?: number;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'center';
  autoClose?: boolean;
  showProgress?: boolean;
  closeOnClick?: boolean;
  pauseOnHover?: boolean;
}

export interface NotificationStats {
  totalNotifications: number;
  unreadNotifications: number;
  readNotifications: number;
  favoriteNotifications: number;
  notificationsByType: Record<string, number>;
  notificationsByPriority: Record<string, number>;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notifications: Notification[] = [];
  private notificationsSubject = new BehaviorSubject<Notification[]>([]);
  private statsSubject = new BehaviorSubject<NotificationStats>({
    totalNotifications: 0,
    unreadNotifications: 0,
    readNotifications: 0,
    favoriteNotifications: 0,
    notificationsByType: {},
    notificationsByPriority: {}
  });

  constructor() {
    this.initializeData();
  }

  private initializeData() {
    // Initialiser avec les données existantes
    this.notifications = [
      {
        id: 1,
        title: 'Bienvenue sur TicketScan',
        message: 'Votre compte a été créé avec succès. Commencez à scanner vos reçus !',
        type: 'success',
        category: 'system',
        isRead: true,
        isFavorite: false,
        priority: 'medium',
        actionUrl: '/dashboard',
        actionText: 'Aller au dashboard',
        createdAt: new Date('2024-01-01T09:00:00'),
        updatedAt: new Date('2024-01-01T09:00:00')
      },
      {
        id: 2,
        title: 'Nouveau reçu scanné',
        message: 'Le reçu de Carrefour Market a été analysé avec succès.',
        type: 'info',
        category: 'receipt',
        isRead: false,
        isFavorite: false,
        priority: 'low',
        actionUrl: '/receipts',
        actionText: 'Voir le reçu',
        createdAt: new Date('2024-01-15T14:30:00'),
        updatedAt: new Date('2024-01-15T14:30:00')
      },
      {
        id: 3,
        title: 'Mise à jour disponible',
        message: 'Une nouvelle version de l\'application est disponible.',
        type: 'info',
        category: 'system',
        isRead: false,
        isFavorite: false,
        priority: 'medium',
        actionUrl: '/settings',
        actionText: 'Mettre à jour',
        createdAt: new Date('2024-01-14T16:45:00'),
        updatedAt: new Date('2024-01-14T16:45:00')
      },
      {
        id: 4,
        title: 'Produit ajouté aux favoris',
        message: 'Le produit "Pain de mie" a été ajouté à vos favoris.',
        type: 'success',
        category: 'product',
        isRead: true,
        isFavorite: true,
        priority: 'low',
        actionUrl: '/products',
        actionText: 'Voir le produit',
        createdAt: new Date('2024-01-13T11:20:00'),
        updatedAt: new Date('2024-01-13T11:20:00')
      },
      {
        id: 5,
        title: 'Magasin fermé temporairement',
        message: 'Le magasin Prosuma sera fermé le 20 janvier pour maintenance.',
        type: 'warning',
        category: 'store',
        isRead: false,
        isFavorite: false,
        priority: 'high',
        actionUrl: '/stores',
        actionText: 'Voir les détails',
        createdAt: new Date('2024-01-12T10:15:00'),
        updatedAt: new Date('2024-01-12T10:15:00')
      },
      {
        id: 6,
        title: 'Erreur de synchronisation',
        message: 'Impossible de synchroniser les données avec le serveur.',
        type: 'error',
        category: 'system',
        isRead: false,
        isFavorite: false,
        priority: 'urgent',
        actionUrl: '/settings/sync',
        actionText: 'Réessayer',
        createdAt: new Date('2024-01-11T08:30:00'),
        updatedAt: new Date('2024-01-11T08:30:00')
      },
      {
        id: 7,
        title: 'Nouveau produit disponible',
        message: 'Le produit "Yaourt nature" est maintenant disponible chez Casino.',
        type: 'info',
        category: 'product',
        isRead: true,
        isFavorite: false,
        priority: 'low',
        actionUrl: '/products',
        actionText: 'Voir le produit',
        createdAt: new Date('2024-01-10T15:45:00'),
        updatedAt: new Date('2024-01-10T15:45:00')
      },
      {
        id: 8,
        title: 'Rappel de paiement',
        message: 'N\'oubliez pas de payer votre abonnement premium avant le 25 janvier.',
        type: 'warning',
        category: 'user',
        isRead: false,
        isFavorite: false,
        priority: 'high',
        actionUrl: '/settings/billing',
        actionText: 'Payer maintenant',
        createdAt: new Date('2024-01-09T12:00:00'),
        updatedAt: new Date('2024-01-09T12:00:00')
      }
    ];

    this.updateStats();
    this.notificationsSubject.next([...this.notifications]);
  }

  // Méthodes principales
  show(title: string, message: string, type: Notification['type'] = 'info', options?: NotificationOptions): Notification {
    const notification: Notification = {
      id: this.generateId(),
      title,
      message,
      type,
      category: 'general',
      isRead: false,
      isFavorite: false,
      priority: 'medium',
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.notifications.unshift(notification);
    this.updateStats();
    this.notificationsSubject.next([...this.notifications]);

    // Auto-close si configuré
    if (options?.autoClose !== false) {
      const duration = options?.duration || 5000;
      setTimeout(() => {
        this.remove(notification.id);
      }, duration);
    }

    return notification;
  }

  // Méthodes de raccourci
  success(title: string, message: string, options?: NotificationOptions): Notification {
    return this.show(title, message, 'success', options);
  }

  error(title: string, message: string, options?: NotificationOptions): Notification {
    return this.show(title, message, 'error', options);
  }

  warning(title: string, message: string, options?: NotificationOptions): Notification {
    return this.show(title, message, 'warning', options);
  }

  info(title: string, message: string, options?: NotificationOptions): Notification {
    return this.show(title, message, 'info', options);
  }

  // Méthodes CRUD
  getAllNotifications(): Observable<Notification[]> {
    return this.notificationsSubject.asObservable();
  }

  getNotificationById(id: number): Notification | undefined {
    return this.notifications.find(n => n.id === id);
  }

  addNotification(notification: Omit<Notification, 'id' | 'createdAt' | 'updatedAt'>): Notification {
    const newNotification: Notification = {
      ...notification,
      id: this.generateId(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.notifications.unshift(newNotification);
    this.updateStats();
    this.notificationsSubject.next([...this.notifications]);
    return newNotification;
  }

  updateNotification(id: number, updates: Partial<Notification>): Notification | null {
    const index = this.notifications.findIndex(n => n.id === id);
    if (index !== -1) {
      this.notifications[index] = {
        ...this.notifications[index],
        ...updates,
        updatedAt: new Date()
      };
      this.updateStats();
      this.notificationsSubject.next([...this.notifications]);
      return this.notifications[index];
    }
    return null;
  }

  remove(id: number): boolean {
    const index = this.notifications.findIndex(n => n.id === id);
    if (index !== -1) {
      this.notifications.splice(index, 1);
      this.updateStats();
      this.notificationsSubject.next([...this.notifications]);
      return true;
    }
    return false;
  }

  // Méthodes de gestion
  markAsRead(id: number): boolean {
    const notification = this.getNotificationById(id);
    if (notification && !notification.isRead) {
      notification.isRead = true;
      notification.updatedAt = new Date();
      this.updateStats();
      this.notificationsSubject.next([...this.notifications]);
      return true;
    }
    return false;
  }

  markAllAsRead(): void {
    this.notifications.forEach(notification => {
      if (!notification.isRead) {
        notification.isRead = true;
        notification.updatedAt = new Date();
      }
    });
    this.updateStats();
    this.notificationsSubject.next([...this.notifications]);
  }

  toggleFavorite(id: number): boolean {
    const notification = this.getNotificationById(id);
    if (notification) {
      notification.isFavorite = !notification.isFavorite;
      notification.updatedAt = new Date();
      this.updateStats();
      this.notificationsSubject.next([...this.notifications]);
      return true;
    }
    return false;
  }

  // Méthodes de filtrage
  getUnreadNotifications(): Notification[] {
    return this.notifications.filter(n => !n.isRead);
  }

  getReadNotifications(): Notification[] {
    return this.notifications.filter(n => n.isRead);
  }

  getFavoriteNotifications(): Notification[] {
    return this.notifications.filter(n => n.isFavorite);
  }

  getNotificationsByType(type: string): Notification[] {
    return this.notifications.filter(n => n.type === type);
  }

  getNotificationsByCategory(category: string): Notification[] {
    return this.notifications.filter(n => n.category === category);
  }

  getNotificationsByPriority(priority: string): Notification[] {
    return this.notifications.filter(n => n.priority === priority);
  }

  // Méthodes de recherche
  searchNotifications(query: string): Notification[] {
    if (!query.trim()) return [];
    
    const terms = query.toLowerCase().split(' ');
    return this.notifications.filter(notification => {
      const searchableText = `${notification.title} ${notification.message}`.toLowerCase();
      return terms.every(term => searchableText.includes(term));
    });
  }

  // Méthodes de nettoyage
  clearAll(): void {
    this.notifications = [];
    this.updateStats();
    this.notificationsSubject.next([]);
  }

  clearRead(): void {
    this.notifications = this.notifications.filter(n => !n.isRead);
    this.updateStats();
    this.notificationsSubject.next([...this.notifications]);
  }

  clearExpired(): void {
    const now = new Date();
    this.notifications = this.notifications.filter(n => !n.expiresAt || n.expiresAt > now);
    this.updateStats();
    this.notificationsSubject.next([...this.notifications]);
  }

  // Statistiques
  getStats(): Observable<NotificationStats> {
    return this.statsSubject.asObservable();
  }

  private updateStats() {
    const totalNotifications = this.notifications.length;
    const unreadNotifications = this.notifications.filter(n => !n.isRead).length;
    const readNotifications = this.notifications.filter(n => n.isRead).length;
    const favoriteNotifications = this.notifications.filter(n => n.isFavorite).length;

    const notificationsByType: Record<string, number> = {};
    const notificationsByPriority: Record<string, number> = {};

    this.notifications.forEach(notification => {
      notificationsByType[notification.type] = (notificationsByType[notification.type] || 0) + 1;
      notificationsByPriority[notification.priority] = (notificationsByPriority[notification.priority] || 0) + 1;
    });

    const stats: NotificationStats = {
      totalNotifications,
      unreadNotifications,
      readNotifications,
      favoriteNotifications,
      notificationsByType,
      notificationsByPriority
    };

    this.statsSubject.next(stats);
  }

  // Méthodes utilitaires
  private generateId(): number {
    return this.notifications.length > 0 ? Math.max(...this.notifications.map(n => n.id)) + 1 : 1;
  }

  getUnreadCount(): number {
    return this.notifications.filter(n => !n.isRead).length;
  }

  hasUnreadNotifications(): boolean {
    return this.getUnreadCount() > 0;
  }

  // Méthodes de notification en temps réel (simulées)
  subscribeToRealtime(): Observable<Notification> {
    // Simulation d'abonnement aux notifications en temps réel
    return new Observable(observer => {
      // En réalité, cela se connecterait à un WebSocket ou SSE
      console.log('Abonnement aux notifications en temps réel');
      
      return () => {
        console.log('Désabonnement des notifications en temps réel');
      };
    });
  }
}
