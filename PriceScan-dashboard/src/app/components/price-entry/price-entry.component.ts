import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PriceService } from '../../services/price.service';

@Component({
  selector: 'app-price-entry',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './price-entry.component.html',
  styleUrls: ['./price-entry.component.scss']
})
export class PriceEntryComponent {
  priceForm: FormGroup;
  loading: boolean = false;
  error: string = '';
  success: boolean = false;

  constructor(private fb: FormBuilder, private priceService: PriceService) {
    this.priceForm = this.fb.group({
      productCode: ['', Validators.required],
      price: [0, [Validators.required, Validators.min(0.01)]],
      store: ['', Validators.required]
    });
  }

  submitPrice() {
    if (this.priceForm.valid) {
      this.loading = true;
      this.error = '';
      this.success = false;
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const data = {
            ...this.priceForm.value,
            date: new Date(),
            location: { lat: position.coords.latitude, lng: position.coords.longitude }
          };
          this.priceService.savePrice(data).subscribe({
            next: () => {
              this.loading = false;
              this.success = true;
              this.priceForm.reset();
            },
            error: () => {
              this.error = "Échec de l'enregistrement du prix";
              this.loading = false;
            }
          });
        },
        () => {
          this.error = "Échec de la récupération de la localisation";
          this.loading = false;
        }
      );
    }
  }
}