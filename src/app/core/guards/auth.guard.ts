import { inject } from '@angular/core';
import { CanActivateFn, CanMatchFn, Router, Route, UrlSegment } from '@angular/router';
import { AuthService } from '../services/auth.service';

/**
 * Functional Guard (CanActivateFn) para proteger rutas privadas autenticadas.
 * Se evalúa durante la fase de activación de la ruta. Si no hay sesión válida,
 * redirige al usuario a '/login' guardando la URL previa en queryParams (returnUrl)
 * para restaurar el contexto de navegación tras iniciar sesión con éxito.
 *
 * Cumplimiento curricular: RA 1 (CE 1.f) y RA 3 (CE 3.d).
 */
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  // Redirección contextual preservando la intención de navegación
  router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
  return false;
};

/**
 * Functional Guard (CanMatchFn) para protección a nivel de enrutador y optimización de Lazy Loading.
 * Se evalúa antes de resolver la ruta y antes de solicitar la descarga del bundle JavaScript
 * del componente lazy ('loadComponent'). Si retorna 'false', el enrutador descarta la coincidencia
 * y el chunk JS jamás se descarga por red, optimizando rendimiento y eliminando fugas de código cliente.
 */
export const authMatchGuard: CanMatchFn = (route: Route, segments: UrlSegment[]) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    return true;
  }

  const destinationUrl = '/' + segments.map(s => s.path).join('/');
  router.navigate(['/login'], { queryParams: { returnUrl: destinationUrl } });
  return false;
};
