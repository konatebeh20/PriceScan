import { Injectable } from '@angular/core';

export interface ValidationRule {
  field: string;
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  customValidator?: (value: any, data?: any) => boolean;
  errorMessage: string;
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  fieldErrors: { [key: string]: string[] };
}

export interface UserProfileData {
  username: string;
  email: string;
  firstname: string;
  lastname: string;
  accountType: 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre';
  businessName?: string;
  businessAddress?: string;
  businessLocation?: string;
  phone?: string;
}

export interface PromotionData {
  title: string;
  description: string;
  discountType: 'percentage' | 'fixed';
  discountValue: number;
  startDate: Date;
  endDate: Date;
  minPurchase?: number;
  isActive: boolean;
  isFeatured: boolean;
}

export interface ReceiptData {
  store: string;
  address: string;
  date: string;
  time: string;
  ticketNumber: string;
  items: Array<{
    name: string;
    qty: number;
    price: number;
  }>;
  total: string;
}

@Injectable({
  providedIn: 'root'
})
export class ValidationService {
  
  // Règles de validation pour le profil utilisateur
  private userProfileRules: ValidationRule[] = [
    {
      field: 'username',
      required: true,
      minLength: 3,
      maxLength: 50,
      pattern: /^[a-zA-Z0-9_]+$/,
      errorMessage: 'Le nom d\'utilisateur doit contenir 3-50 caractères (lettres, chiffres, underscore)'
    },
    {
      field: 'email',
      required: true,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      errorMessage: 'Veuillez entrer une adresse email valide'
    },
    {
      field: 'firstname',
      required: true,
      minLength: 2,
      maxLength: 50,
      pattern: /^[a-zA-ZÀ-ÿ\s'-]+$/,
      errorMessage: 'Le prénom doit contenir 2-50 caractères (lettres uniquement)'
    },
    {
      field: 'lastname',
      required: true,
      minLength: 2,
      maxLength: 50,
      pattern: /^[a-zA-ZÀ-ÿ\s'-]+$/,
      errorMessage: 'Le nom doit contenir 2-50 caractères (lettres uniquement)'
    },
    {
      field: 'accountType',
      required: true,
      customValidator: (value) => ['particulier', 'supermarche', 'pharmacie', 'quincaillerie', 'autre'].includes(value),
      errorMessage: 'Veuillez sélectionner un type de compte valide'
    },
    {
      field: 'businessName',
      required: false,
      minLength: 2,
      maxLength: 100,
      customValidator: (value: any, data: any) => {
        if (data?.accountType === 'particulier') return true;
        return value && value.length >= 2;
      },
      errorMessage: 'Le nom de l\'entreprise est requis pour les comptes professionnels'
    },
    {
      field: 'phone',
      required: false,
      pattern: /^(\+225|225)?[0-9]{8,10}$/,
      errorMessage: 'Veuillez entrer un numéro de téléphone valide (format: +225 01234567)'
    }
  ];

  // Règles de validation pour les promotions
  private promotionRules: ValidationRule[] = [
    {
      field: 'title',
      required: true,
      minLength: 5,
      maxLength: 100,
      errorMessage: 'Le titre doit contenir 5-100 caractères'
    },
    {
      field: 'description',
      required: true,
      minLength: 10,
      maxLength: 500,
      errorMessage: 'La description doit contenir 10-500 caractères'
    },
    {
      field: 'discountValue',
      required: true,
      customValidator: (value) => value > 0 && value <= 100,
      errorMessage: 'La valeur de réduction doit être entre 1 et 100'
    },
    {
      field: 'startDate',
      required: true,
      customValidator: (value) => value instanceof Date && value > new Date(),
      errorMessage: 'La date de début doit être dans le futur'
    },
    {
      field: 'endDate',
      required: true,
      customValidator: (value: any, data: any) => {
        if (!(value instanceof Date)) return false;
        return value > data.startDate;
      },
      errorMessage: 'La date de fin doit être après la date de début'
    },
    {
      field: 'minPurchase',
      required: false,
      customValidator: (value) => !value || value >= 0,
      errorMessage: 'Le montant minimum d\'achat doit être positif'
    }
  ];

  // Règles de validation pour les reçus
  private receiptRules: ValidationRule[] = [
    {
      field: 'store',
      required: true,
      minLength: 2,
      maxLength: 100,
      errorMessage: 'Le nom du magasin est requis (2-100 caractères)'
    },
    {
      field: 'date',
      required: true,
      customValidator: (value) => {
        const date = new Date(value);
        return !isNaN(date.getTime()) && date <= new Date();
      },
      errorMessage: 'Veuillez entrer une date valide (pas dans le futur)'
    },
    {
      field: 'items',
      required: true,
      customValidator: (value) => Array.isArray(value) && value.length > 0,
      errorMessage: 'Le reçu doit contenir au moins un article'
    },
    {
      field: 'total',
      required: true,
      pattern: /^\d+(\s\d+)*\sF\sCFA$/,
      errorMessage: 'Le total doit être au format "18 450 F CFA"'
    }
  ];

  constructor() {}

  // Valider le profil utilisateur
  validateUserProfile(data: UserProfileData): ValidationResult {
    return this.validateData(data, this.userProfileRules);
  }

  // Valider une promotion
  validatePromotion(data: PromotionData): ValidationResult {
    return this.validateData(data, this.promotionRules);
  }

  // Valider un reçu
  validateReceipt(data: ReceiptData): ValidationResult {
    return this.validateData(data, this.receiptRules);
  }

  // Validation générique avec règles personnalisées
  validateData(data: any, rules: ValidationRule[]): ValidationResult {
    const result: ValidationResult = {
      isValid: true,
      errors: [],
      fieldErrors: {}
    };

    for (const rule of rules) {
      const value = data[rule.field];
      const fieldErrors: string[] = [];

      // Validation required
      if (rule.required && (!value || value === '')) {
        fieldErrors.push(`${rule.field} est requis`);
        result.isValid = false;
        continue;
      }

      // Si la valeur n'est pas requise et est vide, passer à la règle suivante
      if (!rule.required && (!value || value === '')) {
        continue;
      }

      // Validation minLength
      if (rule.minLength && typeof value === 'string' && value.length < rule.minLength) {
        fieldErrors.push(`${rule.field} doit contenir au moins ${rule.minLength} caractères`);
        result.isValid = false;
      }

      // Validation maxLength
      if (rule.maxLength && typeof value === 'string' && value.length > rule.maxLength) {
        fieldErrors.push(`${rule.field} doit contenir au maximum ${rule.maxLength} caractères`);
        result.isValid = false;
      }

      // Validation pattern
      if (rule.pattern && typeof value === 'string' && !rule.pattern.test(value)) {
        fieldErrors.push(rule.errorMessage);
        result.isValid = false;
      }

      // Validation personnalisée
      if (rule.customValidator) {
        try {
          if (!rule.customValidator(value, data)) {
            fieldErrors.push(rule.errorMessage);
            result.isValid = false;
          }
        } catch (error) {
          fieldErrors.push(`Erreur de validation pour ${rule.field}`);
          result.isValid = false;
        }
      }

      // Ajouter les erreurs du champ
      if (fieldErrors.length > 0) {
        result.fieldErrors[rule.field] = fieldErrors;
        result.errors.push(...fieldErrors);
      }
    }

    return result;
  }

  // Valider un email
  validateEmail(email: string): boolean {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
  }

  // Valider un numéro de téléphone
  validatePhone(phone: string): boolean {
    const phonePattern = /^(\+225|225)?[0-9]{8,10}$/;
    return phonePattern.test(phone);
  }

  // Valider un mot de passe
  validatePassword(password: string): { isValid: boolean; strength: string; suggestions: string[] } {
    const suggestions: string[] = [];
    let score = 0;

    if (password.length >= 8) score++;
    else suggestions.push('Le mot de passe doit contenir au moins 8 caractères');

    if (/[a-z]/.test(password)) score++;
    else suggestions.push('Ajoutez au moins une lettre minuscule');

    if (/[A-Z]/.test(password)) score++;
    else suggestions.push('Ajoutez au moins une lettre majuscule');

    if (/[0-9]/.test(password)) score++;
    else suggestions.push('Ajoutez au moins un chiffre');

    if (/[^A-Za-z0-9]/.test(password)) score++;
    else suggestions.push('Ajoutez au moins un caractère spécial');

    let strength: string;
    if (score < 3) strength = 'faible';
    else if (score < 5) strength = 'moyen';
    else strength = 'fort';

    return {
      isValid: score >= 4,
      strength,
      suggestions: score >= 4 ? [] : suggestions
    };
  }

  // Valider un montant
  validateAmount(amount: string | number): boolean {
    const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
    return !isNaN(numAmount) && numAmount >= 0;
  }

  // Valider une date
  validateDate(date: string | Date): boolean {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return !isNaN(dateObj.getTime());
  }

  // Valider une URL
  validateUrl(url: string): boolean {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  // Nettoyer et valider les données d'entrée
  sanitizeInput(input: string): string {
    return input
      .trim()
      .replace(/[<>]/g, '') // Supprimer les balises HTML basiques
      .replace(/\s+/g, ' '); // Normaliser les espaces
  }

  // Valider un code-barres
  validateBarcode(barcode: string): boolean {
    // Code-barres EAN-13 (13 chiffres)
    if (/^\d{13}$/.test(barcode)) {
      return this.validateEAN13(barcode);
    }
    
    // Code-barres UPC-A (12 chiffres)
    if (/^\d{12}$/.test(barcode)) {
      return this.validateUPCA(barcode);
    }
    
    // Code-barres Code 128 (variable)
    if (/^[A-Za-z0-9\-\.\/\+\s]{1,48}$/.test(barcode)) {
      return true;
    }
    
    return false;
  }

  // Valider un code EAN-13
  private validateEAN13(barcode: string): boolean {
    if (barcode.length !== 13) return false;
    
    let sum = 0;
    for (let i = 0; i < 12; i++) {
      const digit = parseInt(barcode[i]);
      sum += digit * (i % 2 === 0 ? 1 : 3);
    }
    
    const checkDigit = (10 - (sum % 10)) % 10;
    return checkDigit === parseInt(barcode[12]);
  }

  // Valider un code UPC-A
  private validateUPCA(barcode: string): boolean {
    if (barcode.length !== 12) return false;
    
    let sum = 0;
    for (let i = 0; i < 11; i++) {
      const digit = parseInt(barcode[i]);
      sum += digit * (i % 2 === 0 ? 1 : 3);
    }
    
    const checkDigit = (10 - (sum % 10)) % 10;
    return checkDigit === parseInt(barcode[11]);
  }

  // Obtenir les messages d'erreur formatés
  getFormattedErrors(validationResult: ValidationResult): string {
    if (validationResult.isValid) {
      return 'Validation réussie';
    }
    
    return validationResult.errors.join('\n');
  }

  // Vérifier si un champ a des erreurs
  hasFieldErrors(validationResult: ValidationResult, fieldName: string): boolean {
    return !!(validationResult.fieldErrors[fieldName] && validationResult.fieldErrors[fieldName].length > 0);
  }

  // Obtenir les erreurs d'un champ spécifique
  getFieldErrors(validationResult: ValidationResult, fieldName: string): string[] {
    return validationResult.fieldErrors[fieldName] || [];
  }
}
