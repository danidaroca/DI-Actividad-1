export interface StatMetric {
  id: string;
  title: string;
  value: string | number;
  subtitle?: string;
  changePercentage?: number;
  trend?: 'up' | 'down' | 'neutral';
  iconName?: string;
  colorTheme?: 'primary' | 'success' | 'warning' | 'danger' | 'tertiary';
}
