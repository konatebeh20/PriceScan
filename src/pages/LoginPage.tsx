import React from 'react';
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonList, IonItem, IonLabel, IonInput, IonButton, useIonRouter } from '@ionic/react';

const LoginPage: React.FC = () => {
  const router = useIonRouter();
  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    router.push('/tabs/search', 'root', 'replace');
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonTitle>TicketScan - Bienvenue</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <form onSubmit={handleLogin} style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <IonList>
            <IonItem>
              <IonLabel position="floating">Email</IonLabel>
              <IonInput type="email" required />
            </IonItem>
            <IonItem>
              <IonLabel position="floating">Mot de passe</IonLabel>
              <IonInput type="password" required />
            </IonItem>
          </IonList>
          <IonButton type="submit" expand="block" className="ion-margin-top">
            Connexion / Inscription
          </IonButton>
        </form>
      </IonContent>
    </IonPage>
  );
};

export default LoginPage;