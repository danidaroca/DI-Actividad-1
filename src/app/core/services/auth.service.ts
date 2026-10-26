import { Injectable, inject } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { delay, tap } from 'rxjs/operators';
import { User, LoginCredentials, RegisterDTO, AuthResponse, UserRole } from '../models/user.model';
import { AsyncValidatorService } from './async-validator.service';

const STORAGE_KEY_USER = 'gestion_user_data';
const STORAGE_KEY_TOKEN = 'gestion_auth_token';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private router = inject(Router);
  private asyncValidatorService = inject(AsyncValidatorService);

  private currentUserSubject = new BehaviorSubject<User | null>(this.getStoredUser());
  public currentUser$ = this.currentUserSubject.asObservable();

  // Usuarios simulados iniciales
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
   * Verifica si el usuario actual está autenticado
   */
  public isAuthenticated(): boolean {
    return !!this.currentUserSubject.value && !!localStorage.getItem(STORAGE_KEY_TOKEN);
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
   * Verifica si el usuario tiene un rol específico
   */
  public hasRole(role: UserRole): boolean {
    const user = this.currentUserSubject.value;
    return user?.role === role;
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

    // Generación de token JWT sintético simulado
    const fakeToken = `simulated-jwt-token.${btoa(JSON.stringify({ sub: user.id, role: user.role }))}.${Date.now()}`;
    const response: AuthResponse = {
      user,
      token: fakeToken,
      expiresIn: 3600
    };

    return of(response).pipe(
      delay(700), // Simula latencia de servidor
      tap(res => {
        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(res.user));
        localStorage.setItem(STORAGE_KEY_TOKEN, res.token);
        this.currentUserSubject.next(res.user);
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

    const fakeToken = `simulated-jwt-token.${btoa(JSON.stringify({ sub: newUser.id, role: newUser.role }))}.${Date.now()}`;
    const response: AuthResponse = {
      user: newUser,
      token: fakeToken,
      expiresIn: 3600
    };

    return of(response).pipe(
      delay(800),
      tap(res => {
        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(res.user));
        localStorage.setItem(STORAGE_KEY_TOKEN, res.token);
        this.currentUserSubject.next(res.user);
      })
    );
  }

  /**
   * Cierre de sesión y limpieza de estado
   */
  public logout(): void {
    localStorage.removeItem(STORAGE_KEY_USER);
    localStorage.removeItem(STORAGE_KEY_TOKEN);
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }
}
