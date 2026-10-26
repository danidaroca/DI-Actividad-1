import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { UserRole } from '../models/user.model';

/**
 * Guard para control de acceso basado en roles (RBAC).
 * Verifica que el rol del usuario coincida con el rol requerido en data['expectedRole'].
 */
export const roleGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const expectedRole = route.data['expectedRole'] as UserRole;
  const currentUser = authService.getCurrentUser();

  if (!currentUser) {
    router.navigate(['/login']);
    return false;
  }

  if (expectedRole && currentUser.role !== expectedRole) {
    // Si no es admin y quiere entrar al dashboard de admin, redirigir a registros
    router.navigate(['/inventory']);
    return false;
  }

  return true;
};
