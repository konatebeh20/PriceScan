import React, { useState } from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonSegment,
  IonSegmentButton, IonLabel, IonList, IonItem, IonAvatar
} from '@ionic/react';

// Données statiques pour les classements
const FAKE_WEEKLY_LEADERBOARD = [
  { rank: 1, name: 'Fatima K.', points: 850, avatar: 'https://i.pravatar.cc/80?u=a' },
  { rank: 2, name: 'Jean-Pierre N.', points: 720, avatar: 'https://i.pravatar.cc/80?u=b' },
  { rank: 3, name: 'Aïssata B.', points: 680, avatar: 'https://i.pravatar.cc/80?u=c' },
];

const FAKE_MONTHLY_LEADERBOARD = [
  { rank: 1, name: 'Abdoulaye YEO', points: 2950, avatar: 'https://i.pravatar.cc/80?u=d' },
  { rank: 2, name: 'Fatima K.', points: 2600, avatar: 'https://i.pravatar.cc/80?u=a' },
  { rank: 3, name: 'Marie-Claire D.', points: 2450, avatar: 'https://i.pravatar.cc/80?u=e' },
];

const LeaderboardPage: React.FC = () => {
  const [segment, setSegment] = useState<'weekly' | 'monthly'>('weekly');

  const leaderboardData = segment === 'weekly' ? FAKE_WEEKLY_LEADERBOARD : FAKE_MONTHLY_LEADERBOARD;

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonTitle>Classements</IonTitle>
        </IonToolbar>
        <IonToolbar>
          <IonSegment value={segment} onIonChange={e => setSegment(e.detail.value as any)}>
            <IonSegmentButton value="weekly">
              <IonLabel>Hebdomadaire</IonLabel>
            </IonSegmentButton>
            <IonSegmentButton value="monthly">
              <IonLabel>Mensuel</IonLabel>
            </IonSegmentButton>
          </IonSegment>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonList>
          {leaderboardData.map((user) => (
            <IonItem key={user.rank}>
              <IonLabel style={{ fontSize: '1.2em', marginRight: '16px' }}>
                <strong>{user.rank}</strong>
              </IonLabel>
              <IonAvatar slot="start">
                <img src={user.avatar} alt="User avatar" />
              </IonAvatar>
              <IonLabel>
                <h2>{user.name}</h2>
                <p>{user.points} points</p>
              </IonLabel>
            </IonItem>
          ))}
        </IonList>
      </IonContent>
    </IonPage>
  );
};

export default LeaderboardPage;