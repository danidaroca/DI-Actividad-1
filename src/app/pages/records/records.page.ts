import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonButtons, 
  IonMenuButton, 
  IonContent, 
  IonButton, 
  IonIcon, 
  IonModal, 
  IonItem, 
  IonLabel, 
  IonInput, 
  IonSelect, 
  IonSelectOption, 
  IonSpinner, 
  IonNote,
  IonToast
} from '@ionic/angular';
import { addIcons } from 'ionicons';
import { addOutline, downloadOutline, refreshOutline, closeOutline, checkmarkOutline, cubeOutline } from 'ionicons/icons';
import { DataService } from '../../core/services/data.service';
import { AuthService } from '../../core/services/auth.service';
import { AsyncValidatorService } from '../../core/services/async-validator.service';
import { BusinessRecord } from '../../core/models/record.model';
import { DataTableComponent, TableColumn } from '../../shared/components/data-table/data-table.component';

@Component({
  selector: 'app-records',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonMenuButton,
    IonContent,
    IonButton,
    IonIcon,
    IonModal,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonSpinner,
    IonNote,
    IonToast,
    DataTableComponent
  ],
  templateUrl: './records.page.html',
  styleUrls: ['./records.page.scss']
})
export class RecordsPage implements OnInit {
  private dataService = inject(DataService);
  private authService = inject(AuthService);
  private asyncValidator = inject(AsyncValidatorService);
  private fb = inject(FormBuilder);

  public records: BusinessRecord[] = [];
  public isLoading: boolean = true;
  public isModalOpen: boolean = false;
  public isSubmitting: boolean = false;
  public toastMessage: string | null = null;
  public isToastOpen: boolean = false;

  public isAdmin = this.authService.isAdmin();

  // Columnas configuradas para el componente reutilizable DataTable
  public tableColumns: TableColumn[] = [
    { key: 'code', label: 'Código', type: 'text' },
    { key: 'name', label: 'Descripción / Nombre', type: 'text' },
    { key: 'category', label: 'Categoría', type: 'text' },
    { key: 'stock', label: 'Stock', type: 'number' },
    { key: 'price', label: 'Precio', type: 'currency' },
    { key: 'status', label: 'Estado', type: 'badge' }
  ];

  // Formulario reactivo de alta de nuevo registro
  public recordForm: FormGroup;

  constructor() {
    addIcons({
      addOutline,
      downloadOutline,
      refreshOutline,
      closeOutline,
      checkmarkOutline,
      cubeOutline
    });

    this.recordForm = this.fb.group({
      code: [
        '',
        [Validators.required, Validators.pattern(/^[A-Z]{3,4}-\d{3}$/)],
        [this.asyncValidator.codeAvailableValidator()] // Validación asíncrona
      ],
      name: ['', [Validators.required, Validators.minLength(4)]],
      category: ['Tecnología', [Validators.required]],
      stock: [1, [Validators.required, Validators.min(0)]],
      price: [99.99, [Validators.required, Validators.min(0.01)]],
      status: ['DISPONIBLE', [Validators.required]]
    });
  }

  get code() { return this.recordForm.get('code'); }
  get name() { return this.recordForm.get('name'); }
  get stock() { return this.recordForm.get('stock'); }
  get price() { return this.recordForm.get('price'); }

  ngOnInit(): void {
    this.fetchRecords();
  }

  fetchRecords(): void {
    this.isLoading = true;
    this.dataService.getRecords().subscribe({
      next: (data) => {
        this.records = data;
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  openCreateModal(): void {
    this.recordForm.reset({
      category: 'Tecnología',
      stock: 1,
      price: 50.00,
      status: 'DISPONIBLE'
    });
    this.isModalOpen = true;
  }

  closeModal(): void {
    this.isModalOpen = false;
  }

  onSubmitRecord(): void {
    if (this.recordForm.invalid) {
      this.recordForm.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    this.dataService.addRecord(this.recordForm.value).subscribe({
      next: (newRec) => {
        this.isSubmitting = false;
        this.closeModal();
        this.fetchRecords();
        this.showToast(`Registro ${newRec.code} creado satisfactoriamente.`);
      },
      error: () => {
        this.isSubmitting = false;
      }
    });
  }

  onDeleteRecord(item: BusinessRecord): void {
    if (!this.isAdmin) {
      this.showToast('Acción restringida: solo los administradores pueden eliminar registros.');
      return;
    }

    this.dataService.deleteRecord(item.id).subscribe({
      next: () => {
        this.fetchRecords();
        this.showToast(`Elemento ${item.code} eliminado correctamente.`);
      }
    });
  }

  onSelectRecord(item: BusinessRecord): void {
    this.showToast(`Detalles de: ${item.name} (${item.code})`);
  }

  onExportCSV(): void {
    this.dataService.exportRecordsToCSV();
  }

  private showToast(msg: string): void {
    this.toastMessage = msg;
    this.isToastOpen = true;
  }
}
