import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.page.html',
  styleUrls: ['./auth.page.scss'],
  standalone: true,
  imports: [CommonModule, IonicModule, ReactiveFormsModule]
})
export class AuthPage {
  
  isLogin = true;
  loginForm: FormGroup;
  registerForm: FormGroup;
  
  constructor(
    private router: Router,
    private formBuilder: FormBuilder
  ) {
    this.initForms();
  }
  
  initForms() {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
    
    this.registerForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
  }
  
  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password');
    const confirmPassword = form.get('confirmPassword');
    
    if (password && confirmPassword && password.value !== confirmPassword.value) {
      confirmPassword.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    
    return null;
  }
  
  toggleMode() {
    this.isLogin = !this.isLogin;
  }
  
  async onLogin() {
    if (this.loginForm.valid) {
      // TODO: Implémenter la logique de connexion
      console.log('Login:', this.loginForm.value);
      this.router.navigate(['/user']);
    }
  }
  
  async onRegister() {
    if (this.registerForm.valid) {
      // TODO: Implémenter la logique d'inscription
      console.log('Register:', this.registerForm.value);
      this.router.navigate(['/user']);
    }
  }
  
  // Aller directement à l'app (pour les tests)
  skipAuth() {
    this.router.navigate(['/user']);
  }
}
