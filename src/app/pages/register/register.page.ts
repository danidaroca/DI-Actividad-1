import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { 
  IonContent, 
  IonCard, 
  IonCardHeader, 
  IonCardTitle, 
  IonCardSubtitle, 
  IonCardContent, 
  IonItem, 
  IonLabel, 
  IonInput, 
  IonSelect, 
  IonSelectOption, 
  IonButton, 
  IonIcon, 
  IonSpinner, 
  IonNote, 
  IonText 
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { personAddOutline, personOutline, mailOutline, lockClosedOutline, checkmarkCircleOutline, closeCircleOutline, alertCircleOutline } from 'ionicons/icons';
import { AuthService } from '../../core/services/auth.service';
import { AsyncValidatorService } from '../../core/services/async-validator.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink,
    IonContent,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonButton,
    IonIcon,
    IonSpinner,
    IonNote,
    IonText
  ],
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss']
})
export class RegisterPage {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private asyncValidator = inject(AsyncValidatorService);
  private router = inject(Router);

  public registerForm: FormGroup;
  public isLoading: boolean = false;
  public errorMessage: string | null = null;
  public successMessage: string | null = null;

  constructor() {
    addIcons({
      personAddOutline,
      personOutline,
      mailOutline,
      lockClosedOutline,
      checkmarkCircleOutline,
      closeCircleOutline,
      alertCircleOutline
    });

    this.registerForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      email: [
        '',
        [Validators.required, Validators.email],
        [this.asyncValidator.emailAvailableValidator()] // Validación asíncrona contra backend simulado
      ],
      role: ['STANDARD_USER', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
  }

  // Getters para legibilidad en la plantilla declarativa
  get name() { return this.registerForm.get('name'); }
  get email() { return this.registerForm.get('email'); }
  get role() { return this.registerForm.get('role'); }
  get password() { return this.registerForm.get('password'); }
  get confirmPassword() { return this.registerForm.get('confirmPassword'); }

  private passwordMatchValidator(group: AbstractControl) {
    const pass = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return pass === confirm ? null : { passwordMismatch: true };
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = null;

    const { name, email, password, role } = this.registerForm.value;

    this.authService.register({ name, email, password, role }).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.successMessage = '¡Registro completado con éxito! Redirigiendo...';
        setTimeout(() => {
          if (res.user.role === 'ADMIN') {
            this.router.navigate(['/dashboard']);
          } else {
            this.router.navigate(['/inventory']);
          }
        }, 1200);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Error al registrar el usuario.';
      }
    });
  }
}
