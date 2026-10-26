import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonCard, IonCardContent, IonIcon } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { cashOutline, cubeOutline, layersOutline, alertCircleOutline, trendingUpOutline, trendingDownOutline, removeOutline } from 'ionicons/icons';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  imports: [CommonModule, IonCard, IonCardContent, IonIcon],
  templateUrl: './stat-card.component.html',
  styleUrls: ['./stat-card.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class StatCardComponent {
  @Input({ required: true }) title!: string;
  @Input({ required: true }) value!: string | number;
  @Input() subtitle?: string;
  @Input() changePercentage?: number;
  @Input() trend: 'up' | 'down' | 'neutral' = 'neutral';
  @Input() iconName: string = 'layers-outline';
  @Input() colorTheme: 'primary' | 'success' | 'warning' | 'danger' | 'tertiary' = 'primary';

  @Output() cardClick = new EventEmitter<void>();

  constructor() {
    addIcons({
      cashOutline,
      cubeOutline,
      layersOutline,
      alertCircleOutline,
      trendingUpOutline,
      trendingDownOutline,
      removeOutline
    });
  }

  onTriggerClick(): void {
    this.cardClick.emit();
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      this.onTriggerClick();
    }
  }
}
