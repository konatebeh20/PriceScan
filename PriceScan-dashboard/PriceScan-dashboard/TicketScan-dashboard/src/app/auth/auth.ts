import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

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
  
  // Sample users for demo
  private users = [
    {
      email: 'konatebeh20@gmail.com',
      password: 'scan123',
      firstName: 'Konaté',
      lastName: 'Beh',
      accountType: 'particulier'
    }
  ];

  constructor(private router: Router) {}

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
    
    // Simulate API call
    setTimeout(() => {
      const user = this.users.find(u => 
        u.email === this.loginForm.email && u.password === this.loginForm.password
      );
      
      if (user) {
        // Store user data
        const userData = {
          username: `${user.firstName} ${user.lastName}`,
          email: user.email,
          accountType: user.accountType,
          createdAt: new Date(),
          lastLogin: new Date()
        };
        
        sessionStorage.setItem('ticketscan_current_user', JSON.stringify(userData));
        
        // Redirect to dashboard
        this.router.navigate(['/dashboard']);
      } else {
        this.formErrors['loginPassword'] = 'Email ou mot de passe incorrect';
      }
      
      this.isLoading = false;
    }, 1000);
  }

  handleRegister() {
    this.clearFormErrors();
    
    // Validate required fields
    if (!this.registerForm.firstName) {
      this.formErrors['registerFirstName'] = 'Le prénom est requis';
    }
    if (!this.registerForm.lastName) {
      this.formErrors['registerLastName'] = 'Le nom est requis';
    }
    if (!this.registerForm.email) {
      this.formErrors['registerEmail'] = 'L\'email est requis';
    }
    if (!this.registerForm.accountType) {
      this.formErrors['registerAccountType'] = 'Le type de compte est requis';
    }
    if (!this.registerForm.password) {
      this.formErrors['registerPassword'] = 'Le mot de passe est requis';
    }
    if (!this.registerForm.confirmPassword) {
      this.formErrors['registerConfirmPassword'] = 'La confirmation du mot de passe est requise';
    }
    
    // Check if there are any errors
    if (Object.keys(this.formErrors).some(key => this.formErrors[key])) {
      return;
    }
    
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
    
    // Validate password strength
    if (this.passwordStrength.class === 'weak') {
      this.formErrors['registerPassword'] = 'Le mot de passe est trop faible';
      return;
    }

    this.isLoading = true;
    
    // Simulate API call
    setTimeout(() => {
      // Check if email already exists
      const existingUser = this.users.find(u => u.email === this.registerForm.email);
      if (existingUser) {
        this.formErrors['registerEmail'] = 'Cet email est déjà utilisé';
        this.isLoading = false;
        return;
      }
      
      // Create new user
      const newUser = {
        email: this.registerForm.email,
        password: this.registerForm.password,
        firstName: this.registerForm.firstName,
        lastName: this.registerForm.lastName,
        accountType: this.registerForm.accountType
      };
      
      this.users.push(newUser);
      
      // Auto-login after registration
      const userData = {
        username: `${newUser.firstName} ${newUser.lastName}`,
        email: newUser.email,
        accountType: newUser.accountType,
        createdAt: new Date(),
        lastLogin: new Date()
      };
      
      sessionStorage.setItem('ticketscan_current_user', JSON.stringify(userData));
      
      // Redirect to dashboard
      this.router.navigate(['/dashboard']);
      
      this.isLoading = false;
    }, 1500);
  }

  checkPasswordStrength() {
    const password = this.registerForm.password;
    
    if (!password) {
      this.passwordStrength = { text: '', class: '' };
      return;
    }
    
    let score = 0;
    let feedback = '';
    
    // Length check
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    
    // Character variety checks
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    
    // Determine strength
    if (score <= 2) {
      feedback = 'Faible';
      this.passwordStrength = { text: feedback, class: 'weak' };
    } else if (score <= 4) {
      feedback = 'Moyen';
      this.passwordStrength = { text: feedback, class: 'medium' };
    } else {
      feedback = 'Fort';
      this.passwordStrength = { text: feedback, class: 'strong' };
    }
  }

  showForgotPassword() {
    alert('Fonctionnalité de récupération de mot de passe\n\nCette fonctionnalité sera bientôt disponible.\n\nEn attendant, vous pouvez contacter le support à support@ticketscan.com');
  }

  clearFormErrors() {
    this.formErrors = {};
  }
}
