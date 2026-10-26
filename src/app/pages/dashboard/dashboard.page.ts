import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonButtons, 
  IonMenuButton, 
  IonContent, 
  IonGrid, 
  IonRow, 
  IonCol, 
  IonButton, 
  IonIcon, 
  IonCard, 
  IonCardHeader, 
  IonCardTitle, 
  IonCardContent, 
  IonList, 
  IonItem, 
  IonLabel, 
  IonBadge, 
  IonSpinner 
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { downloadOutline, refreshOutline, timeOutline, checkmarkCircleOutline, alertCircleOutline, informationCircleOutline } from 'ionicons/icons';
import { DataService } from '../../core/services/data.service';
import { AuthService } from '../../core/services/auth.service';
import { StatCardComponent } from '../../shared/components/stat-card/stat-card.component';
import { StatMetric } from '../../core/models/metric.model';
import { SystemNotification } from '../../core/models/record.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonMenuButton,
    IonContent,
    IonGrid,
    IonRow,
    IonCol,
    IonButton,
    IonIcon,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonList,
    IonItem,
    IonLabel,
    IonBadge,
    IonSpinner,
    StatCardComponent
  ],
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss']
})
export class DashboardPage implements OnInit {
  private dataService = inject(DataService);
  private authService = inject(AuthService);

  public metrics: StatMetric[] = [];
  public notifications: SystemNotification[] = [];
  public isLoading: boolean = true;
  public currentUser = this.authService.getCurrentUser();

  constructor() {
    addIcons({
      downloadOutline,
      refreshOutline,
      timeOutline,
      checkmarkCircleOutline,
      alertCircleOutline,
      informationCircleOutline
    });
  }

  ngOnInit(): void {
    this.loadDashboardData();
    this.subscribeToNotifications();
  }

  loadDashboardData(): void {
    this.isLoading = true;
    this.dataService.getDashboardMetrics().subscribe({
      next: (data) => {
        this.metrics = data;
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  subscribeToNotifications(): void {
    this.dataService.notifications$.subscribe(notifs => {
      this.notifications = notifs;
    });
  }

  onExportCSV(): void {
    this.dataService.exportRecordsToCSV();
  }

  onCardClick(metric: StatMetric): void {
    console.log(`Métrica seleccionada: ${metric.title}`);
  }
}
