import React, { useState } from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButtons,
  IonBackButton, IonCard, IonCardHeader, IonCardTitle, IonCardContent,
  IonButton, IonIcon
} from '@ionic/react';
import { heart, heartOutline } from 'ionicons/icons';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

// Données statiques pour l'historique des prix
const FAKE_PRICE_HISTORY = [
  { date: '15/07', 'Super U': 850, 'Carrefour': 860, 'CDCI': 840 },
  { date: '01/08', 'Super U': 850, 'Carrefour': 870, 'CDCI': 845 },
  { date: '15/08', 'Super U': 855, 'Carrefour': 875, 'CDCI': 850 },
  { date: 'Aujourd\'hui', 'Super U': 850, 'Carrefour': 875, 'CDCI': 840 },
];

const ProductDetailPage: React.FC = () => {
  // NOUVEL ÉTAT : pour suivre si le produit est en favori
  const [isFavorite, setIsFavorite] = useState(false);

  // NOUVELLE FONCTION : pour basculer l'état de favori
  const toggleFavorite = () => {
    setIsFavorite(!isFavorite);
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonButtons slot="start">
            <IonBackButton defaultHref="/tabs/search" />
          </IonButtons>
          <IonTitle>Détail du Produit</IonTitle>
          {/* NOUVEAU BOUTON AJOUTÉ ICI */}
          <IonButtons slot="end">
            <IonButton onClick={toggleFavorite}>
              <IonIcon 
                slot="icon-only" 
                icon={isFavorite ? heart : heartOutline} 
                color={isFavorite ? 'danger' : 'light'}
              />
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <IonCard>
          <img alt="lait" src="https://previews.123rf.com/images/pivden/pivden1805/pivden180500125/101744139-bo%C3%AEte-de-lait-en-carton-isol%C3%A9-sur-fond-blanc.jpg" />
          <IonCardHeader>
            <IonCardTitle>Lait UHT</IonCardTitle>
          </IonCardHeader>
          <IonCardContent>
            <h3>Prix Actuels :</h3>
            <p><strong>Super U :</strong> 850 F CFA (hier)</p>
            <p><strong>Carrefour :</strong> 875 F CFA (aujourd'hui)</p>
            <p><strong>CDCI :</strong> 840 F CFA (il y a 3 jours)</p>

            <h3 style={{ marginTop: '20px' }}>Historique des Prix :</h3>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={FAKE_PRICE_HISTORY}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="Super U" stroke="#8884d8" />
                <Line type="monotone" dataKey="Carrefour" stroke="#82ca9d" />
                <Line type="monotone" dataKey="CDCI" stroke="#ffc658" />
              </LineChart>
            </ResponsiveContainer>

          </IonCardContent>
        </IonCard>
      </IonContent>
    </IonPage>
  );
};

export default ProductDetailPage;