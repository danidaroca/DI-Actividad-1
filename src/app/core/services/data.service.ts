import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { delay, map, tap } from 'rxjs/operators';
import { BusinessRecord, SystemNotification } from '../models/record.model';
import { StatMetric } from '../models/metric.model';
import { AsyncValidatorService } from './async-validator.service';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private asyncValidator = inject(AsyncValidatorService);

  // Fuente 1: API REST Relacional Mock (SQL)
  private mockRecords: BusinessRecord[] = [
    {
      id: 'rec-1',
      code: 'PROD-001',
      name: 'Portátil Profesional Ultraligero 16GB',
      category: 'Tecnología',
      stock: 24,
      price: 899.99,
      status: 'DISPONIBLE',
      lastUpdated: '2026-10-20'
    },
    {
      id: 'rec-2',
      code: 'PROD-002',
      name: 'Monitor Panorámico 27" 4K IPS',
      category: 'Tecnología',
      stock: 12,
      price: 349.50,
      status: 'DISPONIBLE',
      lastUpdated: '2026-10-21'
    },
    {
      id: 'rec-3',
      code: 'PROD-003',
      name: 'Silla Ergonómica de Oficina Transpirable',
      category: 'Mobiliario',
      stock: 0,
      price: 219.00,
      status: 'AGOTADO',
      lastUpdated: '2026-10-18'
    },
    {
      id: 'rec-4',
      code: 'SRV-101',
      name: 'Mantenimiento Cloud y Soporte 24/7',
      category: 'Servicios',
      stock: 50,
      price: 150.00,
      status: 'DISPONIBLE',
      lastUpdated: '2026-10-22'
    },
    {
      id: 'rec-5',
      code: 'SUM-201',
      name: 'Kit de Conectividad Fibra y Switches',
      category: 'Suministros',
      stock: 5,
      price: 85.20,
      status: 'RESERVADO',
      lastUpdated: '2026-10-24'
    }
  ];

  // Fuente 2: Servicio en tiempo real basado en documentos (NoSQL / Firestore Mock)
  private notificationsSubject = new BehaviorSubject<SystemNotification[]>([
    {
      id: 'notif-1',
      timestamp: '11:45',
      type: 'INFO',
      message: 'Sincronización periódica con la base de datos completada.'
    },
    {
      id: 'notif-2',
      timestamp: '11:50',
      type: 'WARNING',
      message: 'Stock bajo detectado en Kit de Conectividad Fibra.'
    },
    {
      id: 'notif-3',
      timestamp: '11:55',
      type: 'SUCCESS',
      message: 'Copia de seguridad incremental almacenada en réplica NoSQL.'
    }
  ]);
  public notifications$ = this.notificationsSubject.asObservable();

  /**
   * Obtener todos los registros (simula GET a REST API SQL)
   */
  public getRecords(): Observable<BusinessRecord[]> {
    return of([...this.mockRecords]).pipe(delay(450));
  }

  /**
   * Añadir un nuevo registro de negocio
   */
  public addRecord(record: Omit<BusinessRecord, 'id' | 'lastUpdated'>): Observable<BusinessRecord> {
    const newRecord: BusinessRecord = {
      ...record,
      id: `rec-${Date.now()}`,
      lastUpdated: new Date().toISOString().split('T')[0]
    };

    this.mockRecords.unshift(newRecord);
    this.asyncValidator.registerCode(newRecord.code);

    // Emitir evento en tiempo real en la colección NoSQL
    this.emitNotification('INFO', `Nuevo elemento registrado: ${newRecord.name} (${newRecord.code})`);

    return of(newRecord).pipe(delay(500));
  }

  /**
   * Eliminar un registro de negocio
   */
  public deleteRecord(id: string): Observable<boolean> {
    const index = this.mockRecords.findIndex(r => r.id === id);
    if (index === -1) {
      return throwError(() => new Error('Elemento no encontrado.'));
    }

    const deleted = this.mockRecords.splice(index, 1)[0];
    this.emitNotification('WARNING', `Elemento eliminado: ${deleted.name} (${deleted.code})`);
    return of(true).pipe(delay(350));
  }

  /**
   * Obtener métricas consolidadas de negocio para el Cuadro de Mando
   */
  public getDashboardMetrics(): Observable<StatMetric[]> {
    const totalRecords = this.mockRecords.length;
    const totalStock = this.mockRecords.reduce((acc, r) => acc + r.stock, 0);
    const totalValue = this.mockRecords.reduce((acc, r) => acc + (r.stock * r.price), 0);
    const outOfStock = this.mockRecords.filter(r => r.stock === 0).length;

    const metrics: StatMetric[] = [
      {
        id: 'metric-val',
        title: 'Valor Total Activos',
        value: `${totalValue.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} €`,
        subtitle: 'Calculado en tiempo real',
        changePercentage: 8.4,
        trend: 'up',
        iconName: 'cash-outline',
        colorTheme: 'success'
      },
      {
        id: 'metric-stock',
        title: 'Unidades en Stock',
        value: totalStock,
        subtitle: 'Artículos físicos disponibles',
        changePercentage: -2.1,
        trend: 'down',
        iconName: 'cube-outline',
        colorTheme: 'primary'
      },
      {
        id: 'metric-items',
        title: 'Registros Totales',
        value: totalRecords,
        subtitle: 'Catálogo corporativo',
        changePercentage: 12.5,
        trend: 'up',
        iconName: 'layers-outline',
        colorTheme: 'tertiary'
      },
      {
        id: 'metric-alert',
        title: 'Alertas de Stock',
        value: outOfStock,
        subtitle: 'Artículos agotados o críticos',
        changePercentage: 0,
        trend: 'neutral',
        iconName: 'alert-circle-outline',
        colorTheme: outOfStock > 0 ? 'danger' : 'success'
      }
    ];

    return of(metrics).pipe(delay(400));
  }

  /**
   * Exporta la lista de registros a formato CSV estándar (Paso 3.3)
   */
  public exportRecordsToCSV(): void {
    const headers = ['ID', 'Código', 'Nombre', 'Categoría', 'Stock', 'Precio (€)', 'Estado', 'Última Actualización'];
    const rows = this.mockRecords.map(r => [
      `"${r.id}"`,
      `"${r.code}"`,
      `"${r.name.replace(/"/g, '""')}"`,
      `"${r.category}"`,
      r.stock,
      r.price.toFixed(2),
      `"${r.status}"`,
      `"${r.lastUpdated}"`
    ]);

    const csvContent = '\uFEFF' + [headers.join(';'), ...rows.map(e => e.join(';'))].join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `informe_inventario_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  private emitNotification(type: 'INFO' | 'WARNING' | 'SUCCESS', message: string): void {
    const current = this.notificationsSubject.value;
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    this.notificationsSubject.next([
      {
        id: `notif-${Date.now()}`,
        timestamp: timeStr,
        type,
        message
      },
      ...current.slice(0, 8)
    ]);
  }
}
