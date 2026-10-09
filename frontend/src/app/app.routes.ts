import { Routes } from '@angular/router';

import { adminGuard } from './core/auth/admin.guard';
import { AdminAnnotationsPage } from './features/admin-annotations/admin-annotations';
import { AdminLoginPage } from './features/admin-login/admin-login';
import { GeneDetailPage } from './features/gene-detail/gene-detail';
import { GeneExplorer } from './features/gene-explorer/gene-explorer';

export const routes: Routes = [
  {
    path: '',
    component: GeneExplorer,
  },
  {
    path: 'genes/:id',
    component: GeneDetailPage,
  },
  {
    path: 'admin/login',
    component: AdminLoginPage,
  },
  {
    path: 'admin',
    component: AdminAnnotationsPage,
    canActivate: [adminGuard],
  },
  {
    path: '**',
    redirectTo: '',
  },
];
