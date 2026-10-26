# Sistema de Gestión Multiplataforma (PWA/Híbrida)

**Módulo Profesional:** Desarrollo de Interfaces (Código: 0488)  
**Ciclo Formativo:** Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM)  
**Actividad:** Actividad Individual 1 - Proyecto de Evaluación Práctica  

---

## 📌 1. Descripción del Proyecto

Aplicación de gestión empresarial multiplataforma desarrollada desde cero con **Ionic Framework** y **Angular (Standalone Architecture)**, implementando una arquitectura desacoplada basada en servicios reactivos con RxJS y Angular Signals, control de acceso basado en roles (RBAC) y directrices de accesibilidad WCAG.

Este repositorio contiene la base arquitectónica fundamental, la navegación declarativa y los componentes visuales reutilizables solicitados en las fases iniciales del proyecto.

---

## 🏗️ 2. Arquitectura del Software

El proyecto sigue una arquitectura modular y reactiva:

```
src/
├── app/
│   ├── core/                           # Servicios singleton, modelos y seguridad
│   │   ├── guards/
│   │   │   ├── auth.guard.ts           # Protección de rutas privadas
│   │   │   └── role.guard.ts           # Control de acceso según rol (RBAC)
│   │   ├── models/
│   │   │   ├── user.model.ts           # Modelos de usuario, roles y credenciales
│   │   │   ├── record.model.ts         # Entidades de inventario y eventos
│   │   │   └── metric.model.ts         # Métricas de cuadro de mando
│   │   └── services/
│   │       ├── auth.service.ts         # Autenticación, JWT sintético y sesiones
│   │       ├── async-validator.service.ts # Validaciones asíncronas contra backend
│   │       └── data.service.ts         # Consumo dual (API REST SQL + NoSQL en vivo)
│   ├── pages/                          # Vistas enrutadas con Carga Diferida (Lazy Loading)
│   │   ├── login/                      # Formulario reactivo de inicio de sesión
│   │   ├── register/                   # Alta con validación asíncrona de email
│   │   ├── dashboard/                  # Cuadro de mando ejecutivo (solo ADMIN)
│   │   ├── records/                    # Gestión de registros/inventario con modal de alta
│   │   └── help/                       # Manual de usuario embebido en la aplicación
│   └── shared/                         # Componentes reutilizables e independientes
│       └── components/
│           ├── stat-card/              # Widget de métricas/KPI (Paso 2.1)
│           └── data-table/             # Tabla avanzada con buscador y filtro (Paso 2.1)
```

---

## 🚀 3. Estado de Ejecución de las Fases

Tal como se ha planificado para esta entrega de desarrollo, se han completado las fases estructurales clave y dejado preparados los cimientos para las siguientes:

### ✅ FASE 1: Estructuración y Renderizado Declarativo (COMPLETADA)
* **Paso 1.1 - Enrutamiento y Navegación:**
  * Navegación global con menú lateral interactivo (`Side Menu`) y carga diferida (`Lazy Loading`) mediante `loadComponent()`.
  * Protección de rutas mediante `authGuard` y `roleGuard`.
  * Diferenciación de vistas según dos roles: **Administrador** y **Usuario Estándar**.
* **Paso 1.2 - Formularios y Validaciones Asíncronas:**
  * Formulario reactivo de **Login** con gestión de errores declarativa.
  * Formulario reactivo de **Alta de Usuario** con **validación asíncrona** en tiempo real (`AsyncValidatorService`) que consulta la existencia previa del correo en base de datos.
  * Formulario de **Alta de Registros** con validación asíncrona de código de producto y patrón regex.
  * Feedback visual adaptativo con estados `PENDING` (spinner), `valid` e `invalid`.

### ✅ FASE 2: Componentización Visual y Lógica de Negocio (COMPLETADA)
* **Paso 2.1 - Componentes Personalizados Reutilizables:**
  * `<app-stat-card>`: Widget estadístico/KPI modular para representar valores consolidados, porcentajes de tendencia y temáticas de color.
  * `<app-data-table>`: Tabla de datos agnóstica con barra de búsqueda instantánea, selector de categorías dinámico, paginación y columnas tipadas.
* **Paso 2.2 - Gestión de Estado y Eventos:**
  * Componentes desacoplados e independientes de la vista padre.
  * Comunicación unidireccional estricta mediante `@Input()` / Signals y emisión de eventos mediante `@Output()` (`rowSelect`, `rowDelete`, `rowEdit`, `cardClick`).

### 🟡 FASE 3: Consumo de Datos y Reportes (PARCIALMENTE IMPLEMENTADA)
* **Implementado:** Simulación de consumo dual (`data.service.ts` con API REST relacional SQL y flujo reactivo en tiempo real NoSQL / Firestore mediante `BehaviorSubject`), y función de **exportación de informes tabulados a CSV**.
* **Pendiente para siguientes entregas:** Gráficos visuales avanzados con librería externa (Chart.js) y exportación a PDF con motor de maquetación.

### 🟡 FASE 4: Usabilidad y Accesibilidad (INTEGRADA)
* Enfoque **Mobile-First** con diseño fluido y responsivo en móviles, tablets y monitores.
* Atributos semánticos `WAI-ARIA` (`role="table"`, `role="region"`, `aria-label`, `aria-busy`, `aria-live`) y navegación completa por teclado (`tabindex` lógico y eventos de tecla Enter).

### 🟡 FASE 5: Control de Versiones y Despliegue
* **Implementado:** Inicialización íntegra con **Git Flow** (ramas `main`, `develop` y feature branches: `feature/fase1-enrutamiento-auth` y `feature/fase2-componentes`).
* **Pendiente para siguientes entregas:** Pipeline CI/CD automático y hosting en la nube (Vercel/Firebase).

---

## 🔑 4. Credenciales de Acceso de Prueba

La pantalla de login incluye botones de carga rápida con un solo clic para facilitar la corrección:

| Rol | Correo Electrónico | Contraseña | Permisos |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin@empresa.com` | `Admin123!` | Acceso total: Cuadro de Mando, Gestión, Borrado y Exportación |
| **Usuario Estándar** | `user@empresa.com` | `User123!` | Acceso limitado: Consulta de registros, altas y manual de ayuda |

---

## 💻 5. Instalación y Ejecución Local

### Prerrequisitos
* **Node.js** (v18+)
* **NPM** (v9+)
* **Ionic CLI** (`npm install -g @ionic/cli`)

### Pasos
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/danidaroca/DI-Actividad-1.git
   cd DI-Actividad-1
   ```
2. Instalar dependencias:
   ```bash
   npm install
   ```
3. Iniciar el servidor de desarrollo local:
   ```bash
   ionic serve
   # o bien:
   npm start
   ```
4. Abrir en el navegador: [http://localhost:8100](http://localhost:8100)

### Compilación para Producción
```bash
npm run build
```
Los archivos optimizados para producción se generan en la carpeta `www/`.

---

## 🌿 6. Estructura de Ramas (Git Flow)

* `main`: Código estable y validado para entrega.
* `develop`: Rama principal de integración y desarrollo.
* `feature/fase1-enrutamiento-auth`: Base arquitectónica, enrutamiento lazy loading, guards y formularios con validación asíncrona.
* `feature/fase2-componentes`: Creación de componentes modulares (`StatCard` y `DataTable`) e integración de fuentes de datos.
