export type UserRole = 'ADMIN' | 'STANDARD_USER' | 'SUPERVISOR';

export interface TokenClaims {
  sub: string;             // Identificador único de usuario (Subject)
  email: string;           // Correo electrónico
  role: UserRole;          // Rol principal en el modelo RBAC
  permissions: string[];   // Lista de capacidades granulares
  iat: number;             // Issued At (Timestamp de emisión)
  exp: number;             // Expiration Time (Timestamp de expiración)
}

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatarUrl?: string;
  createdAt: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  expiresIn: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterDTO {
  name: string;
  email: string;
  password: string;
  role?: UserRole;
}
