import React, { useState } from 'react';
import {
  IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButton, IonImg, IonIcon
} from '@ionic/react';
import { camera, albums, checkmarkCircle, closeCircle } from 'ionicons/icons';
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';

const NewTicketPage: React.FC = () => {
  const [photo, setPhoto] = useState<string | undefined>();

  const selectImage = async (source: CameraSource) => {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: CameraResultType.Uri,
        source: source // Utilise la source : Caméra ou Galerie
      });

      if (image.webPath) {
        setPhoto(image.webPath);
      }
    } catch (error) {
      console.error("Erreur lors de la sélection de l'image", error);
    }
  };

  const handleAnalysis = () => {
    alert('Analyse du ticket simulée !');
    setPhoto(undefined); // Réinitialise l'image après l'analyse
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar color="primary">
          <IonTitle>Importer un Ticket</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen className="ion-padding">
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          
          {!photo ? (
            // Si aucune photo n'est sélectionnée, affiche les boutons de choix
            <>
              <IonButton expand="block" size="large" onClick={() => selectImage(CameraSource.Camera)}>
                <IonIcon slot="start" icon={camera} />
                Prendre une Photo
              </IonButton>
              <IonButton expand="block" fill="outline" size="large" className="ion-margin-top" onClick={() => selectImage(CameraSource.Photos)}>
                <IonIcon slot="start" icon={albums} />
                Choisir depuis la Galerie
              </IonButton>
            </>
          ) : (
            // Si une photo est sélectionnée, l'affiche avec les boutons d'action
            <>
              <IonImg src={photo} style={{ marginBottom: '20px', border: '1px solid #ddd' }} />
              <IonButton expand="full" size="large" onClick={handleAnalysis}>
                <IonIcon slot="start" icon={checkmarkCircle} />
                Lancer l'analyse
              </IonButton>
              <IonButton expand="full" fill="clear" color="danger" onClick={() => setPhoto(undefined)}>
                <IonIcon slot="start" icon={closeCircle} />
                Annuler
              </IonButton>
            </>
          )}

        </div>
      </IonContent>
    </IonPage>
  );
};

export default NewTicketPage;