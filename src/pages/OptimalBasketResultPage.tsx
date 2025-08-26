import React from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButtons,
  IonBackButton, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonItem, IonLabel, IonList
} from '@ionic/react';
import { useParams } from 'react-router-dom';

const OptimalBasketResultPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonButtons slot="start">
            <IonBackButton defaultHref={`/tabs/lists/${id}`} />
          </IonButtons>
          <IonTitle>Panier Optimal</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <IonCard>
          <IonCardHeader>
            <IonCardTitle color="success">Économie Maximale : 1 250 F CFA</IonCardTitle>
          </IonCardHeader>
          <IonCardContent>
            <p>Voici la meilleure combinaison pour vos achats :</p>
          </IonCardContent>
        </IonCard>

        <IonCard>
          <IonCardHeader>
            <IonCardTitle>Magasin A : Super U</IonCardTitle>
            <IonLabel>Total : 4 500 F CFA</IonLabel>
          </IonCardHeader>
          <IonCardContent>
            <IonList>
              <IonItem>Lait</IonItem>
              <IonItem>Fromage</IonItem>
            </IonList>
          </IonCardContent>
        </IonCard>

        <IonCard>
          <IonCardHeader>
            <IonCardTitle>Magasin B : CDCI</IonCardTitle>
            <IonLabel>Total : 2 800 F CFA</IonLabel>
          </IonCardHeader>
          <IonCardContent>
            <IonList>
              <IonItem>Pain</IonItem>
              <IonItem>Œufs</IonItem>
            </IonList>
          </IonCardContent>
        </IonCard>
      </IonContent>
    </IonPage>
  );
};

export default OptimalBasketResultPage;