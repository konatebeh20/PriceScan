import React from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar,
  IonSearchbar, IonList, IonItem, IonLabel, IonButton, useIonRouter, IonGrid, IonRow, IonCol
} from '@ionic/react';

const SearchPage: React.FC = () => {
  const router = useIonRouter();
  const goToDetail = () => { router.push('/tabs/product/123'); };
  const goToMap = () => { router.push('/tabs/map'); };
  // Redirige vers la page d'import pour un produit inconnu
  const goToAddUnknown = () => { router.push('/tabs/newticket'); };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonTitle>Comparer les Prix</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonSearchbar placeholder="Rechercher un produit..."></IonSearchbar>

        <div className="ion-padding">
          <IonGrid>
            <IonRow>
              <IonCol>
                <IonButton expand="full" onClick={goToMap}>
                  Voir la Carte
                </IonButton>
              </IonCol>
              <IonCol>
                <IonButton expand="full" fill="outline" onClick={goToAddUnknown}>
                  Produit Inconnu ?
                </IonButton>
              </IonCol>
            </IonRow>
          </IonGrid>
        </div>

        <IonList>
          <IonItem button onClick={goToDetail}>
            <IonLabel>
              <h2>Lait</h2>
              <p>Cliquez pour voir les détails</p>
            </IonLabel>
          </IonItem>
        </IonList> {/* CORRECTION ICI */}
      </IonContent>
    </IonPage>
  );
};

export default SearchPage;