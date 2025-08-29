import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/tabs/home',
    pathMatch: 'full',
  },
  {
    path: 'tabs',
    loadComponent: () => import('./tabs/tabs.page').then(m => m.TabsPage),
    children: [
      {
        path: 'home',
        loadComponent: () => import('./pages/home/home.page').then(m => m.HomePage)
      },
      {
        path: 'scan',
        loadComponent: () => import('./pages/scan/scan.page').then(m => m.ScanPage)
      },
        {
    path: 'compare',
    loadComponent: () => import('./pages/compare/compare.page').then(m => m.ComparePage)
  },
  {
    path: 'history',
    loadComponent: () => import('./pages/history/history.page').then(m => m.HistoryPage)
  },
  {
    path: 'profile',
    loadComponent: () => import('./pages/profile/profile.page').then(m => m.ProfilePage)
  }
    ]
  },
  {
    path: 'product-detail/:id',
    loadComponent: () => import('./pages/scan/scan.page').then(m => m.ScanPage)
  },
  {
    path: 'price-alert',
    loadComponent: () => import('./pages/scan/scan.page').then(m => m.ScanPage)
  }
];
