import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { 
  IonSearchbar, 
  IonButton, 
  IonIcon, 
  IonBadge, 
  IonSelect, 
  IonSelectOption,
  IonSpinner
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { trashOutline, createOutline, eyeOutline, chevronBackOutline, chevronForwardOutline, filterOutline } from 'ionicons/icons';

export interface TableColumn {
  key: string;
  label: string;
  type?: 'text' | 'currency' | 'badge' | 'number' | 'date';
}

@Component({
  selector: 'app-data-table',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    IonSearchbar, 
    IonButton, 
    IonIcon, 
    IonBadge, 
    IonSelect, 
    IonSelectOption,
    IonSpinner
  ],
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DataTableComponent {
  // Inputs requeridos y configurables
  @Input({ required: true }) set data(value: any[]) {
    this._dataSignal.set(value || []);
    this.currentPage.set(1);
  }
  @Input({ required: true }) columns: TableColumn[] = [];
  @Input() searchPlaceholder: string = 'Buscar registros...';
  @Input() emptyMessage: string = 'No se encontraron elementos.';
  @Input() showActions: boolean = true;
  @Input() canDelete: boolean = true;
  @Input() canEdit: boolean = true;
  @Input() isLoading: boolean = false;
  @Input() pageSize: number = 5;

  // Outputs personalizados
  @Output() rowSelect = new EventEmitter<any>();
  @Output() rowEdit = new EventEmitter<any>();
  @Output() rowDelete = new EventEmitter<any>();

  // Estado reactivo interno mediante Angular Signals
  private _dataSignal = signal<any[]>([]);
  public searchTerm = signal<string>('');
  public currentPage = signal<number>(1);
  public selectedCategory = signal<string>('ALL');

  // Categorías extraídas automáticamente
  public categories = computed(() => {
    const list = this._dataSignal();
    const cats = new Set<string>();
    list.forEach(item => {
      if (item.category) cats.add(item.category);
    });
    return Array.from(cats);
  });

  // Datos filtrados por texto y categoría
  public filteredData = computed(() => {
    const list = this._dataSignal();
    const query = this.searchTerm().trim().toLowerCase();
    const cat = this.selectedCategory();

    return list.filter(item => {
      const matchCat = cat === 'ALL' || item.category === cat;
      if (!matchCat) return false;

      if (!query) return true;
      return Object.values(item).some(val => 
        String(val).toLowerCase().includes(query)
      );
    });
  });

  // Paginación
  public totalPages = computed(() => {
    const count = this.filteredData().length;
    return Math.max(1, Math.ceil(count / this.pageSize));
  });

  public paginatedData = computed(() => {
    const filtered = this.filteredData();
    const start = (this.currentPage() - 1) * this.pageSize;
    return filtered.slice(start, start + this.pageSize);
  });

  constructor() {
    addIcons({
      trashOutline,
      createOutline,
      eyeOutline,
      chevronBackOutline,
      chevronForwardOutline,
      filterOutline
    });
  }

  onSearch(event: any): void {
    const val = event.detail?.value || '';
    this.searchTerm.set(val);
    this.currentPage.set(1);
  }

  onCategoryChange(event: any): void {
    this.selectedCategory.set(event.detail?.value || 'ALL');
    this.currentPage.set(1);
  }

  prevPage(): void {
    if (this.currentPage() > 1) {
      this.currentPage.update(p => p - 1);
    }
  }

  nextPage(): void {
    if (this.currentPage() < this.totalPages()) {
      this.currentPage.update(p => p + 1);
    }
  }

  onRowClick(item: any): void {
    this.rowSelect.emit(item);
  }

  onEditClick(event: Event, item: any): void {
    event.stopPropagation();
    this.rowEdit.emit(item);
  }

  onDeleteClick(event: Event, item: any): void {
    event.stopPropagation();
    this.rowDelete.emit(item);
  }

  getBadgeColor(status: string): string {
    switch (status) {
      case 'DISPONIBLE': return 'success';
      case 'AGOTADO': return 'danger';
      case 'RESERVADO': return 'warning';
      default: return 'medium';
    }
  }
}
