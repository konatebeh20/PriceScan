import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatErrorModule } from '@angular/material/form-field'; // Added for mat-error
import { PriceService } from '../../services/price.service';

@Component({
  selector: 'app-image-upload',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule, MatProgressSpinnerModule, MatErrorModule], // Added MatErrorModule
  templateUrl: './image-upload.component.html',
  styleUrls: ['./image-upload.component.scss']
})
export class ImageUploadComponent {
  selectedFile: File | null = null;
  previewUrl: string | ArrayBuffer | null = null; // Explicitly typed to handle null
  uploading: boolean = false;
  error: string = '';

  constructor(private priceService: PriceService) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.selectedFile = input.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) {
          this.previewUrl = e.target.result as string | ArrayBuffer; // Type assertion
        }
      };
      reader.readAsDataURL(this.selectedFile);
      this.error = '';
    }
  }

  uploadImage() {
    if (this.selectedFile) {
      this.uploading = true;
      this.error = '';
      this.priceService.uploadImage(this.selectedFile).subscribe({
        next: (response) => {
          this.uploading = false;
          this.selectedFile = null;
          this.previewUrl = null;
          console.log('Image uploaded:', response);
        },
        error: () => {
          this.error = "Échec du téléchargement de l'image";
          this.uploading = false;
        }
      });
    }
  }
}