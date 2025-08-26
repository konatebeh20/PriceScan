// Fichier : src/pages/MapPage.tsx

import React, { useState, useEffect } from 'react';
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButtons, IonBackButton, IonSpinner, IonAlert } from '@ionic/react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Geolocation, Position } from '@capacitor/geolocation';
import 'leaflet/dist/leaflet.css';

// --- DÉBUT DE LA CORRECTION POUR L'ICÔNE ---
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;
// --- FIN DE LA CORRECTION POUR L'ICÔNE ---

const MapPage: React.FC = () => {
  const [position, setPosition] = useState<Position | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getCurrentPosition = async () => {
      try {
        const coordinates = await Geolocation.getCurrentPosition({
          enableHighAccuracy: true,
          timeout: 10000,
        });
        setPosition(coordinates);
      } catch (e) {
        setError('Impossible de récupérer votre position. Veuillez activer la géolocalisation et rafraîchir la page.');
      }
    };
    getCurrentPosition();
  }, []);

  const renderMap = () => {
    if (error) {
      return <IonAlert isOpen={true} message={error} buttons={['OK']} onDidDismiss={() => setError(null)} />;
    }

    if (!position) {
      return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
          <IonSpinner />
        </div>
      );
    }

    return (
      <MapContainer 
        center={[position.coords.latitude, position.coords.longitude]} 
        zoom={13} 
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[position.coords.latitude, position.coords.longitude]}>
          <Popup>Vous êtes ici.</Popup>
        </Marker>
      </MapContainer>
    );
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonButtons slot="start">
            <IonBackButton defaultHref="/tabs/search" />
          </IonButtons>
          <IonTitle>Carte des Bonnes Affaires</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        {renderMap()}
      </IonContent>
    </IonPage>
  );
};

export default MapPage;