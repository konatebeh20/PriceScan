import { Component, Input, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';
import { Receipt, ReceiptItem } from '../../services/receipt.service';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';
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
  IonCardSubtitle,
  IonItem, 
  IonLabel, 
  IonInput, 
  IonRow, 
  IonCol, 
  IonItemDivider,
  IonButtons,
  IonList,
  IonNote
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-receipt-detail-modal',
  templateUrl: './receipt-detail-modal.component.html',
  styleUrls: ['./receipt-detail-modal.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
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
    IonCardSubtitle,
    IonItem,
    IonLabel,
    IonInput,
    IonRow,
    IonCol,
    IonItemDivider,
    IonButtons,
    IonList,
    IonNote
  ]
})
export class ReceiptDetailModalComponent implements OnInit {
  @Input() receipt!: Receipt;
  @Input() isNewReceipt: boolean = false;

  receiptForm!: FormGroup;
  isEditing = false;

  constructor(
    private modalController: ModalController,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit() {
    this.initForm();
  }

  initForm() {
    this.receiptForm = this.formBuilder.group({
      storeName: [this.receipt.storeName, Validators.required],
      date: [this.receipt.date, Validators.required],
      totalAmount: [this.receipt.totalAmount, [Validators.required, Validators.min(0)]],
      items: this.formBuilder.array([])
    });

    // Ajouter les articles existants au formulaire
    if (this.receipt.items && this.receipt.items.length > 0) {
      this.receipt.items.forEach(item => {
        this.addItem(item);
      });
    } else {
      // Ajouter un article vide par défaut
      this.addItem();
    }
  }

  get itemsFormArray() {
    return this.receiptForm.get('items') as FormArray;
  }

  addItem(item?: ReceiptItem) {
    const itemForm = this.formBuilder.group({
      name: [item?.name || '', Validators.required],
      quantity: [item?.quantity || 1, [Validators.required, Validators.min(1)]],
      unitPrice: [item?.unitPrice || 0, [Validators.required, Validators.min(0)]],
      totalPrice: [item?.totalPrice || 0, [Validators.required, Validators.min(0)]],
      category: [item?.category || '']
    });

    // Calculer automatiquement le prix total
    itemForm.get('quantity')?.valueChanges.subscribe(quantity => {
      const unitPrice = itemForm.get('unitPrice')?.value || 0;
      if (quantity !== null) {
        itemForm.patchValue({ totalPrice: quantity * unitPrice });
      }
    });

    itemForm.get('unitPrice')?.valueChanges.subscribe(unitPrice => {
      const quantity = itemForm.get('quantity')?.value || 1;
      if (unitPrice !== null) {
        itemForm.patchValue({ totalPrice: quantity * unitPrice });
      }
    });

    this.itemsFormArray.push(itemForm);
  }

  removeItem(index: number) {
    this.itemsFormArray.removeAt(index);
    this.calculateTotal();
  }

  calculateTotal() {
    const items = this.receiptForm.get('items')?.value || [];
    const total = items.reduce((sum: number, item: any) => sum + (item.totalPrice || 0), 0);
    this.receiptForm.patchValue({ totalAmount: total });
  }

  toggleEditing() {
    this.isEditing = !this.isEditing;
  }

  saveReceipt() {
    if (this.receiptForm.valid) {
      const formValue = this.receiptForm.value;
      
      // Mettre à jour le reçu
      this.receipt = {
        ...this.receipt,
        storeName: formValue.storeName,
        date: formValue.date,
        totalAmount: formValue.totalAmount,
        items: formValue.items
      };

      // Fermer le modal avec le reçu mis à jour
      this.modalController.dismiss(this.receipt, 'saved');
    }
  }

  closeModal() {
    this.modalController.dismiss(null, 'cancelled');
  }

  // Formatage de la date
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
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
}
