import { Component, OnInit } from '@angular/core';
import { ReceiptService, Receipt } from '../../services/receipt.service';
import { StorageService } from '../../services/storage.service';
import { ModalController, AlertController, ToastController } from '@ionic/angular';
import { ReceiptDetailModalComponent } from '../receipt-detail-modal/receipt-detail-modal.component';
import { CommonModule } from '@angular/common';
import { 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonContent, 
  IonButton, 
  IonIcon, 
  IonCard, 
  IonCardHeader, 
  IonCardTitle, 
  IonCardContent, 
  IonItem, 
  IonLabel, 
  IonNote, 
  IonFab, 
  IonFabButton, 
  IonSpinner,
  IonButtons
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-receipt-list',
  templateUrl: './receipt-list.component.html',
  styleUrls: ['./receipt-list.component.scss'],
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
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonItem,
    IonLabel,
    IonNote,
    IonFab,
    IonFabButton,
    IonSpinner,
    IonButtons
  ]
})
export class ReceiptListComponent implements OnInit {
  receipts: Receipt[] = [];
  isLoading = false;
  userId = 'user123'; // À remplacer par l'ID utilisateur réel

  constructor(
    private receiptService: ReceiptService,
    private storageService: StorageService,
    private modalController: ModalController,
    private alertController: AlertController,
    private toastController: ToastController
  ) {}

  ngOnInit() {
    this.loadReceipts();
  }

  async loadReceipts() {
    this.isLoading = true;
    
    try {
      // Charger depuis le stockage local
      this.receipts = await this.storageService.getReceipts();
      
      // Synchroniser avec le serveur
      this.syncWithServer();
    } catch (error) {
      console.error('Erreur lors du chargement des reçus:', error);
      this.showToast('Erreur lors du chargement des reçus', 'danger');
    } finally {
      this.isLoading = false;
    }
  }

  async syncWithServer() {
    try {
      // Charger depuis le serveur
      this.receiptService.getUserReceipts(this.userId).subscribe({
        next: (serverReceipts) => {
          // Fusionner avec les reçus locaux
          this.mergeReceipts(serverReceipts);
        },
        error: (error) => {
          console.error('Erreur lors de la synchronisation:', error);
        }
      });
    } catch (error) {
      console.error('Erreur lors de la synchronisation:', error);
    }
  }

  mergeReceipts(serverReceipts: Receipt[]) {
    // Créer un map des reçus locaux par ID
    const localReceiptsMap = new Map(this.receipts.map(r => [r.id, r]));
    
    // Mettre à jour ou ajouter les reçus du serveur
    serverReceipts.forEach(serverReceipt => {
      if (serverReceipt.id) {
        localReceiptsMap.set(serverReceipt.id, serverReceipt);
      }
    });
    
    // Convertir le map en array et trier par date
    this.receipts = Array.from(localReceiptsMap.values())
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    
    // Sauvegarder localement
    this.saveReceiptsLocally();
  }

  async saveReceiptsLocally() {
    try {
      // Vider le stockage local
      await this.storageService.clear();
      
      // Sauvegarder tous les reçus
      for (const receipt of this.receipts) {
        await this.storageService.saveReceipt(receipt);
      }
    } catch (error) {
      console.error('Erreur lors de la sauvegarde locale:', error);
    }
  }

  async viewReceipt(receipt: Receipt) {
    const modal = await this.modalController.create({
      component: ReceiptDetailModalComponent,
      componentProps: {
        receipt: receipt,
        isNewReceipt: false
      }
    });

    modal.present();

    const { data } = await modal.onWillDismiss();
    if (data && data.saved) {
      // Mettre à jour le reçu
      await this.updateReceipt(data.receipt);
    }
  }

  async updateReceipt(updatedReceipt: Receipt) {
    try {
      // Mettre à jour localement
      await this.storageService.updateReceipt(updatedReceipt.id!, updatedReceipt);
      
      // Mettre à jour dans la liste
      const index = this.receipts.findIndex(r => r.id === updatedReceipt.id);
      if (index !== -1) {
        this.receipts[index] = updatedReceipt;
      }
      
      // Synchroniser avec le serveur
      this.receiptService.updateReceipt(updatedReceipt.id!, updatedReceipt).subscribe();
      
      this.showToast('Reçu mis à jour avec succès!', 'success');
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
      this.showToast('Erreur lors de la mise à jour', 'danger');
    }
  }

  async deleteReceipt(receipt: Receipt) {
    const alert = await this.alertController.create({
      header: 'Confirmer la suppression',
      message: `Êtes-vous sûr de vouloir supprimer le reçu de ${receipt.storeName} ?`,
      buttons: [
        {
          text: 'Annuler',
          role: 'cancel'
        },
        {
          text: 'Supprimer',
          role: 'destructive',
          handler: () => {
            this.performDelete(receipt);
          }
        }
      ]
    });
    
    await alert.present();
  }

  async performDelete(receipt: Receipt) {
    try {
      // Supprimer localement
      await this.storageService.deleteReceipt(receipt.id!);
      
      // Supprimer de la liste
      this.receipts = this.receipts.filter(r => r.id !== receipt.id);
      
      // Supprimer du serveur
      if (receipt.id) {
        this.receiptService.deleteReceipt(receipt.id).subscribe();
      }
      
      this.showToast('Reçu supprimé avec succès!', 'success');
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
      this.showToast('Erreur lors de la suppression', 'danger');
    }
  }

  async refreshReceipts() {
    await this.loadReceipts();
  }

  // Formatage de la date
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  // Formatage du prix
  formatPrice(price: number): string {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR'
    }).format(price);
  }

  // Calculer le total des dépenses
  getTotalSpent(): number {
    return this.receipts.reduce((total, receipt) => total + receipt.totalAmount, 0);
  }

  // Obtenir le nombre de magasins visités
  getUniqueStores(): string[] {
    const stores = new Set(this.receipts.map(r => r.storeName));
    return Array.from(stores);
  }

  // Afficher un toast
  async showToast(message: string, color: string = 'primary') {
    const toast = await this.toastController.create({
      message,
      duration: 3000,
      color,
      position: 'bottom'
    });
    await toast.present();
  }
}
