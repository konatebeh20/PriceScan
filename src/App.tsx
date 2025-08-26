import React from 'react';
import { Redirect, Route } from 'react-router-dom';
import { IonApp, IonIcon, IonLabel, IonRouterOutlet, IonTabBar, IonTabButton, IonTabs, setupIonicReact } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { search, list, podium, personCircle, addCircle } from 'ionicons/icons';

// Import de TOUTES nos pages
import LoginPage from './pages/LoginPage';
import SearchPage from './pages/SearchPage';
import ShoppingListsPage from './pages/ShoppingListsPage';
import ShoppingListDetailPage from './pages/ShoppingListDetailPage';
import LeaderboardPage from './pages/LeaderboardPage';
import ProfilePage from './pages/ProfilePage';
import ProductDetailPage from './pages/ProductDetailPage';
import MapPage from './pages/MapPage';
import OptimalBasketResultPage from './pages/OptimalBasketResultPage';
import NewTicketPage from './pages/NewTicketPage';

/* Styles (ne pas toucher) */
import '@ionic/react/css/core.css';
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';
import './theme/variables.css';
import 'leaflet/dist/leaflet.css';

setupIonicReact();

// Composant interne pour gérer la navigation par onglets
const TabsController: React.FC = () => (
  <IonTabs>
    <IonRouterOutlet>
      <Route exact path="/tabs/search" component={SearchPage} />
      <Route exact path="/tabs/map" component={MapPage} />
      <Route exact path="/tabs/lists" component={ShoppingListsPage} />
      <Route path="/tabs/lists/:id" component={ShoppingListDetailPage} />
      <Route path="/tabs/optimal-basket/:id" component={OptimalBasketResultPage} />
      <Route exact path="/tabs/newticket" component={NewTicketPage} />
      <Route exact path="/tabs/leaderboard" component={LeaderboardPage} />
      <Route exact path="/tabs/profile" component={ProfilePage} />
      <Route path="/tabs/product/:id" component={ProductDetailPage} />
      <Route exact path="/tabs">
        <Redirect to="/tabs/search" />
      </Route>
    </IonRouterOutlet>
    <IonTabBar slot="bottom">
      <IonTabButton tab="search" href="/tabs/search">
        <IonIcon icon={search} />
        <IonLabel>Comparer</IonLabel>
      </IonTabButton>
      <IonTabButton tab="lists" href="/tabs/lists">
        <IonIcon icon={list} />
        <IonLabel>Listes</IonLabel>
      </IonTabButton>
      <IonTabButton tab="newticket" href="/tabs/newticket">
        <IonIcon icon={addCircle} />
        <IonLabel>Importer</IonLabel>
      </IonTabButton>
      <IonTabButton tab="leaderboard" href="/tabs/leaderboard">
        <IonIcon icon={podium} />
        <IonLabel>Classements</IonLabel>
      </IonTabButton>
      <IonTabButton tab="profile" href="/tabs/profile">
        <IonIcon icon={personCircle} />
        <IonLabel>Profil</IonLabel>
      </IonTabButton>
    </IonTabBar>
  </IonTabs>
);

const App: React.FC = () => (
  <IonApp>
    <IonReactRouter>
      <IonRouterOutlet>
        <Route exact path="/login" component={LoginPage} />
        <Route path="/tabs" component={TabsController} />
        <Route exact path="/">
          <Redirect to="/login" />
        </Route>
      </IonRouterOutlet>
    </IonReactRouter>
  </IonApp>
);

export default App;