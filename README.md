# Sistema de Gestión Multiplataforma (PWA/Híbrida)

**Módulo Profesional:** Desarrollo de Interfaces (Código: 0488)  
**Ciclo Formativo:** Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM)  
**Actividad:** Actividad Individual 1 - Proyecto de Evaluación Práctica (Entregable Final)  
**Autor:** Daniel Daroca  
**Repositorio GitHub:** [https://github.com/danidaroca/DI-Actividad-1](https://github.com/danidaroca/DI-Actividad-1)  

---

## 📌 1. Descripción General del Proyecto

Aplicación de gestión empresarial multiplataforma desarrollada desde cero utilizando el framework **Ionic 9** sobre arquitectura **Angular 22 (Standalone Components)**. 

El proyecto implementa una arquitectura desacoplada y robusta, consumo asíncrono de orígenes duales de datos (API REST SQL relacional + Servicio de eventos en tiempo real NoSQL/Firestore mockeado mediante `BehaviorSubject`), control de acceso estricto basado en roles (RBAC con `authGuard` y `roleGuard`), dashboard ejecutivo interactivo con gráficos **Chart.js**, generación y descarga de informes tabulados oficiales en **PDF y CSV**, cumplimiento integral de normativas de accesibilidad **WCAG 2.1**, documentación técnica automatizada con **Compodoc** y pipeline de integración continua **CI/CD** con despliegue en la nube.

---

## 🏗️ 2. Arquitectura del Software

```
src/
├── app/
│   ├── core/                           # Capa singleton: servicios, modelos y seguridad
│   │   ├── guards/
│   │   │   ├── auth.guard.ts           # Protección de rutas privadas (redirección a login)
│   │   │   └── role.guard.ts           # Control de acceso por roles (ADMIN vs STANDARD)
│   │   ├── models/
│   │   │   ├── user.model.ts           # Modelos de usuario, credenciales y roles
│   │   │   ├── record.model.ts         # Entidades de inventario y notificaciones
│   │   │   └── metric.model.ts         # Métricas KPI consolidadas
│   │   └── services/
│   │       ├── auth.service.ts         # Autenticación, JWT sintético y sesiones reactivas
│   │       ├── async-validator.service.ts # Validaciones asíncronas contra backend simulado
│   │       └── data.service.ts         # Consumo dual (SQL + NoSQL), forkJoin, exportación PDF/CSV
│   ├── pages/                          # Vistas enrutadas con Carga Diferida (Lazy Loading)
│   │   ├── login/                      # Formulario reactivo de login con botones demo
│   │   ├── register/                   # Formulario de alta con validación asíncrona de email
│   │   ├── dashboard/                  # Cuadro de mando con Chart.js y filtros en tiempo real (ADMIN)
│   │   ├── records/                    # Gestión de inventario, modal reactivo y exportación
│   │   └── help/                       # Manual de usuario interactivo embebido
│   └── shared/                         # Componentes reutilizables e independientes
│       └── components/
│           ├── stat-card/              # Widget KPI instanciable (@Input/@Output, OnPush)
│           └── data-table/             # Tabla avanzada con buscador, filtros y Signals
├── assets/                             # Recursos estáticos e iconos
└── theme/                              # Variables y estilos globales de diseño
```

---

## 🚀 3. Estado de Ejecución de las Fases (100% Completadas)

### ✅ FASE 1: Estructuración y Renderizado Declarativo (RA 1 y RA 2)
* **Paso 1.1 - Sistema de Enrutamiento y Navegación:**
  * Menú lateral responsivo (`Side Menu`) interactivo con carga diferida (`Lazy Loading` mediante `loadComponent`).
  * Protección robusta de rutas mediante `authGuard` y `roleGuard`.
  * Control de acceso por roles: **Administrador** (acceso total + Cuadro de Mando) y **Usuario Estándar** (catálogo e inventario).
* **Paso 1.2 - Formularios y Validaciones Asíncronas:**
  * Formulario reactivo de **Login** con gestión de errores UX declarativa.
  * Formulario reactivo de **Alta de Usuario** con **validación asíncrona** en tiempo real (`AsyncValidatorService`) que comprueba la existencia de correo en base de datos con indicador `PENDING` (spinner), validación positiva (check verde) y control de duplicados.
  * Formulario de **Alta de Registros** con validación asíncrona de código único de producto (`PROD-XXX`) y validaciones síncronas de formato.

### ✅ FASE 2: Componentización Visual y Lógica de Negocio (RA 3)
* **Paso 2.1 - Componentes Personalizados:**
  * `<app-stat-card>`: Widget estadístico/KPI modular para representar valores consolidados, porcentajes de variación, indicadores de tendencia y temas cromáticos.
  * `<app-data-table>`: Tabla de datos agnóstica con buscador reactivo instantáneo, filtro por categorías, paginación y columnas dinámicas tipadas.
* **Paso 2.2 - Gestión de Estado y Eventos:**
  * Componentes totalmente independientes del contenedor padre con estrategia `ChangeDetectionStrategy.OnPush`.
  * Paso de datos declarativo vía `@Input()` / Signals y emisión desacoplada mediante `@Output()` (`rowSelect`, `rowDelete`, `rowEdit`, `cardClick`).

### ✅ FASE 3: Consumo de Datos y Generación de Informes (RA 5)
* **Paso 3.1 - Concurrencia y Asincronía:**
  * Simulación de consumo dual: API REST relacional (SQL) para inventario transaccional y servicio en tiempo real NoSQL (Firestore Mock) basado en `BehaviorSubject` para auditoría y logs.
  * Orquestación asíncrona avanzada mediante **RxJS `forkJoin`** con control de spinners de carga y gestión de errores.
* **Paso 3.2 - Dashboard Interactivo con Chart.js:**
  * Gráficos visuales dinámicos de **Barras** (Stock/Valor por categoría) y **Doughnut** (Cuota económica de activos).
  * Filtro interactivo en tiempo real que permite conmutar entre "Unidades en Stock" y "Valoración Económica (€)" recalculando la visualización al instante.
  * Ciclo de vida optimizado con destrucción explícita de instancias en `ngOnDestroy` para evitar memory leaks.
* **Paso 3.3 - Exportación de Datos:**
  * **Exportación a PDF Oficial:** Generación en cliente con `jsPDF` y `jspdf-autotable`, incluyendo membrete institucional, tarjetas resumen KPI, tabla formateada con colores semánticos y paginación automática.
  * **Exportación a CSV Normalizado:** Archivo delimitado con cabeceras estándar y codificación `UTF-8 BOM` para compatibilidad directa con Excel.

### ✅ FASE 4: Usabilidad, Accesibilidad y Calidad (RA 4)
* **Paso 4.1 - Diseño Adaptativo (Responsive):**
  * Enfoque **Mobile-First** con adaptación anatómica fluida para smartphones, tablets y pantallas de escritorio.
* **Paso 4.2 - Cumplimiento WCAG y WAI-ARIA:**
  * Contraste de color reglamentario, tipografía escalable, control total de navegación mediante teclado (`tabindex='0'` y eventos de tecla Enter) y atributos semánticos `WAI-ARIA` (`role="table"`, `role="region"`, `aria-label`, `aria-busy`, `aria-live`).

### ✅ FASE 5: Documentación, Control de Versiones y Despliegue (RA 6 y RA 7)
* **Paso 5.1 - Control de Versiones Git Flow:**
  * Historial íntegro de commits y ramas estructuradas: `main`, `develop`, `feature/fase1-enrutamiento-auth`, `feature/fase2-componentes`, `feature/fase3-dashboard-informes` y `feature/fase5-compodoc-ci`.
* **Paso 5.2 - Documentación Técnica y de Usuario:**
  * Documentación técnica generada automáticamente con **Compodoc** en la carpeta `documentation/`.
  * Manual de usuario interactivo embebido en la aplicación en la ruta `/help` y redactado exhaustivamente en este `README.md`.
* **Paso 5.3 - Despliegue en Producción y CI/CD:**
  * Configuración para despliegue en **Vercel** (`vercel.json`) con redirecciones SPA y cabeceras de seguridad.
  * Pipeline automatizado de integración continua con **GitHub Actions** (`ci/workflows/ci.yml`) que valida tests, compila con Compodoc y genera el artefacto en `www/`.

---

## 🔑 4. Credenciales de Acceso de Prueba

La pantalla de login (`/login`) cuenta con botones de **autocompletado en un solo clic** para agilizar la corrección docente:

| Rol | Correo Electrónico | Contraseña | Vistas y Funcionalidades Accesibles |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin@empresa.com` | `Admin123!` | Acceso completo: Cuadro de Mando con Chart.js, Gestión de Inventario, Altas, Borrado de artículos, Exportación PDF/CSV y Manual de ayuda. |
| **Usuario Estándar** | `user@empresa.com` | `User123!` | Acceso operativo: Catálogo de Inventario, Alta de nuevos productos, Exportación de informes y Manual de ayuda. *(Ruta `/dashboard` protegida por `roleGuard`)*. |

---

## 💻 5. Instalación y Ejecución Local

### Prerrequisitos
* **Node.js** (v18 o superior)
* **NPM** (v9 o superior)
* **Ionic CLI** (opcional, `npm install -g @ionic/cli`)

### Instrucciones
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/danidaroca/DI-Actividad-1.git
   cd DI-Actividad-1
   ```
2. **Instalar dependencias:**
   ```bash
   npm install
   ```
3. **Ejecutar el servidor de desarrollo:**
   ```bash
   npm start
   # o bien mediante Ionic:
   ionic serve
   ```
   Acceder desde el navegador a: [http://localhost:8100](http://localhost:8100)

4. **Generar la documentación técnica con Compodoc:**
   ```bash
   npm run compodoc:build
   # Para visualizar la documentación interactiva en el puerto 8080:
   npm run compodoc:serve
   ```

5. **Compilar para producción:**
   ```bash
   npm run build
   ```
   El artefacto compilado y optimizado se genera en el directorio `www/`.

---

## 🌿 6. Estructura de Ramas (Git Flow)

El desarrollo ha seguido la metodología profesional **Git Flow**:
* `main`: Rama de entrega final y código en producción.
* `develop`: Rama de integración de características.
* `feature/fase1-enrutamiento-auth`: Enrutamiento lazy loading, guards y validación asíncrona.
* `feature/fase2-componentes`: Componentes agnósticos modulares (`StatCard` y `DataTable`).
* `feature/fase3-dashboard-informes`: Dashboard interactivo con Chart.js, forkJoin y exportación PDF/CSV.
* `feature/fase5-compodoc-ci`: Compodoc, pipeline de GitHub Actions y configuración Vercel.
