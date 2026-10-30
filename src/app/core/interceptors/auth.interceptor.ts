import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

/**
 * Functional HTTP Interceptor (HttpInterceptorFn) para la inyección de credenciales.
 * Intercepta de forma transparente todas las peticiones salientes y propaga
 * la cabecera estándar 'Authorization: Bearer <token>' obtenida del AuthService.
 *
 * Cumplimiento curricular: RA 3 (CE 3.d) y RA 6 (CE 6.a).
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  // Si no hay token de sesión (rutas públicas como login/register), se deja pasar la petición inalterada
  if (!token) {
    return next(req);
  }

  // Clonación inmutable de la petición agregando la cabecera Bearer
  const clonedRequest = req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });

  return next(clonedRequest);
};
