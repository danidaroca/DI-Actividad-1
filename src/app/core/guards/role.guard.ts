import { inject } from '@angular/core';
import { CanActivateFn, CanMatchFn, Router, Route, UrlSegment } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { UserRole } from '../models/user.model';

/**
 * Functional Guard (CanActivateFn) para Control de Acceso Basado en Roles (RBAC).
 * Valida de forma declarativa que el rol del usuario conectado contenga
 * los privilegios requeridos en la propiedad 'data.expectedRole'.
 * Si el usuario no tiene privilegios, redirige a una ruta operativa segura (/inventory)
 * evitando pantallas de error no controladas.
 *
 * Cumplimiento curricular: RA 1 (CE 1.f) y RA 6 (CE 6.a).
 */
export const roleGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const expectedRole = route.data['expectedRole'] as UserRole;
  const currentUser = authService.getCurrentUser();

  if (!currentUser) {
    router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }

  if (expectedRole && currentUser.role !== expectedRole) {
    // Si no cuenta con el rol autorizado (ej: usuario estándar intentando acceder a /dashboard de ADMIN)
    router.navigate(['/inventory'], { queryParams: { error: 'forbidden' } });
    return false;
  }

  return true;
};

/**
 * Functional Guard (CanMatchFn) para RBAC en la fase de emparejamiento de rutas.
 * Impide la descarga del chunk JS del módulo administrativo si el usuario no posee el rol ADMIN.
 */
export const roleMatchGuard: CanMatchFn = (route: Route, segments: UrlSegment[]) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const expectedRole = route.data?.['expectedRole'] as UserRole;
  const currentUser = authService.getCurrentUser();

  if (!currentUser || (expectedRole && currentUser.role !== expectedRole)) {
    router.navigate(['/inventory']);
    return false;
  }

  return true;
};
