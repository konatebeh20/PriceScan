import React, { useState, useEffect } from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonCard,
  IonCardHeader, IonCardTitle, IonCardContent, IonAvatar, IonItem,
  IonLabel, IonGrid, IonRow, IonCol, IonIcon, IonList, IonToggle, IonListHeader
} from '@ionic/react';
import { storefront, ribbon, trophy, ticket, camera } from 'ionicons/icons';

const FAKE_USER_STATS = { name: 'Abdoulaye YEO', email: 'abdoulyeo45@gmail.com', level: 5, points: 1250, contributions: 89 };
const FAKE_BADGES = [{ icon: storefront, name: 'Expert du quartier' }, { icon: ribbon, name: 'Chasseur de promos' }, { icon: trophy, name: 'Contributeur en bronze' }];
const FAKE_HISTORY = [{ type: 'Ticket de caisse', details: 'Super U - 12 articles', points: '+ 50 pts', icon: ticket }, { type: 'Scan en rayon', details: 'Prix du Lait - Carrefour', points: '+ 5 pts', icon: camera }, { type: 'Ticket de caisse', details: 'CDCI - 8 articles', points: '+ 35 pts', icon: ticket }];

const ProfilePage: React.FC = () => {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const [isDarkMode, setIsDarkMode] = useState(prefersDark);

  useEffect(() => {
    document.body.classList.toggle('dark', isDarkMode);
  }, [isDarkMode]);

  const toggleDarkModeHandler = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonTitle>Mon Profil</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <IonItem lines="none">
          <IonAvatar slot="start" style={{ width: '60px', height: '60px' }}><img src={`https://ui-avatars.com/api/?name=${FAKE_USER_STATS.name}&background=random`} alt="User avatar" /></IonAvatar>
          <IonLabel><h2>{FAKE_USER_STATS.name}</h2><p>{FAKE_USER_STATS.email}</p></IonLabel>
        </IonItem>

        <IonCard>
          <IonList>
            <IonListHeader>
              <IonLabel>Paramètres</IonLabel>
            </IonListHeader>
            <IonItem>
              <IonLabel>Mode Sombre</IonLabel>
              <IonToggle
                slot="end"
                checked={isDarkMode}
                onIonChange={toggleDarkModeHandler}
              />
            </IonItem>
          </IonList> {/* CORRECTION ICI */}
        </IonCard>

        <IonCard>
          <IonCardHeader><IonCardTitle>Mes Statistiques</IonCardTitle></IonCardHeader>
          <IonCardContent><IonGrid><IonRow className="ion-text-center"><IonCol><IonLabel>Niveau</IonLabel><h2>{FAKE_USER_STATS.level}</h2></IonCol><IonCol><IonLabel>Points</IonLabel><h2>{FAKE_USER_STATS.points}</h2></IonCol><IonCol><IonLabel>Contributions</IonLabel><h2>{FAKE_USER_STATS.contributions}</h2></IonCol></IonRow></IonGrid></IonCardContent>
        </IonCard>

        <IonCard>
          <IonCardHeader><IonCardTitle>Mes Badges</IonCardTitle></IonCardHeader>
          <IonCardContent><IonGrid><IonRow>{FAKE_BADGES.map((badge, index) => (<IonCol size="4" key={index} className="ion-text-center"><IonIcon icon={badge.icon} style={{ fontSize: '48px' }} color="primary" /><p style={{ fontSize: '12px', marginTop: '4px' }}>{badge.name}</p></IonCol>))}</IonRow></IonGrid></IonCardContent>
        </IonCard>

        <IonCard>
          <IonCardHeader><IonCardTitle>Mon Historique</IonCardTitle></IonCardHeader>
          <IonCardContent><IonList>{FAKE_HISTORY.map((item, index) => (<IonItem key={index}><IonIcon icon={item.icon} slot="start" color="medium" /><IonLabel><h2>{item.type}</h2><p>{item.details}</p></IonLabel><IonLabel slot="end" color="success" className="ion-text-right">{item.points}</IonLabel></IonItem>))}</IonList></IonCardContent>
        </IonCard>

      </IonContent>
    </IonPage>
  );
};

export default ProfilePage;