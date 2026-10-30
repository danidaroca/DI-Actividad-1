import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonButtons, 
  IonMenuButton, 
  IonContent, 
  IonCard, 
  IonCardHeader, 
  IonCardTitle, 
  IonCardContent, 
  IonAccordionGroup, 
  IonAccordion, 
  IonItem, 
  IonLabel,
  IonIcon
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { helpCircleOutline, shieldOutline, documentTextOutline, searchOutline, downloadOutline, pieChartOutline } from 'ionicons/icons';

@Component({
  selector: 'app-help',
  standalone: true,
  imports: [
    CommonModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonMenuButton,
    IonContent,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonAccordionGroup,
    IonAccordion,
    IonItem,
    IonLabel,
    IonIcon
  ],
  templateUrl: './help.page.html',
  styleUrls: ['./help.page.scss']
})
export class HelpPage {
  constructor() {
    addIcons({ helpCircleOutline, shieldOutline, documentTextOutline, searchOutline, downloadOutline, pieChartOutline });
  }
}
