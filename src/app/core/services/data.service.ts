import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable, of, throwError, forkJoin } from 'rxjs';
import { delay, map, tap, take } from 'rxjs/operators';
import { BusinessRecord, SystemNotification } from '../models/record.model';
import { StatMetric } from '../models/metric.model';
import { AsyncValidatorService } from './async-validator.service';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export interface DashboardConsolidated {
  metrics: StatMetric[];
  records: BusinessRecord[];
  notifications: SystemNotification[];
}

export interface CategoryDistribution {
  categories: string[];
  stockPerCategory: number[];
  valuePerCategory: number[];
}

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
    },
    {
      id: 'rec-6',
      code: 'PROD-004',
      name: 'Teclado Mecánico Inalámbrico RGB',
      category: 'Tecnología',
      stock: 35,
      price: 119.95,
      status: 'DISPONIBLE',
      lastUpdated: '2026-10-25'
    },
    {
      id: 'rec-7',
      code: 'MOB-102',
      name: 'Mesa Elevable Eléctrica Doble Motor',
      category: 'Mobiliario',
      stock: 8,
      price: 489.00,
      status: 'DISPONIBLE',
      lastUpdated: '2026-10-26'
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
   * Orquestación asíncrona avanzada concurrente mediante forkJoin (Paso 3.1 - RA 5 Sobresaliente).
   * Consolida fuentes simultáneas de SQL y NoSQL con gestión de errores.
   */
  public getDashboardConsolidatedData(): Observable<DashboardConsolidated> {
    return forkJoin({
      metrics: this.getDashboardMetrics(),
      records: this.getRecords(),
      notifications: this.notifications$.pipe(take(1))
    }).pipe(
      delay(300)
    );
  }

  /**
   * Obtiene la distribución agregada por categorías para alimentar gráficos de Chart.js
   */
  public getCategoryDistribution(): Observable<CategoryDistribution> {
    return this.getRecords().pipe(
      map(records => {
        const catMap = new Map<string, { stock: number; value: number }>();

        records.forEach(r => {
          const current = catMap.get(r.category) || { stock: 0, value: 0 };
          current.stock += r.stock;
          current.value += (r.stock * r.price);
          catMap.set(r.category, current);
        });

        const categories = Array.from(catMap.keys());
        const stockPerCategory = categories.map(c => catMap.get(c)!.stock);
        const valuePerCategory = categories.map(c => parseFloat(catMap.get(c)!.value.toFixed(2)));

        return {
          categories,
          stockPerCategory,
          valuePerCategory
        };
      })
    );
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
    const headers = ['ID', 'Código', 'Nombre', 'Categoría', 'Stock', 'Precio (€)', 'Total (€)', 'Estado', 'Última Actualización'];
    const rows = this.mockRecords.map(r => [
      `"${r.id}"`,
      `"${r.code}"`,
      `"${r.name.replace(/"/g, '""')}"`,
      `"${r.category}"`,
      r.stock,
      r.price.toFixed(2),
      (r.stock * r.price).toFixed(2),
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

  /**
   * Exportación robusta de informes tabulados con diseño en PDF (Paso 3.3 - RA 5 Sobresaliente)
   * Genera un documento corporativo con encabezado, métricas globales, tabla estilizada y pie de página.
   */
  public exportRecordsToPDF(): void {
    const doc = new jsPDF({
      orientation: 'landscape',
      unit: 'mm',
      format: 'a4'
    });

    const todayStr = new Date().toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });

    // 1. Encabezado corporativo
    doc.setFillColor(30, 58, 138); // Navy blue #1e3a8a
    doc.rect(0, 0, 297, 24, 'F');

    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.text('SISTEMA DE GESTIÓN MULTIPLATAFORMA (PWA/HÍBRIDA)', 14, 12);

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.text('MÓDULO: DESARROLLO DE INTERFACES (0488) | DAM - INFORME TABULADO OFICIAL', 14, 18);
    doc.text(`Generado: ${todayStr}`, 230, 18);

    // 2. Resumen ejecutivo de métricas (KPIs)
    const totalRecords = this.mockRecords.length;
    const totalStock = this.mockRecords.reduce((acc, r) => acc + r.stock, 0);
    const totalValue = this.mockRecords.reduce((acc, r) => acc + (r.stock * r.price), 0);
    const outOfStock = this.mockRecords.filter(r => r.stock === 0).length;

    doc.setTextColor(31, 41, 55);
    doc.setFontSize(11);
    doc.setFont('helvetica', 'bold');
    doc.text('RESUMEN CONSOLIDADO DE INVENTARIO Y ACTIVOS', 14, 33);

    // Cajas de resumen KPI
    const kpiBoxes = [
      { label: 'Total Registros', val: `${totalRecords} items`, fill: [238, 242, 255], border: [99, 102, 241] },
      { label: 'Unidades en Stock', val: `${totalStock} uds`, fill: [240, 253, 244], border: [34, 197, 94] },
      { label: 'Valoración Activos', val: `${totalValue.toLocaleString('es-ES', { minimumFractionDigits: 2 })} €`, fill: [254, 243, 199], border: [245, 158, 11] },
      { label: 'Alertas de Stock', val: `${outOfStock} agotados`, fill: [254, 242, 242], border: [239, 68, 68] }
    ];

    let startX = 14;
    kpiBoxes.forEach(k => {
      doc.setFillColor(k.fill[0], k.fill[1], k.fill[2]);
      doc.setDrawColor(k.border[0], k.border[1], k.border[2]);
      doc.setLineWidth(0.5);
      doc.roundedRect(startX, 37, 62, 14, 2, 2, 'FD');

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7.5);
      doc.setTextColor(75, 85, 99);
      doc.text(k.label, startX + 4, 42);

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(10);
      doc.setTextColor(17, 24, 39);
      doc.text(k.val, startX + 4, 48);

      startX += 68;
    });

    // 3. Tabla tabulada avanzada con autoTable
    const tableHeaders = [['Código', 'Nombre / Descripción del Artículo', 'Categoría', 'Stock', 'Precio (€)', 'Valor Total (€)', 'Estado']];
    const tableBody = this.mockRecords.map(r => [
      r.code,
      r.name,
      r.category,
      r.stock.toString(),
      `${r.price.toFixed(2)} €`,
      `${(r.stock * r.price).toFixed(2)} €`,
      r.status
    ]);

    autoTable(doc, {
      head: tableHeaders,
      body: tableBody,
      startY: 56,
      theme: 'grid',
      styles: {
        fontSize: 8.5,
        cellPadding: 3,
        valign: 'middle'
      },
      headStyles: {
        fillColor: [30, 58, 138],
        textColor: [255, 255, 255],
        fontStyle: 'bold',
        halign: 'left'
      },
      alternateRowStyles: {
        fillColor: [248, 250, 252]
      },
      columnStyles: {
        0: { cellWidth: 26, fontStyle: 'bold' },
        1: { cellWidth: 90 },
        2: { cellWidth: 35 },
        3: { cellWidth: 22, halign: 'center' },
        4: { cellWidth: 28, halign: 'right' },
        5: { cellWidth: 35, halign: 'right', fontStyle: 'bold' },
        6: { cellWidth: 33, halign: 'center' }
      },
      didParseCell: (data) => {
        if (data.section === 'body' && data.column.index === 6) {
          const val = data.cell.raw;
          if (val === 'DISPONIBLE') {
            data.cell.styles.textColor = [22, 101, 52];
            data.cell.styles.fontStyle = 'bold';
          } else if (val === 'AGOTADO') {
            data.cell.styles.textColor = [185, 28, 28];
            data.cell.styles.fontStyle = 'bold';
          } else if (val === 'RESERVADO') {
            data.cell.styles.textColor = [180, 83, 9];
          }
        }
      },
      didDrawPage: (data) => {
        // Pie de página con numeración
        const pageCount = (doc as any).internal.getNumberOfPages();
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text(
          `Documento oficial de control de inventario - Página ${data.pageNumber} de ${pageCount}`,
          14,
          202
        );
        doc.text(
          'Sistema Empresarial Híbrido PWA - DI 0488',
          240,
          202
        );
      }
    });

    doc.save(`informe_inventario_oficial_${new Date().toISOString().split('T')[0]}.pdf`);
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
