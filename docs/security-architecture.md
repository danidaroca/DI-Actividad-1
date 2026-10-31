# Memoria Técnica de Arquitectura de Seguridad y Control de Acceso
**Módulo Profesional:** Desarrollo de Interfaces (Código: 0488)  
**Ciclo Formativo:** Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM 2)  
**Autor:** Daniel Daroca  
**Repositorio GitHub:** [https://github.com/danidaroca/DI-Actividad-1](https://github.com/danidaroca/DI-Actividad-1)  
**Entregable Oficial:** `Memoria_Seguridad_Ionic_Daroca_Daniel.pdf` y sección `docs/security-architecture.md`

---

## 1. Alineación Curricular Oficial (Comunidad de Madrid)

El diseño e implementación de la capa de seguridad de la aplicación multiplataforma (Ionic 9 + Angular 22 Standalone) responde a las exigencias curriculares del módulo profesional de Desarrollo de Interfaces:

* **RA 1: Confecciona interfaces de usuario identificando las capacidades del entorno de desarrollo y aplicando patrones de diseño arquitectónicos.**
  * *CE 1.b:* Se han utilizado herramientas y patrones arquitectónicos específicos del entorno de desarrollo (patrones de flujo de navegación reactivo desacoplado mediante Signals, RxJS y separación estricta de capas entre UI, Servicios de Dominio e Infraestructura de Red).
  * *CE 1.f:* Se ha verificado el correcto flujo de control en la navegación entre vistas según el perfil de usuario mediante *Functional Guards* (`CanMatchFn` y `CanActivateFn`), previniendo accesos indebidos y redirigiendo contextualmente.
* **RA 3: Crea componentes y servicios visuales gestionando eventos y comunicación asíncrona.**
  * *CE 3.d:* Se han interceptado y gestionado eventos de red y peticiones HTTP desacoplando totalmente la lógica de interfaz de la de autenticación/autorización mediante una cadena de *Functional HTTP Interceptors* (`HttpInterceptorFn`).
* **RA 6: Documenta interfaces de usuario describiendo su arquitectura, estructura de clases y mecanismos de despliegue/seguridad.**
  * *CE 6.a:* Se han documentado las decisiones arquitectónicas, modelos de privilegios (RBAC) y alternativas técnicas evaluadas con rigor profesional.

---

## 2. Apartado A: Fundamentación Teórico-Técnica

### 2.1. Functional Guards en Angular / Ionic Standalone

A partir de Angular 15+ y consolidado en Angular 17/18+, la arquitectura de protección de rutas prescinde de las clases monolíticas basadas en interfaces (`implements CanActivate`) en favor de **Functional Guards** tipados (`CanMatchFn`, `CanActivateFn`, `CanDeactivateFn`). Estas funciones puras se ejecutan dentro del contexto de inyección del enrutador (`EnvironmentInjector`), permitiendo invocar la función `inject()` directamente sin necesidad de constructores.

```
Petición de Navegación (/dashboard)
        │
        ▼
   [canMatch]  ──── (false) ────► Descarta coincidencia. Chunk JS NO se descarga.
        │ (true)
        ▼
  Descarga Lazy Chunk (loadComponent)
        │
        ▼
  [canActivate] ──── (false) ────► Cancela activación. Redirección con returnUrl.
        │ (true)
        ▼
 Montaje y Renderizado del Componente
```

#### Ciclo de Vida y Tipos de Guards Funcionales:
1. **`CanMatchFn` (Fase de Emparejamiento):**
   * Se ejecuta durante la evaluación inicial de las rutas candidatas, **antes** de que el enrutador intente resolver el módulo o componente de carga perezosa (`loadComponent` o `loadChildren`).
   * Si retorna `false` (o `UrlTree`), el enrutador ignora la definición de ruta actual y continúa evaluando rutas alternativas o de respaldo (`**`).
2. **`CanActivateFn` (Fase de Activación):**
   * Se evalúa una vez que la ruta ha coincidido y el componente ya ha sido descargado en memoria.
   * Determina si el usuario tiene permiso para inicializar el componente. Si retorna `false`, aborta la activación y navega hacia un destino alternativo (`/login`).
3. **`CanDeactivateFn` (Fase de Abandono):**
   * Se ejecuta cuando el usuario intenta abandonar la vista actual (por ejemplo, para prevenir la pérdida de datos no guardados en formularios de alta).

#### Diferencia Crítica en Rendimiento y Lazy Loading (`canActivate` vs `canMatch`):
* En una arquitectura Mobile-First / PWA con bundles pesados (como librerías de analítica `Chart.js` o motores de maquetación `jsPDF`), proteger una ruta exclusivamente con `canActivate` presenta una deficiencia arquitectónica: **el navegador primero descarga el chunk JavaScript correspondiente a través de la red**, y sólo después evalúa el guard para bloquear la vista.
* Al implementar `canMatch`, si un usuario sin rol administrativo intenta acceder a `/dashboard`, el enrutador bloquea la coincidencia **sin solicitar jamás el chunk JS** del dashboard. Esto produce:
  1. **Ahorro de ancho de banda:** Cero transferencia de paquetes JavaScript innecesarios en dispositivos móviles.
  2. **Seguridad reforzada (Zero Leakage):** El código fuente compilado de las vistas y lógicas protegidas nunca llega a la caché del cliente no autorizado.

---

### 2.2. HTTP Interceptors Funcionales (`HttpInterceptorFn`)

Los interceptores HTTP funcionales constituyen un pipeline de middleware basado en el patrón arquitectónico *Chain of Responsibility*. Cada interceptor recibe la petición saliente (`HttpRequest`) y una función de continuación (`HttpHandlerFn` o `next`), permitiendo manipular peticiones salientes y respuestas entrantes mediante flujos reactivos de RxJS.

```
HttpRequest
     │
     ▼
┌─────────────────────────┐
│     authInterceptor     │ ──► Clona request e inyecta 'Authorization: Bearer <token>'
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    errorInterceptor     │ ──► Captura 401 (Refresh/Login) o 403 (Forbidden)
└───────────┬─────────────┘
            │
            ▼
       Backend / API
```

#### Inyección y Propagación de Cabeceras:
* El interceptor autenticador recupera de forma reactiva el token de sesión almacenado y procede a la **clonación inmutable** de la petición original agregando la cabecera `Authorization: Bearer <token>`. La inmutabilidad garantiza que las reintentaciones y cachés intermedias operen de manera determinista.

#### Manejo Centralizado de Excepciones y Estrategia ante Expiración (Refresh Token):
* El interceptor de errores intercepta respuestas erróneas mediante el operador reactivo `catchError`:
  * **HTTP 401 Unauthorized:** Denota token expirado, ausente o manipulado. La estrategia ejecuta un flujo de *Silent Refresh* (si el backend soporta rotación de tokens) o invalida la sesión local llamando a `authService.logout(false)` y navega hacia `/login`, agregando el parámetro contextual `returnUrl` para restaurar la vista previa tras reautenticarse.
  * **HTTP 403 Forbidden:** Identifica que la identidad es legítima, pero carece de permisos de rol para el endpoint solicitado. Se aborta la acción y se redirige a la vista segura `/inventory` emitiendo una notificación al usuario.

---

### 2.3. Control de Acceso Basado en Roles (RBAC - Role-Based Access Control)

#### Definición Formal del Modelo RBAC frente a Identidades Simples:
* En lugar de vincular permisos directamente a usuarios concretos, el modelo **RBAC** introduce una capa intermedia de abstracción formal:
  $$\text{Usuario} \longrightarrow \text{Rol(es)} \longrightarrow \text{Conjunto de Permisos / Operaciones}$$
* Esto desacopla el crecimiento de usuarios de la política de seguridad: añadir un nuevo rol o modificar sus permisos no requiere alterar el código ni la estructura de los usuarios.

#### Diferencia entre Autenticación y Autorización:
* **Autenticación (AuthN - *¿Quién eres?*):** Proceso de verificación criptográfica de la identidad declarada (credenciales email/contraseña, biometría o firma del token). Determina si existe una sesión válida.
* **Autorización (AuthZ - *¿Qué tienes permitido hacer?*):** Evaluación de privilegios en función del rol asignado y los claims contenidos en el token. Determina si el usuario autenticado puede acceder a la vista `/dashboard` o pulsar el botón de eliminación en la tabla.

#### Estructura y Encapsulamiento del Payload JWT (Claims):
El token de sesión contiene en su carga útil (*payload*) las aserciones de seguridad requeridas por el cliente para tomar decisiones instantáneas sin sobrecargar la red:

```json
{
  "sub": "usr-admin-01",
  "email": "admin@empresa.com",
  "role": "ADMIN",
  "permissions": [
    "dashboard:read",
    "inventory:read",
    "inventory:create",
    "inventory:update",
    "inventory:delete",
    "reports:export"
  ],
  "iat": 1730282400,
  "exp": 1730286000
}
```

El servicio `AuthService` decodifica y encapsula estas propiedades en memoria, exponiendo **Angular Signals** reactivas de lectura (`currentUserSignal`, `isAdminSignal`) para que la interfaz se reconfigure en tiempo constante $O(1)$.

---

## 3. Apartado B: Justificación de Implementación en el Proyecto

### 3.1. Ubicación en el Árbol de Rutas y Configuración Global

#### Configuración Global del Pipeline HTTP (`src/main.ts`):
El registro de los interceptores funcionales se centraliza en el arranque de la aplicación mediante la función `provideHttpClient` configurada con `withInterceptors`:

```typescript
// src/main.ts
bootstrapApplication(AppComponent, {
  providers: [
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    provideIonicAngular(),
    provideHttpClient(
      withInterceptors([authInterceptor, errorInterceptor])
    ),
    provideRouter(routes, withPreloading(PreloadAllModules), withComponentInputBinding()),
  ],
});
```

#### Árbol de Enrutamiento (`src/app/app.routes.ts`):
Se combinan `canMatch` (para evitar descargas prematuras de bundles) y `canActivate` (para verificación formal de estado y redirección contextual):

```typescript
// src/app/app.routes.ts
export const routes: Routes = [
  { path: '', redirectTo: 'inventory', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.page').then(m => m.LoginPage)
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.page').then(m => m.RegisterPage)
  },
  {
    path: 'dashboard',
    canMatch: [authMatchGuard, roleMatchGuard],
    canActivate: [authGuard, roleGuard],
    data: { expectedRole: 'ADMIN' },
    loadComponent: () => import('./pages/dashboard/dashboard.page').then(m => m.DashboardPage)
  },
  {
    path: 'inventory',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/records/records.page').then(m => m.RecordsPage)
  },
  {
    path: 'help',
    canActivate: [authGuard],
    loadComponent: () => import('./pages/help/help.page').then(m => m.HelpPage)
  },
  { path: '**', redirectTo: 'inventory' }
];
```

#### Jerarquía de Roles y Matriz de Control de Acceso:
* **ADMIN:** Acceso irrestricto. Dashboard interactivo con Chart.js, visualización de catálogo, creación de registros, edición, borrado de activos, y exportación oficial a PDF y CSV.
* **SUPERVISOR (Extensible):** Acceso al Dashboard de analítica y gestión operativa del catálogo sin privilegios de eliminación destructiva de datos.
* **STANDARD_USER:** Acceso a inventario operativo, alta de nuevos registros, exportación de informes y manual de ayuda. El acceso a `/dashboard` queda estrictamente denegado por `roleGuard`.

---

### 3.2. Control Visual y Experiencia de Usuario (UI/UX Condicional)

En lugar de permitir que el usuario interactúe con una opción para luego mostrar un mensaje de error ("Acceso Denegado"), el sistema aplica un **control preventivo de interfaz**.

#### 1. Menú Lateral Global (`src/app/app.component.html`):
El enlace al Cuadro de Mando del Administrador se renderiza condicionalmente verificando el rol activo. Si el usuario conectado tiene rol `STANDARD_USER`, la opción ni siquiera existe en el DOM:

```html
<!-- app.component.html -->
@if (user.role === 'ADMIN') {
  <ion-menu-toggle auto-hide="false">
    <ion-item routerDirection="root" [routerLink]="['/dashboard']" routerLinkActive="selected" detail="false">
      <ion-icon aria-hidden="true" slot="start" name="stats-chart-outline"></ion-icon>
      <ion-label>Cuadro de Mando</ion-label>
    </ion-item>
  </ion-menu-toggle>
}
```

#### 2. Componente Reutilizable DataTable (`src/app/pages/records/records.page.html`):
En la vista de inventario, el componente desacoplado `<app-data-table>` recibe la señal de privilegios mediante un `@Input() canDelete`. Para un usuario estándar, el botón de la papelera no se dibuja en las filas:

```html
<!-- records.page.html -->
<app-data-table
  [data]="records"
  [columns]="tableColumns"
  [isLoading]="isLoading"
  [canDelete]="isAdmin"
  (rowSelect)="onSelectRecord($event)"
  (rowDelete)="onDeleteRecord($event)">
</app-data-table>
```

Y en la plantilla del componente (`data-table.component.html`):
```html
<!-- data-table.component.html -->
@if (canDelete) {
  <ion-button 
    fill="clear" 
    size="small" 
    color="danger"
    aria-label="Eliminar registro"
    (click)="onDeleteClick($event, row)">
    <ion-icon name="trash-outline" slot="icon-only"></ion-icon>
  </ion-button>
}
```

---

## 4. Apartado C: Matriz de Alternativas Evaluadas

La selección de la arquitectura actual frente a paradigmas alternativos se fundamenta en el siguiente análisis técnico:

| Dimensión Técnica | Alternativa Evaluada | Solución Implementada (Arquitectura del Proyecto) | Justificación Técnica de la Decisión |
| :--- | :--- | :--- | :--- |
| **Capa de Protección de Rutas** | **Comprobación en Componente:** Validación en hooks `ngOnInit()` o `ionViewWillEnter()`. | **Functional Guards a Nivel de Enrutador:** `canMatch` y `canActivate`. | La resolución en componente causa **renderizado fantasma (*flash of unauthenticated content*)**, ejecuta ciclos de vida innecesarios, descarga el bundle JS por la red y genera fugas de memoria por suscripciones huérfanas antes de la redirección. Los guards en el enrutador interceptan antes de instanciar el componente. |
| **Gestión de Credenciales en Red** | **Inyección Manual:** Añadir cabeceras `HttpHeaders` manualmente en cada método de servicio (`data.service.ts`). | **Pipeline Centralizado:** `HttpInterceptorFn` (`authInterceptor` + `errorInterceptor`). | La inyección manual viola el principio **DRY**, introduce riesgo crítico de omisión humana en nuevos servicios y dispersa la lógica de renovación de sesión. El interceptor asegura cobertura del 100% de llamadas HTTP y desacopla la vista de la autenticación. |
| **Modelo de Autorización** | **Control Booleano Simple (`isAdmin: boolean`):** Flag binario en el objeto de usuario. | **Modelo RBAC Formal con Claims JWT:** Jerarquía de roles (`ADMIN`, `SUPERVISOR`, `STANDARD_USER`) y permisos granulares. | Un flag binario es frágil, carece de granularidad y colapsa cuando el sistema incorpora roles intermedios o de auditoría. RBAC proporciona un modelo escalable sin la sobrecarga computacional de evaluar reglas dinámicas en runtime como exigiría ABAC. |
| **Modelo de Autorización (Comparativa)** | **ABAC (Attribute-Based Access Control):** Evaluación en runtime por contexto (IP, horario, departamento). | **Modelo RBAC Formal:** Roles mapeados a matrices estáticas de permisos. | ABAC impone una complejidad arquitectónica y consumo de CPU desproporcionado para clientes móviles. RBAC ofrece complejidad algorítmica $O(1)$ en consultas locales de interfaz mediante Signals computadas. |
