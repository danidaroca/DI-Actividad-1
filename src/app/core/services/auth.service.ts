import { Injectable, inject, signal, computed } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { delay, tap } from 'rxjs/operators';
import { User, LoginCredentials, RegisterDTO, AuthResponse, UserRole, TokenClaims } from '../models/user.model';
import { AsyncValidatorService } from './async-validator.service';

const STORAGE_KEY_USER = 'gestion_user_data';
const STORAGE_KEY_TOKEN = 'gestion_auth_token';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private router = inject(Router);
  private asyncValidatorService = inject(AsyncValidatorService);

  // Estado reactivo basado en BehaviorSubject (compatible RxJS)
  private currentUserSubject = new BehaviorSubject<User | null>(this.getStoredUser());
  public currentUser$ = this.currentUserSubject.asObservable();

  // Estado reactivo moderno basado en Angular Signals (Rigor Técnico)
  public currentUserSignal = signal<User | null>(this.getStoredUser());
  public isAuthenticatedSignal = computed(() => !!this.currentUserSignal() && !!this.getToken());
  public isAdminSignal = computed(() => this.currentUserSignal()?.role === 'ADMIN');

  // Matriz de permisos RBAC según el rol
  private readonly rolePermissionsMap: Record<UserRole, string[]> = {
    ADMIN: ['dashboard:read', 'inventory:read', 'inventory:create', 'inventory:update', 'inventory:delete', 'reports:export'],
    SUPERVISOR: ['dashboard:read', 'inventory:read', 'inventory:create', 'inventory:update', 'reports:export'],
    STANDARD_USER: ['inventory:read', 'inventory:create', 'reports:export']
  };

  // Usuarios simulados iniciales para evaluación
  private mockUsers: User[] = [
    {
      id: 'usr-admin-01',
      name: 'Administrador Demo',
      email: 'admin@empresa.com',
      role: 'ADMIN',
      avatarUrl: 'assets/icon/favicon.png',
      createdAt: '2026-01-10T08:00:00Z'
    },
    {
      id: 'usr-std-02',
      name: 'Usuario Estándar',
      email: 'user@empresa.com',
      role: 'STANDARD_USER',
      avatarUrl: 'assets/icon/favicon.png',
      createdAt: '2026-02-15T10:30:00Z'
    }
  ];

  constructor() {}

  /**
   * Obtiene el usuario almacenado en LocalStorage
   */
  private getStoredUser(): User | null {
    try {
      const data = localStorage.getItem(STORAGE_KEY_USER);
      return data ? JSON.parse(data) : null;
    } catch {
      return null;
    }
  }

  /**
   * Obtiene el token de autenticación actual
   */
  public getToken(): string | null {
    return localStorage.getItem(STORAGE_KEY_TOKEN);
  }

  /**
   * Verifica si el usuario actual está autenticado
   */
  public isAuthenticated(): boolean {
    return !!this.currentUserSubject.value && !!this.getToken();
  }

  /**
   * Obtiene el usuario actual síncronamente
   */
  public getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Verifica si el usuario actual tiene rol de Administrador
   */
  public isAdmin(): boolean {
    const user = this.currentUserSubject.value;
    return user?.role === 'ADMIN';
  }

  /**
   * Verifica si el usuario tiene un rol específico (RBAC)
   */
  public hasRole(role: UserRole): boolean {
    const user = this.currentUserSubject.value;
    return user?.role === role;
  }

  /**
   * Comprueba si el usuario tiene un permiso específico dentro del modelo RBAC
   */
  public hasPermission(permission: string): boolean {
    const user = this.currentUserSubject.value;
    if (!user) return false;
    const permissions = this.rolePermissionsMap[user.role] || [];
    return permissions.includes(permission);
  }

  /**
   * Decodifica y extrae los claims del token JWT simulado
   */
  public getClaims(): TokenClaims | null {
    const token = this.getToken();
    if (!token) return null;
    try {
      const parts = token.split('.');
      if (parts.length >= 2) {
        return JSON.parse(atob(parts[1])) as TokenClaims;
      }
      return null;
    } catch {
      return null;
    }
  }

  /**
   * Inicio de sesión simulado con verificación asíncrona de credenciales
   */
  public login(credentials: LoginCredentials): Observable<AuthResponse> {
    const emailNorm = credentials.email.trim().toLowerCase();
    const user = this.mockUsers.find(u => u.email.toLowerCase() === emailNorm);

    if (!user) {
      return throwError(() => new Error('Credenciales incorrectas. Verifique el correo electrónico.'));
    }

    if (!credentials.password || credentials.password.length < 4) {
      return throwError(() => new Error('Contraseña inválida (mínimo 4 caracteres).'));
    }

    const permissions = this.rolePermissionsMap[user.role] || [];
    const now = Math.floor(Date.now() / 1000);
    const claims: TokenClaims = {
      sub: user.id,
      email: user.email,
      role: user.role,
      permissions,
      iat: now,
      exp: now + 3600 // Expira en 1 hora
    };

    // Generación de token JWT estructurado
    const fakeToken = `simulated-jwt.${btoa(JSON.stringify(claims))}.${Date.now()}`;
    const response: AuthResponse = {
      user,
      token: fakeToken,
      expiresIn: 3600
    };

    return of(response).pipe(
      delay(600), // Simula latencia de red
      tap(res => {
        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(res.user));
        localStorage.setItem(STORAGE_KEY_TOKEN, res.token);
        this.currentUserSubject.next(res.user);
        this.currentUserSignal.set(res.user);
      })
    );
  }

  /**
   * Flujo de refresco reactivo de token ante expiración (Silent Refresh)
   */
  public refreshToken(): Observable<string> {
    const user = this.getCurrentUser();
    if (!user) {
      return throwError(() => new Error('No existe sesión activa para renovar token.'));
    }

    const permissions = this.rolePermissionsMap[user.role] || [];
    const now = Math.floor(Date.now() / 1000);
    const renewedClaims: TokenClaims = {
      sub: user.id,
      email: user.email,
      role: user.role,
      permissions,
      iat: now,
      exp: now + 3600
    };

    const newToken = `simulated-jwt.${btoa(JSON.stringify(renewedClaims))}.${Date.now()}`;
    return of(newToken).pipe(
      delay(400),
      tap(tok => {
        localStorage.setItem(STORAGE_KEY_TOKEN, tok);
      })
    );
  }

  /**
   * Registro reactivo de un nuevo usuario en el sistema
   */
  public register(dto: RegisterDTO): Observable<AuthResponse> {
    const emailNorm = dto.email.trim().toLowerCase();
    const exists = this.mockUsers.some(u => u.email.toLowerCase() === emailNorm);

    if (exists) {
      return throwError(() => new Error('El correo electrónico ya se encuentra registrado.'));
    }

    const newUser: User = {
      id: `usr-${Date.now()}`,
      name: dto.name.trim(),
      email: emailNorm,
      role: dto.role || 'STANDARD_USER',
      avatarUrl: 'assets/icon/favicon.png',
      createdAt: new Date().toISOString()
    };

    this.mockUsers.push(newUser);
    this.asyncValidatorService.registerEmail(emailNorm);

    const permissions = this.rolePermissionsMap[newUser.role] || [];
    const now = Math.floor(Date.now() / 1000);
    const claims: TokenClaims = {
      sub: newUser.id,
      email: newUser.email,
      role: newUser.role,
      permissions,
      iat: now,
      exp: now + 3600
    };

    const fakeToken = `simulated-jwt.${btoa(JSON.stringify(claims))}.${Date.now()}`;
    const response: AuthResponse = {
      user: newUser,
      token: fakeToken,
      expiresIn: 3600
    };

    return of(response).pipe(
      delay(700),
      tap(res => {
        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(res.user));
        localStorage.setItem(STORAGE_KEY_TOKEN, res.token);
        this.currentUserSubject.next(res.user);
        this.currentUserSignal.set(res.user);
      })
    );
  }

  /**
   * Cierre de sesión y limpieza de estado
   * @param navigate Si es true, redirige a /login por defecto
   */
  public logout(navigate: boolean = true): void {
    localStorage.removeItem(STORAGE_KEY_USER);
    localStorage.removeItem(STORAGE_KEY_TOKEN);
    this.currentUserSubject.next(null);
    this.currentUserSignal.set(null);
    if (navigate) {
      this.router.navigate(['/login']);
    }
  }
}
