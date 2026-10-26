import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { 
  IonContent, 
  IonCard, 
  IonCardHeader, 
  IonCardTitle, 
  IonCardSubtitle, 
  IonCardContent, 
  IonItem, 
  IonInput, 
  IonButton, 
  IonIcon, 
  IonSpinner, 
  IonNote,
  IonText
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { logInOutline, personOutline, lockClosedOutline, shieldCheckmarkOutline, alertCircleOutline } from 'ionicons/icons';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
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
    IonInput,
    IonButton,
    IonIcon,
    IonSpinner,
    IonNote,
    IonText
  ],
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss']
})
export class LoginPage {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  public loginForm: FormGroup;
  public isLoading: boolean = false;
  public errorMessage: string | null = null;

  constructor() {
    addIcons({ logInOutline, personOutline, lockClosedOutline, shieldCheckmarkOutline, alertCircleOutline });

    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(4)]]
    });
  }

  // Accesores cómodos para la plantilla
  get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = null;

    this.authService.login(this.loginForm.value).subscribe({
      next: (res) => {
        this.isLoading = false;
        const returnUrl = this.route.snapshot.queryParams['returnUrl'];
        if (returnUrl) {
          this.router.navigateByUrl(returnUrl);
        } else if (res.user.role === 'ADMIN') {
          this.router.navigate(['/dashboard']);
        } else {
          this.router.navigate(['/inventory']);
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.message || 'Error de autenticación. Intente nuevamente.';
      }
    });
  }

  fillAdmin(): void {
    this.loginForm.setValue({
      email: 'admin@empresa.com',
      password: 'Admin123!'
    });
  }

  fillStandardUser(): void {
    this.loginForm.setValue({
      email: 'user@empresa.com',
      password: 'User123!'
    });
  }
}
