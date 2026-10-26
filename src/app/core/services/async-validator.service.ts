import { Injectable } from '@angular/core';
import { AbstractControl, AsyncValidatorFn, ValidationErrors } from '@angular/forms';
import { Observable, of, timer } from 'rxjs';
import { map, switchMap, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AsyncValidatorService {
  // Base de datos simulada de emails ya registrados
  private existingEmails: string[] = [
    'admin@empresa.com',
    'user@empresa.com',
    'director@empresa.com',
    'soporte@empresa.com',
    'contacto@empresa.com'
  ];

  // Códigos de producto/registro ya existentes
  private existingCodes: string[] = [
    'PROD-001',
    'PROD-002',
    'PROD-003',
    'SRV-101'
  ];

  /**
   * Simula consulta asíncrona a un backend para verificar disponibilidad de correo.
   * Introduce una latencia de 600ms para simular petición de red.
   */
  checkEmailAvailability(email: string): Observable<boolean> {
    const normalized = (email || '').trim().toLowerCase();
    return timer(600).pipe(
      map(() => !this.existingEmails.includes(normalized))
    );
  }

  /**
   * Simula consulta asíncrona a un backend para verificar disponibilidad de código de registro.
   */
  checkCodeAvailability(code: string): Observable<boolean> {
    const normalized = (code || '').trim().toUpperCase();
    return timer(500).pipe(
      map(() => !this.existingCodes.includes(normalized))
    );
  }

  /**
   * Validador asíncrono para formularios reactivos (Email)
   */
  emailAvailableValidator(): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      if (!control.value || control.value.trim() === '') {
        return of(null);
      }
      return this.checkEmailAvailability(control.value).pipe(
        map(isAvailable => (isAvailable ? null : { emailTaken: true })),
        catchError(() => of(null))
      );
    };
  }

  /**
   * Validador asíncrono para formularios reactivos (Código de producto/registro)
   */
  codeAvailableValidator(): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      if (!control.value || control.value.trim() === '') {
        return of(null);
      }
      return this.checkCodeAvailability(control.value).pipe(
        map(isAvailable => (isAvailable ? null : { codeTaken: true })),
        catchError(() => of(null))
      );
    };
  }

  /**
   * Registrar nuevo email en la base de datos simulada
   */
  registerEmail(email: string): void {
    const normalized = email.trim().toLowerCase();
    if (!this.existingEmails.includes(normalized)) {
      this.existingEmails.push(normalized);
    }
  }

  /**
   * Registrar nuevo código en la base de datos simulada
   */
  registerCode(code: string): void {
    const normalized = code.trim().toUpperCase();
    if (!this.existingCodes.includes(normalized)) {
      this.existingCodes.push(normalized);
    }
  }
}
