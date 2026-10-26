import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { 
  IonApp, 
  IonSplitPane, 
  IonMenu, 
  IonContent, 
  IonList, 
  IonListHeader, 
  IonMenuToggle, 
  IonItem, 
  IonIcon, 
  IonLabel, 
  IonRouterOutlet, 
  IonRouterLink,
  IonBadge,
  IonButton
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { 
  statsChartOutline, 
  cubeOutline, 
  helpCircleOutline, 
  logInOutline, 
  personAddOutline, 
  logOutOutline,
  personCircleOutline,
  businessOutline
} from 'ionicons/icons';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
  imports: [
    CommonModule,
    RouterLink, 
    RouterLinkActive, 
    IonApp, 
    IonSplitPane, 
    IonMenu, 
    IonContent, 
    IonList, 
    IonListHeader, 
    IonMenuToggle, 
    IonItem, 
    IonIcon, 
    IonLabel, 
    IonRouterLink, 
    IonRouterOutlet,
    IonBadge,
    IonButton
  ],
})
export class AppComponent {
  public authService = inject(AuthService);
  private router = inject(Router);

  constructor() {
    addIcons({ 
      statsChartOutline, 
      cubeOutline, 
      helpCircleOutline, 
      logInOutline, 
      personAddOutline, 
      logOutOutline,
      personCircleOutline,
      businessOutline
    });
  }

  logout(): void {
    this.authService.logout();
  }
}
