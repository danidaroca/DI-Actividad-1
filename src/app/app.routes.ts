import { Routes } from '@angular/router';
import { authGuard, authMatchGuard } from './core/guards/auth.guard';
import { roleGuard, roleMatchGuard } from './core/guards/role.guard';

/**
 * Tabla de enrutamiento principal con lazy loading, guards funcionales (CanActivateFn / CanMatchFn)
 * y control de acceso basado en roles (RBAC).
 */
export const routes: Routes = [
  {
    path: '',
    redirectTo: 'inventory',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.page').then(m => m.LoginPage)
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.page').then(m => m.RegisterPage)
  },
  {
    path: 'dashboard',
    canMatch: [authMatchGuard, roleMatchGuard],
    canActivate: [authGuard, roleGuard],
    data: { expectedRole: 'ADMIN' },
    loadComponent: () => import('./pages/dashboard/dashboard.page').then(m => m.DashboardPage)
  },
  {
    path: 'inventory',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/records/records.page').then(m => m.RecordsPage)
  },
  {
    path: 'help',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/help/help.page').then(m => m.HelpPage)
  },
  {
    path: '**',
    redirectTo: 'inventory'
  }
];
