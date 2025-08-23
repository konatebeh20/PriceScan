import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
import { ReceiptService, Receipt, ReceiptScanResult } from '../../services/receipt.service';
import { StorageService } from '../../services/storage.service';
import { AlertController, LoadingController, ToastController, ModalController } from '@ionic/angular';
import { ReceiptDetailModalComponent } from '../receipt-detail-modal/receipt-detail-modal.component';
import { CommonModule } from '@angular/common';
import { 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonContent, 
  IonButton, 
  IonIcon, 
  IonSpinner, 
  IonBackButton, 
  IonButtons
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-receipt-scanner',
  templateUrl: './receipt-scanner.component.html',
  styleUrls: ['./receipt-scanner.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    ReceiptDetailModalComponent,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonButton,
    IonIcon,
    IonSpinner,
    IonBackButton,
    IonButtons
  ]
})
export class ReceiptScannerComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef;
  
  capturedImage: string | null = null;
  isScanning = false;
  scanResult: ReceiptScanResult | null = null;
  userId = 'user123'; // À remplacer par l'ID utilisateur réel

  constructor(
    private receiptService: ReceiptService,
    private storageService: StorageService,
    private alertController: AlertController,
    private loadingController: LoadingController,
    private toastController: ToastController,
    private modalController: ModalController
  ) { }

  ngOnInit() {}

  // Prendre une photo avec la caméra
  async takePicture() {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: CameraResultType.DataUrl,
        source: CameraSource.Camera
      });

      if (image.dataUrl) {
        this.capturedImage = image.dataUrl;
        await this.scanReceipt(image.dataUrl);
      }
    } catch (error) {
      console.error('Erreur lors de la prise de photo:', error);
      this.showToast('Erreur lors de la prise de photo', 'danger');
    }
  }

  // Sélectionner une image depuis la galerie
  async selectFromGallery() {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: CameraResultType.DataUrl,
        source: CameraSource.Photos
      });

      if (image.dataUrl) {
        this.capturedImage = image.dataUrl;
        await this.scanReceipt(image.dataUrl);
      }
    } catch (error) {
      console.error('Erreur lors de la sélection d\'image:', error);
      this.showToast('Erreur lors de la sélection d\'image', 'danger');
    }
  }

  // Scanner le reçu avec l'API OCR
  async scanReceipt(imageDataUrl: string) {
    this.isScanning = true;
    const loading = await this.loadingController.create({
      message: 'Analyse du reçu en cours...'
    });
    await loading.present();

    try {
      // Convertir DataURL en File
      const response = await fetch(imageDataUrl);
      const blob = await response.blob();
      const file = new File([blob], 'receipt.jpg', { type: 'image/jpeg' });

      // Envoyer au service de scan
      this.receiptService.scanReceipt(file).subscribe({
        next: (result) => {
          this.scanResult = result;
          if (result.success && result.data) {
            this.showReceiptDetail(result.data);
          } else {
            this.showScanError(result.error || 'Erreur lors de l\'analyse du reçu');
          }
        },
        error: (error) => {
          console.error('Erreur API:', error);
          this.showScanError('Erreur de connexion au serveur');
        }
      });
    } catch (error) {
      console.error('Erreur lors du scan:', error);
      this.showScanError('Erreur lors du traitement de l\'image');
    } finally {
      this.isScanning = false;
      await loading.dismiss();
    }
  }

  // Afficher le modal de détail du reçu
  async showReceiptDetail(receipt: Receipt) {
    const modal = await this.modalController.create({
      component: ReceiptDetailModalComponent,
      componentProps: {
        receipt: receipt,
        isNewReceipt: true
      }
    });

    modal.present();

    const { data } = await modal.onWillDismiss();
    if (data && data.saved) {
      await this.saveReceipt(receipt);
      this.showToast('Reçu sauvegardé avec succès!', 'success');
      this.resetScanner();
    }
  }

  // Sauvegarder le reçu
  async saveReceipt(receipt: Receipt) {
    try {
      // Ajouter l'ID utilisateur
      receipt.userId = this.userId;
      
      // Sauvegarder localement
      await this.storageService.saveReceipt(receipt);
      
      // Sauvegarder sur le serveur
      this.receiptService.saveReceipt(receipt).subscribe({
        next: (savedReceipt) => {
          console.log('Reçu sauvegardé sur le serveur:', savedReceipt);
        },
        error: (error) => {
          console.error('Erreur lors de la sauvegarde sur le serveur:', error);
          // Le reçu est déjà sauvegardé localement
        }
      });
    } catch (error) {
      console.error('Erreur lors de la sauvegarde locale:', error);
      this.showToast('Erreur lors de la sauvegarde', 'danger');
    }
  }

  // Afficher une erreur de scan
  async showScanError(message: string) {
    const alert = await this.alertController.create({
      header: 'Erreur de scan',
      message: message,
      buttons: [
        {
          text: 'Réessayer',
          handler: () => {
            this.resetScanner();
          }
        },
        {
          text: 'Annuler',
          role: 'cancel'
        }
      ]
    });
    await alert.present();
  }

  // Réinitialiser le scanner
  resetScanner() {
    this.capturedImage = null;
    this.scanResult = null;
    this.isScanning = false;
  }

  // Afficher un toast
  async showToast(message: string, color: string = 'primary') {
    const toast = await this.toastController.create({
      message: message,
      duration: 3000,
      color: color,
      position: 'bottom'
    });
    await toast.present();
  }

  // Ouvrir le sélecteur de fichiers
  openFileInput() {
    this.fileInput.nativeElement.click();
  }

  // Gérer la sélection de fichier
  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.capturedImage = e.target.result;
        this.scanReceipt(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }
}
