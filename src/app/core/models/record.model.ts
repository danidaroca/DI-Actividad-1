export interface BusinessRecord {
  id: string;
  code: string;
  name: string;
  category: 'Tecnología' | 'Mobiliario' | 'Servicios' | 'Suministros';
  stock: number;
  price: number;
  status: 'DISPONIBLE' | 'AGOTADO' | 'RESERVADO';
  lastUpdated: string;
}

export interface SystemNotification {
  id: string;
  timestamp: string;
  type: 'INFO' | 'WARNING' | 'SUCCESS';
  message: string;
}
