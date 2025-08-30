import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../dashboard/services/auth/auth';

interface LoginForm {
  email: string;
  password: string;
}

interface RegisterForm {
  firstName: string;
  lastName: string;
  email: string;
  accountType: string;
  password: string;
  confirmPassword: string;
}

interface PasswordStrength {
  text: string;
  class: string;
}

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auth.html',
  styleUrls: ['./auth.scss']
})
export class AuthComponent implements OnInit {
  currentTab: 'login' | 'register' = 'login';
  isLoading = false;
  
  loginForm: LoginForm = {
    email: '',
    password: ''
  };
  
  registerForm: RegisterForm = {
    firstName: '',
    lastName: '',
    email: '',
    accountType: '',
    password: '',
    confirmPassword: ''
  };
  
  formErrors: { [key: string]: string } = {};
  passwordStrength: PasswordStrength = { text: '', class: '' };
  
  // Aucun utilisateur statique - tous les utilisateurs viennent de la base de données

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit() {
    // Check if user is already logged in
    const currentUser = sessionStorage.getItem('ticketscan_current_user');
    if (currentUser) {
      this.router.navigate(['/dashboard']);
    }
  }

  switchTab(tab: 'login' | 'register') {
    this.currentTab = tab;
    this.clearFormErrors();
  }

  handleLogin() {
    this.clearFormErrors();
    
    if (!this.loginForm.email || !this.loginForm.password) {
      this.formErrors['loginEmail'] = !this.loginForm.email ? 'L\'email est requis' : '';
      this.formErrors['loginPassword'] = !this.loginForm.password ? 'Le mot de passe est requis' : '';
      return;
    }

    this.isLoading = true;
    
    // Appel réel à l'API PriceScan
    // L'API accepte soit username soit email pour la connexion
    this.authService.login({
      email: this.loginForm.email,
      password: this.loginForm.password
    }).subscribe({
      next: (response) => {
        if (response.success) {
          // Connexion réussie
          this.router.navigate(['/dashboard']);
        } else {
          // Erreur de connexion
          this.formErrors['loginPassword'] = response.message || 'Email ou mot de passe incorrect';
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Erreur de connexion:', error);
        this.formErrors['loginPassword'] = 'Erreur de connexion au serveur';
        this.isLoading = false;
      }
    });
  }

  handleRegister() {
    this.clearFormErrors();
    console.log(' Début de la validation d\'inscription...');
    
    // Validate required fields
    if (!this.registerForm.firstName) {
      this.formErrors['registerFirstName'] = 'Le prénom est requis';
      console.log(' Prénom manquant');
    }
    if (!this.registerForm.lastName) {
      this.formErrors['registerLastName'] = 'Le nom est requis';
      console.log(' Nom manquant');
    }
    if (!this.registerForm.email) {
      this.formErrors['registerEmail'] = 'L\'email est requis';
      console.log(' Email manquant');
    }
    if (!this.registerForm.accountType) {
      this.formErrors['registerAccountType'] = 'Le type de compte est requis';
      console.log(' Type de compte manquant');
    }
    if (!this.registerForm.password) {
      this.formErrors['registerPassword'] = 'Le mot de passe est requis';
      console.log(' Mot de passe manquant');
    }
    if (!this.registerForm.confirmPassword) {
      this.formErrors['registerConfirmPassword'] = 'La confirmation du mot de passe est requise';
      console.log(' Confirmation mot de passe manquante');
    }
    
    // Check if there are any errors
    if (Object.keys(this.formErrors).some(key => this.formErrors[key])) {
      console.log(' Erreurs de validation détectées:', this.formErrors);
      return;
    }
    
    console.log(' Validation réussie, appel de l\'API...');
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.registerForm.email)) {
      this.formErrors['registerEmail'] = 'Format d\'email invalide';
      return;
    }
    
    // Validate password confirmation
    if (this.registerForm.password !== this.registerForm.confirmPassword) {
      this.formErrors['registerConfirmPassword'] = 'Les mots de passe ne correspondent pas';
      return;
    }
    
    // Validation simple du mot de passe - au moins 6 caractères
    if (this.registerForm.password.length < 6) {
      this.formErrors['registerPassword'] = 'Le mot de passe doit contenir au moins 6 caractères';
      return;
    }

    this.isLoading = true;
    
    // Appel réel à l'API PriceScan
    console.log(' Tentative d\'inscription avec:', {
      firstname: this.registerForm.firstName,
      lastname: this.registerForm.lastName,
      email: this.registerForm.email,
      password: this.registerForm.password,
      accountType: this.registerForm.accountType
    });
    
    // Créer un username unique basé sur l'email
    const username = this.registerForm.email.split('@')[0] + '_' + Date.now();
    
    this.authService.register({
      firstname: this.registerForm.firstName,
      lastname: this.registerForm.lastName,
      username: username,
      email: this.registerForm.email,
      password: this.registerForm.password,
      accountType: this.registerForm.accountType as 'particulier' | 'supermarche' | 'pharmacie' | 'quincaillerie' | 'autre'
    }).subscribe({
      next: (response) => {
        console.log('📡 Réponse de l\'API:', response);
        if (response.success) {
          // Inscription réussie, redirection vers le dashboard
          console.log(' Inscription réussie, redirection...');
          this.router.navigate(['/dashboard']);
        } else {
          // Erreur d'inscription
          if (response.errors && response.errors.length > 0) {
            response.errors.forEach(error => {
              if (error.includes('email')) {
                this.formErrors['registerEmail'] = error;
              } else if (error.includes('mot de passe')) {
                this.formErrors['registerPassword'] = error;
              }
            });
          } else {
            this.formErrors['registerEmail'] = response.message || 'Erreur lors de l\'inscription';
          }
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Erreur d\'inscription:', error);
        this.formErrors['registerEmail'] = error;
        this.isLoading = false;
      }
    });
  }

  checkPasswordStrength() {
    const password = this.registerForm.password;
    
    if (!password) {
      this.passwordStrength = { text: '', class: '' };
      return;
    }
    
    // Validation simple - afficher la force sans bloquer l'inscription
    if (password.length < 6) {
      this.passwordStrength = { text: 'Trop court', class: 'weak' };
    } else if (password.length < 8) {
      this.passwordStrength = { text: 'Moyen', class: 'medium' };
    } else {
      this.passwordStrength = { text: 'Fort', class: 'strong' };
    }
  }

  showForgotPassword() {
    alert('Fonctionnalité de récupération de mot de passe\n\nCette fonctionnalité sera bientôt disponible.\n\nEn attendant, vous pouvez contacter le support à support@ticketscan.com');
  }

  clearFormErrors() {
    this.formErrors = {};
  }
}
