// Services backend originaux (vos API)
export * from './receipts/receipts';
export * from './user/user-backend';

// Services standards (votre méthodologie)
export * from './dashboard-data/dashboard-data';
export * from './products/products';
export * from './stores/stores';
export * from './user/user';
export * from './notification/notification';
export * from './theme/theme';

// Nouveaux services pour l'intégration PriceScan
export * from './api/api.config';
export * from './sync/sync.service';
export * from './error-handler/error-handler.service';
export * from './validation/validation.service';
export * from './promotion/promotion';
export * from './auth/auth';
