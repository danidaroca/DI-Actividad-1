import { Component, OnInit, AfterViewInit, OnDestroy, ElementRef, ViewChild, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
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
  IonCardSubtitle, 
  IonCardContent, 
  IonList, 
  IonItem, 
  IonLabel, 
  IonBadge, 
  IonSpinner,
  IonSegment,
  IonSegmentButton,
  IonToast
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { 
  downloadOutline, 
  refreshOutline, 
  timeOutline, 
  checkmarkCircleOutline, 
  alertCircleOutline, 
  informationCircleOutline,
  documentTextOutline,
  pieChartOutline,
  barChartOutline,
  filterOutline
} from 'ionicons/icons';
import { DataService, DashboardConsolidated, CategoryDistribution } from '../../core/services/data.service';
import { AuthService } from '../../core/services/auth.service';
import { StatCardComponent } from '../../shared/components/stat-card/stat-card.component';
import { StatMetric } from '../../core/models/metric.model';
import { BusinessRecord, SystemNotification } from '../../core/models/record.model';
import { Chart, registerables } from 'chart.js';

// Registrar controladores y elementos estándar de Chart.js
Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
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
    IonCardSubtitle,
    IonCardContent,
    IonList,
    IonItem,
    IonLabel,
    IonBadge,
    IonSpinner,
    IonSegment,
    IonSegmentButton,
    IonToast,
    StatCardComponent
  ],
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss']
})
export class DashboardPage implements OnInit, AfterViewInit, OnDestroy {
  private dataService = inject(DataService);
  private authService = inject(AuthService);

  @ViewChild('barCanvas') barCanvas?: ElementRef<HTMLCanvasElement>;
  @ViewChild('donutCanvas') donutCanvas?: ElementRef<HTMLCanvasElement>;

  public metrics: StatMetric[] = [];
  public records: BusinessRecord[] = [];
  public notifications: SystemNotification[] = [];
  public categoryDist?: CategoryDistribution;
  public isLoading: boolean = true;
  public currentUser = this.authService.getCurrentUser();

  // Filtro interactivo en tiempo real del gráfico (Paso 3.2 - RA 5)
  public chartMetricMode: 'stock' | 'value' = 'stock';
  public selectedCategoryFilter: string = 'ALL';

  public isToastOpen: boolean = false;
  public toastMessage: string = '';

  // Instancias de Chart.js para control del ciclo de vida y prevención de memory leaks
  private barChartInstance?: Chart;
  private donutChartInstance?: Chart;

  constructor() {
    addIcons({
      downloadOutline,
      refreshOutline,
      timeOutline,
      checkmarkCircleOutline,
      alertCircleOutline,
      informationCircleOutline,
      documentTextOutline,
      pieChartOutline,
      barChartOutline,
      filterOutline
    });
  }

  ngOnInit(): void {
    this.loadConsolidatedData();
    this.subscribeToNotifications();
  }

  ngAfterViewInit(): void {
    // Los gráficos se instanciarán una vez finalice la carga de datos
  }

  ngOnDestroy(): void {
    // Destrucción explícita de gráficos para evitar fugas de memoria (Rubric RA 3)
    this.destroyCharts();
  }

  /**
   * Orquestación asíncrona avanzada mediante RxJS forkJoin (Paso 3.1)
   */
  public loadConsolidatedData(): void {
    this.isLoading = true;

    this.dataService.getDashboardConsolidatedData().subscribe({
      next: (consolidated: DashboardConsolidated) => {
        this.metrics = consolidated.metrics;
        this.records = consolidated.records;
        this.notifications = consolidated.notifications;

        // Calcular distribución de categorías
        this.dataService.getCategoryDistribution().subscribe({
          next: (dist) => {
            this.categoryDist = dist;
            this.isLoading = false;
            // Permitir renderizado del DOM antes de inicializar canvases
            setTimeout(() => {
              this.renderCharts();
            }, 50);
          },
          error: () => {
            this.isLoading = false;
          }
        });
      },
      error: (err) => {
        this.isLoading = false;
        this.showToast('Error al sincronizar datos consolidados.');
      }
    });
  }

  public subscribeToNotifications(): void {
    this.dataService.notifications$.subscribe(notifs => {
      this.notifications = notifs;
    });
  }

  /**
   * Renderizado de gráficos interactivos con Chart.js (Paso 3.2)
   */
  private renderCharts(): void {
    if (!this.categoryDist) return;

    this.destroyCharts();

    // 1. Gráfico de Barras: Unidades vs Valor por Categoría
    if (this.barCanvas?.nativeElement) {
      const isStock = this.chartMetricMode === 'stock';
      const chartData = isStock 
        ? this.categoryDist.stockPerCategory 
        : this.categoryDist.valuePerCategory;

      const label = isStock ? 'Unidades en Stock' : 'Valor Total (€)';
      const bgColors = [
        'rgba(59, 130, 246, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(139, 92, 246, 0.8)'
      ];
      const borderColors = [
        '#2563eb',
        '#059669',
        '#d97706',
        '#7c3aed'
      ];

      this.barChartInstance = new Chart(this.barCanvas.nativeElement, {
        type: 'bar',
        data: {
          labels: this.categoryDist.categories,
          datasets: [{
            label: label,
            data: chartData,
            backgroundColor: bgColors,
            borderColor: borderColors,
            borderWidth: 1.5,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                boxWidth: 14,
                font: { size: 12, family: 'system-ui' }
              }
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const val = context.raw as number;
                  return isStock ? ` ${val} unidades` : ` ${val.toLocaleString('es-ES')} €`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(226, 232, 240, 0.6)' },
              ticks: {
                callback: (val) => isStock ? `${val} uds` : `${val} €`
              }
            },
            x: {
              grid: { display: false }
            }
          }
        }
      });
    }

    // 2. Gráfico de Donut: Cuota porcentual de activos
    if (this.donutCanvas?.nativeElement) {
      const donutData = this.categoryDist.valuePerCategory;

      this.donutChartInstance = new Chart(this.donutCanvas.nativeElement, {
        type: 'doughnut',
        data: {
          labels: this.categoryDist.categories,
          datasets: [{
            data: donutData,
            backgroundColor: [
              '#3b82f6',
              '#10b981',
              '#f59e0b',
              '#8b5cf6'
            ],
            hoverOffset: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                boxWidth: 12,
                font: { size: 11 }
              }
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const val = context.raw as number;
                  return ` ${context.label}: ${val.toLocaleString('es-ES')} €`;
                }
              }
            }
          },
          cutout: '65%'
        }
      });
    }
  }

  /**
   * Cambio interactivo de modo métrico en tiempo real (Paso 3.2)
   */
  public onMetricModeChange(mode: 'stock' | 'value'): void {
    this.chartMetricMode = mode;
    this.renderCharts();
    this.showToast(`Vista de gráfico cambiada a: ${mode === 'stock' ? 'Unidades en Stock' : 'Valoración Económica (€)'}`);
  }

  private destroyCharts(): void {
    if (this.barChartInstance) {
      this.barChartInstance.destroy();
      this.barChartInstance = undefined;
    }
    if (this.donutChartInstance) {
      this.donutChartInstance.destroy();
      this.donutChartInstance = undefined;
    }
  }

  public onExportCSV(): void {
    this.dataService.exportRecordsToCSV();
    this.showToast('Informe CSV descargado correctamente.');
  }

  public onExportPDF(): void {
    this.dataService.exportRecordsToPDF();
    this.showToast('Informe tabulado en PDF generado y descargado.');
  }

  public onCardClick(metric: StatMetric): void {
    this.showToast(`Métrica seleccionada: ${metric.title} (${metric.value})`);
  }

  private showToast(msg: string): void {
    this.toastMessage = msg;
    this.isToastOpen = true;
  }
}
