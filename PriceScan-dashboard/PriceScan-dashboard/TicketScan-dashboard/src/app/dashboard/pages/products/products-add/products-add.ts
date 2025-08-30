import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-products-add',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './products-add.html',
  styleUrls: ['./products-add.scss']
})
export class ProductsAddComponent implements OnInit {
  
  // Form data
  productForm = {
    product_name: '',
    product_barcode: '',
    product_description: '',
    product_category_id: '',
    product_store_id: '',
    product_price: '',
    product_unit: 'piece',
    product_image: '',
    product_status: 'active'
  };

  // Available options
  categories: any[] = [
    { id: 1, category_name: 'Alimentation' },
    { id: 2, category_name: 'Électronique' },
    { id: 3, category_name: 'Vêtements' }
  ];
  
  stores: any[] = [
    { id: 1, store_name: 'Carrefour' },
    { id: 2, store_name: 'Pharmacie' },
    { id: 3, store_name: 'Boutique' }
  ];
  
  // Form state
  isSubmitting = false;
  showSuccessMessage = false;
  showErrorMessage = false;
  errorMessage = '';

  constructor() { }

  ngOnInit(): void {
  }

  // Handle form submission
  onSubmit(): void {
    if (this.isSubmitting) return;

    this.isSubmitting = true;
    this.hideMessages();

    // Simulate API call
    setTimeout(() => {
      this.showSuccessMessage = true;
      this.resetForm();
      this.isSubmitting = false;
      console.log(' Produit créé avec succès:', this.productForm);
    }, 1000);
  }

  // Reset form
  resetForm(): void {
    this.productForm = {
      product_name: '',
      product_barcode: '',
      product_description: '',
      product_category_id: '',
      product_store_id: '',
      product_price: '',
      product_unit: 'piece',
      product_image: '',
      product_status: 'active'
    };
  }

  // Hide messages
  hideMessages(): void {
    this.showSuccessMessage = false;
    this.showErrorMessage = false;
    this.errorMessage = '';
  }

  // Handle image upload
  onImageUpload(event: any): void {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.productForm.product_image = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }

  // Remove image
  removeImage(): void {
    this.productForm.product_image = '';
  }
}
