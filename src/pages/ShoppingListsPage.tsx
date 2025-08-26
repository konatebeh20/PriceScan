// Fichier : src/pages/ShoppingListsPage.tsx

import React from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonList,
  IonItem, IonLabel, IonFab, IonFabButton, IonIcon, useIonRouter
} from '@ionic/react';
import { add } from 'ionicons/icons';

const FAKE_LISTS = [
  { id: '1', name: 'Courses de la semaine' },
  { id: '2', name: 'Anniversaire Maman' },
];

const ShoppingListsPage: React.FC = () => {
  const router = useIonRouter();

  const goToListDetail = (listId: string) => {
    router.push(`/tabs/lists/${listId}`);
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonTitle>Mes Listes</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonList>
          {FAKE_LISTS.map(list => (
            <IonItem button key={list.id} onClick={() => goToListDetail(list.id)}>
              <IonLabel>{list.name}</IonLabel>
            </IonItem>
          ))}
        </IonList>
        <IonFab vertical="bottom" horizontal="end" slot="fixed">
          <IonFabButton onClick={() => alert('Ajouter une nouvelle liste !')}>
            <IonIcon icon={add} />
          </IonFabButton>
        </IonFab>
      </IonContent>
    </IonPage>
  );
};

export default ShoppingListsPage;