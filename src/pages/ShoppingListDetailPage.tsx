import React from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButtons,
  IonBackButton, IonList, IonItem, IonLabel, IonCheckbox, IonButton, useIonRouter
} from '@ionic/react';
import { useParams } from 'react-router-dom';

const FAKE_DETAIL_DATA: { [key: string]: string[] } = {
  '1': ['Lait', 'Pain', 'Œufs', 'Fromage'],
  '2': ['Gâteau', 'Bougies', 'Cadeau', 'Cartes d\'invitation'],
};

const ShoppingListDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const router = useIonRouter();
  const items = FAKE_DETAIL_DATA[id] || [];

  const goToOptimalBasket = () => {
    router.push(`/tabs/optimal-basket/${id}`);
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonButtons slot="start">
            <IonBackButton defaultHref="/tabs/lists" />
          </IonButtons>
          <IonTitle>Détail de la Liste</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <div className="ion-padding">
          <IonButton expand="full" onClick={goToOptimalBasket}>
            Calculer le Panier Optimal
          </IonButton>
        </div>
        <IonList>
          {items.map(item => (
            <IonItem key={item}>
              <IonCheckbox slot="start" />
              <IonLabel>{item}</IonLabel>
            </IonItem>
          ))}
        </IonList>
      </IonContent>
    </IonPage>
  );
};

export default ShoppingListDetailPage;