import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

/**
 * Functional HTTP Interceptor (HttpInterceptorFn) para el manejo centralizado de errores HTTP.
 * Gestiona códigos de estado de seguridad:
 * - 401 Unauthorized: Sesión expirada o token inválido. Limpia el estado y redirige a /login con returnUrl contextual.
 * - 403 Forbidden: Privilegios insuficientes (violación de RBAC). Redirige a ruta segura (/inventory) con aviso.
 *
 * Cumplimiento curricular: RA 1 (CE 1.f), RA 3 (CE 3.d) y Rúbrica de Seguridad.
 */
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Sesión expirada / no autorizada: revocación de estado local y redirección con memoria de ruta
        const currentUrl = router.url;
        authService.logout(false); // Cierre sin navegación interna para preservar parámetros
        router.navigate(['/login'], {
          queryParams: {
            returnUrl: currentUrl,
            reason: 'session_expired'
          }
        });
      } else if (error.status === 403) {
        // Intento de acceso a recurso protegido sin privilegios de rol suficientes (RBAC)
        router.navigate(['/inventory'], {
          queryParams: {
            error: 'forbidden_access'
          }
        });
      }

      return throwError(() => error);
    })
  );
};
