# 📚 Guía de Estudio Rápido para Examen: Desarrollo de Interfaces (0488)
## Resumen Teórico y Preguntas Cortas del Proyecto (Ionic 9 + Angular 22 Standalone)

**Módulo Profesional:** Desarrollo de Interfaces (Código: 0488)  
**Ciclo Formativo:** Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM 2)  
**Proyecto de Referencia:** Sistema de Gestión Multiplataforma con Ionic 9, Angular 22 y Chart.js  
**Repositorio GitHub:** [https://github.com/danidaroca/DI-Actividad-1](https://github.com/danidaroca/DI-Actividad-1)  
**Despliegue Vercel:** [https://di-actividad-1.vercel.app](https://di-actividad-1.vercel.app)  

---

# PARTE 1: CONCEPTOS TEÓRICOS FUNDAMENTALES (Lo que te pueden preguntar)

---

### 1. ARQUITECTURA ANGULAR MODERNA (STANDALONE COMPONENTS)
* **¿Qué es un Standalone Component?**  
  Un componente independiente que no requiere ser declarado en un `NgModule`. Se define con `standalone: true` en su decorador `@Component` e importa sus propias dependencias directamente en la propiedad `imports: [...]`.
* **Ventajas clave:**
  * Eliminación del boilerplate de los módulos (`AppModule`).
  * Facilita el **Tree-Shaking** (el compilador elimina código no utilizado de forma más eficiente).
  * Simplifica la carga perezosa (*Lazy Loading*) a nivel de ruta directa con `loadComponent: () => import(...)`.
* **Arranque de la aplicación:** Se realiza mediante `bootstrapApplication(AppComponent, { providers: [...] })` en `main.ts`.

---

### 2. ENRUTAMIENTO, GUARDS FUNCIONALES Y RENDIMIENTO
* **Functional Guards:**  
  A partir de Angular 15+, los guards ya no son clases con `implements CanActivate`, sino **funciones puras tipadas** (`CanActivateFn`, `CanMatchFn`, `CanDeactivateFn`) que utilizan la función `inject()` para resolver dependencias.
* **DIFERENCIA CLAVE DE EXAMEN: `canMatch` vs `canActivate`**:
  * **`CanMatchFn` (Fase de emparejamiento):** Se ejecuta **antes** de que el enrutador intente descargar el bundle JavaScript del componente lazy (`loadComponent`). Si devuelve `false`, **el chunk JS jamás se descarga por red**. Esto ahorra ancho de banda en dispositivos móviles y evita la filtración de código cliente (*Zero-Leakage*).
  * **`CanActivateFn` (Fase de activación):** Se ejecuta **después** de haber descargado el chunk JS en memoria. Determina si el componente puede inicializarse. Si devuelve `false`, aborta y redirige (ej. a `/login` guardando la ruta en `queryParams: { returnUrl: state.url }`).
* **Redirección contextual (`returnUrl`):**  
  Técnica donde el guard guarda la URL que el usuario intentó visitar (`state.url`). Tras autenticarse con éxito, el sistema navega a esa URL en lugar de a una página por defecto, mejorando la experiencia de usuario (UX).

---

### 3. INTERCEPTORES HTTP FUNCIONALES (`HttpInterceptorFn`)
* **¿Qué es un `HttpInterceptorFn`?**  
  Una función de middleware en la cadena de inyección de peticiones HTTP (patrón *Chain of Responsibility*). Intercepta peticiones salientes (`req`) y respuestas entrantes (`next(req)`).
* **Registro global:** Se configuran en `main.ts` dentro de `provideHttpClient(withInterceptors([authInterceptor, errorInterceptor]))`.
* **Inmutabilidad y clonación:**  
  Las peticiones HTTP son inmutables. Para añadir una cabecera de autenticación no se puede modificar `req`, sino que se debe clonar:
  ```typescript
  const cloned = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  ```
* **Manejo centralizado de errores de seguridad:**
  * **HTTP 401 (Unauthorized):** Token ausente, corrupto o expirado. El interceptor captura el error con `catchError`, invalida la sesión local y redirige al usuario a `/login` con `returnUrl`. Si se dispone de backend con rotación, ejecuta el flujo reactivo de *Silent Refresh Token*.
  * **HTTP 403 (Forbidden):** El usuario está autenticado válidamente, pero su rol carece de privilegios para esa operación (violación de RBAC). Redirige a ruta operativa segura (`/inventory`) sin destruir la sesión.

---

### 4. SEGURIDAD Y CONTROL DE ACCESO (RBAC vs ABAC vs FLAG BOOLEANO)
* **Autenticación vs Autorización:**
  * **Autenticación (AuthN):** "¿Quién eres?". Verifica la identidad del usuario (credenciales, firma del JWT).
  * **Autorización (AuthZ):** "¿Qué puedes hacer?". Verifica los permisos de acceso a vistas y operaciones según el rol.
* **Modelo RBAC (Role-Based Access Control):**  
  Asigna usuarios a roles y roles a conjuntos de permisos:  
  $$\text{Usuario} \longrightarrow \text{Rol (ADMIN, SUPERVISOR, USER)} \longrightarrow \text{Permisos (create, read, delete)}$$
* **Comparativa de alternativas:**
  * **Frente a flag booleano (`isAdmin: boolean`):** El flag es frágil, no escala cuando surgen nuevos perfiles (ej. Auditor o Supervisor) y obliga a modificar el modelo de datos.
  * **Frente a ABAC (Attribute-Based Access Control):** ABAC evalúa reglas complejas por contexto en runtime (IP, horario, geolocalización), lo cual introduce sobrecarga computacional innecesaria en clientes móviles. RBAC ofrece complejidad $O(1)$ en consultas locales de interfaz.
* **Claims del Token JWT:** Propiedades codificadas en el payload del token (`sub`, `email`, `role`, `permissions`, `exp`, `iat`).
* **Control Visual Condicional (UI/UX Preventivo):**  
  Ocultar elementos en la interfaz **antes** de que el usuario interactúe:
  * En menú lateral: `@if (user.role === 'ADMIN')` para ocultar el enlace al Cuadro de Mando.
  * En tabla de datos: `[canDelete]="isAdmin"` para no renderizar el botón rojo de papelera a usuarios estándar.

---

### 5. FORMULARIOS REACTIVOS Y VALIDACIÓN ASÍNCRONA
* **¿Qué es un Validador Asíncrono (`AsyncValidatorFn`)?**  
  Una función validadora que no puede determinar de forma inmediata si un valor es válido porque debe realizar una operación asíncrona (como consultar a un backend si un email o código de producto ya existen). Devuelve un `Observable<ValidationErrors | null>`.
* **Estados del Control en Angular (`AbstractControl.status`):**
  1. **`PENDING`:** La validación asíncrona está en curso. La interfaz debe mostrar un indicador visual de espera (`ion-spinner`).
  2. **`INVALID`:** La validación falló (ej. `{ emailTaken: true }`). La interfaz muestra un mensaje de error y deshabilita el botón de envío.
  3. **`VALID`:** La validación tuvo éxito (`null`). Se muestra un indicador de confirmación (check verde) y se habilita el envío.
* **Sintaxis de definición:**  
  En `fb.group({ email: [valorInicial, [validadoresSincronos], [validadoresAsincronos]] })`.

---

### 6. COMPONENTES DESACOPLADOS Y REACTIVIDAD
* **Componentes Dumb / Presentacionales:**  
  Componentes reutilizables sin lógica de negocio propia (como `<app-stat-card>` o `<app-data-table>`).
  * Reciben datos mediante **`@Input()`**.
  * Comunican acciones hacia el padre mediante **`@Output() evento = new EventEmitter<T>()`**.
* **Estrategia `ChangeDetectionStrategy.OnPush`:**  
  Indica a Angular que solo debe ejecutar la detección de cambios en ese componente si cambia la referencia de un `@Input()` o si se dispara un evento originado en el propio componente. Reduce drásticamente los ciclos de repintado del DOM.
* **Angular Signals:**  
  Nuevo primitivo reactivo de Angular. Almacena un valor (`signal(val)`) y notifica de manera granular $O(1)$ a las vistas que lo consumen. `computed(() => ...)` crea valores derivados automáticos (ej. `isAdminSignal = computed(() => this.user()?.role === 'ADMIN')`).

---

### 7. PROGRAMACIÓN REACTIVA CON RxJS
* **`BehaviorSubject`:**  
  Tipo especial de `Subject` que requiere un valor inicial, almacena el último valor emitido y se lo entrega de forma inmediata a cualquier nuevo suscriptor en cuanto se suscribe (`.subscribe()`). Ideal para gestionar el estado de sesión del usuario y listados en tiempo real.
* **Operador `forkJoin`:**  
  Toma múltiples Observables y espera a que **todos ellos completen**. En ese momento emite un único array/objeto con el último valor emitido por cada uno (equivalente al `Promise.all` de JavaScript). Se usa en el Dashboard para solicitar concurrentemente métricas, inventario y alertas con un único spinner de carga.
* **Operadores de utilidad:** `delay` (simula latencia de red), `tap` (efectos secundarios sin alterar el flujo, ej. guardar en `localStorage`), `catchError` (captura excepciones en el flujo).

---

### 8. VISUALIZACIÓN DE DATOS (CHART.JS) Y FUGAS DE MEMORIA
* **Integración en Angular:** Se asocia a un elemento `<canvas #miCanvas>` del DOM mediante `ViewChild` y se instancia en el hook `ngAfterViewInit()`.
* **PREGUNTA CLAVE DE EXAMEN: Prevención de Fugas de Memoria (*Memory Leaks*):**  
  Las instancias de Chart.js mantienen referencias activas al contexto 2D del Canvas y listeners de eventos en la ventana (resize, tooltip, hover). Es **obligatorio invocar explícitamente `chart.destroy()` en el hook de ciclo de vida `ngOnDestroy()`**. Si no se hace, cada vez que el usuario entra y sale de la vista se acumulan instancias en memoria consumiendo RAM hasta colapsar la app.

---

### 9. EXPORTACIÓN DE INFORMES (PDF Y CSV)
* **Exportación a PDF con `jsPDF` y `jspdf-autotable`:**  
  Generación en el lado cliente (*Client-Side Rendering*). Para datos tabulares anchos se configura en orientación horizontal (`orientation: 'landscape'`). Permite añadir membrete corporativo, bloques resumen de métricas y paginación dinámica (*Página X de Y*).
* **Exportación a CSV con UTF-8 BOM:**  
  Se construye una cadena de texto delimitada por punto y coma (`;`). Para garantizar que **Microsoft Excel** abra el fichero reconociendo tildes y caracteres especiales (como el símbolo `€`), se debe anteponer la marca **BOM (Byte Order Mark: `\uFEFF`)** al crear el `Blob` de datos (`new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })`).

---

### 10. CICLO DE VIDA DE SOFTWARE: GIT FLOW, COMPODOC Y CI/CD
* **Git Flow:**  
  Metodología estricta de ramas: `main` (producción/entregas estables), `develop` (desarrollo e integración continua) y ramas de características `feature/<nombre>` que se fusionan con la opción `--no-ff` (*No Fast-Forward*) para forzar la creación de un commit de fusión y preservar el árbol histórico.
* **Compodoc:**  
  Herramienta de documentación estática para aplicaciones Angular. Lee los comentarios JSDoc y las firmas TypeScript y genera un portal interactivo con diagramas de dependencias, árbol de rutas y catálogo de componentes.
* **Despliegue SPA en Vercel (`vercel.json`):**  
  En una Single Page Application (SPA), el enrutamiento lo gestiona el cliente (JavaScript en el navegador). Si un usuario recarga directamente la URL `/dashboard`, el servidor web físico buscará un archivo `dashboard.html` y devolverá error 404. La regla de reescritura en `vercel.json`:
  ```json
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
  ```
  fuerza al servidor a servir siempre `index.html` para que el enrutador de Angular tome el control de la ruta solicitada.

---

# PARTE 2: SIMULACRO DE EXAMEN (10 PREGUNTAS CORTAS RESUELTAS)

A continuación tienes 10 preguntas con la **respuesta modelo perfecta** redactada con los términos técnicos exactos que busca el corrector:

---

#### ❓ Pregunta 1:
**¿Cuál es la diferencia fundamental entre proteger una ruta mediante `CanMatchFn` y hacerlo mediante `CanActivateFn` en Angular?**
> **Respuesta Modelo:**  
> La diferencia reside en la fase del ciclo de enrutamiento en que operan y en el impacto sobre la descarga del código (*Lazy Loading*).  
> `CanMatchFn` se evalúa **antes** de cargar el componente perezoso (`loadComponent`); si retorna `false`, **el navegador no descarga el bundle JavaScript por la red**, ahorrando ancho de banda y evitando exponer código confidencial a usuarios no autorizados (*Zero-Leakage*). En cambio, `CanActivateFn` se evalúa **después** de haber descargado el chunk en memoria para decidir si el componente se inicializa en el DOM, utilizándose típicamente para comprobación de sesión y redirección contextual con `returnUrl`.

---

#### ❓ Pregunta 2:
**¿Por qué las peticiones HTTP en un `HttpInterceptorFn` deben clonarse y no modificarse directamente?**
> **Respuesta Modelo:**  
> Porque las instancias de `HttpRequest` en Angular son **inmutables por diseño**. Esto asegura que las peticiones sean deterministas y seguras frente a reintentos concurrentes o respuestas cacheadas. Para propagar cabeceras como `Authorization: Bearer <token>`, el interceptor debe generar una nueva instancia inmutable invocando el método `req.clone({ setHeaders: { ... } })`.

---

#### ❓ Pregunta 3:
**¿Qué estrategia de manejo centralizado de errores debe implementar un interceptor de red ante respuestas HTTP 401 y HTTP 403?**
> **Respuesta Modelo:**  
> Mediante el operador reactivo `catchError`:
> * Ante un **HTTP 401 (Unauthorized):** El interceptor asume expiración o ausencia de sesión; limpia el token del almacenamiento local (`localStorage`), revoca el estado y redirige al usuario a `/login` guardando la ruta actual como `returnUrl`. (Opcionalmente dispara un flujo de *Refresh Token* si el backend lo soporta).
> * Ante un **HTTP 403 (Forbidden):** El interceptor reconoce que la sesión es válida pero el rol carece de privilegios (violación de RBAC); redirige a una ruta operativa segura (ej. `/inventory`) mostrando una notificación de acceso denegado sin cerrar la sesión del usuario.

---

#### ❓ Pregunta 4:
**En el modelo de seguridad RBAC, ¿cuál es la diferencia técnica entre Autenticación y Autorización?**
> **Respuesta Modelo:**  
> * La **Autenticación (AuthN)** responde a "¿Quién es el usuario?". Es el proceso de verificar la identidad declarada mediante credenciales (login) o la firma digital y vigencia temporal de un token JWT.
> * La **Autorización (AuthZ)** responde a "¿Qué tiene permitido hacer ese usuario?". Evalúa los privilegios o permisos asignados al rol del usuario autenticado (extraídos de los *claims* del token) para decidir si puede acceder a una vista (ej. `/dashboard`) o ejecutar una acción (ej. eliminar un registro).

---

#### ❓ Pregunta 5:
**¿Cuáles son los tres estados que atraviesa un formulario reactivo durante la validación asíncrona y qué debe mostrar la interfaz en cada uno?**
> **Respuesta Modelo:**  
> 1. **`PENDING`:** La validación está consultando al servidor/backend. La interfaz debe deshabilitar el botón de envío y mostrar un indicador visual de carga (como un `ion-spinner`).
> 2. **`INVALID`:** La validación asíncrona resolvió un error (ej. `{ emailTaken: true }`). La interfaz muestra un aviso semántico de error en color rojo y mantiene bloqueado el envío.
> 3. **`VALID`:** La validación asíncrona resolvió `null` (disponible). La interfaz muestra un indicador positivo (check verde) y habilita el botón para enviar el formulario.

---

#### ❓ Pregunta 6:
**¿Qué problema crítico de rendimiento provoca no destruir una instancia de Chart.js en Angular y en qué hook de ciclo de vida debe resolverse?**
> **Respuesta Modelo:**  
> Provoca una **fuga de memoria (*Memory Leak*)**, ya que Chart.js retiene referencias internas al contexto 2D del elemento `<canvas>` y suscriptores a eventos globales de la ventana (`window.resize`, animaciones y eventos de puntero).  
> Debe resolverse de forma obligatoria en el hook **`ngOnDestroy()`** invocando explícitamente el método **`chartInstance.destroy()`**.

---

#### ❓ Pregunta 7:
**¿Para qué se utiliza el operador `forkJoin` de RxJS en la capa de servicios del Dashboard?**
> **Respuesta Modelo:**  
> Se utiliza para **orquestar peticiones asíncronas concurrentes**. `forkJoin` recibe múltiples Observables (en nuestro caso: métricas globales, catálogo SQL y notificaciones NoSQL), ejecuta las peticiones en paralelo y espera a que todas completen para emitir un único valor conjunto. Esto permite presentar un único spinner de carga global en la interfaz y renderizar todo el Cuadro de Mando en un solo ciclo atómico.

---

#### ❓ Pregunta 8:
**¿Por qué se debe incluir la marca BOM (`\uFEFF`) al generar un archivo CSV para su descarga?**
> **Respuesta Modelo:**  
> El **Byte Order Mark (BOM)** en codificación UTF-8 indica explícitamente a aplicaciones cliente como **Microsoft Excel** que el flujo de bytes entrante está codificado en UTF-8. Sin esta marca inicial (`\uFEFF`), Excel asume por defecto la codificación ANSI o Windows-1252, provocando que caracteres como tildes, la letra 'ñ' y el símbolo del euro (€) se visualicen corruptos (*mojibake*).

---

#### ❓ Pregunta 9:
**¿Qué función cumple la opción `--no-ff` al realizar fusiones de ramas en la metodología Git Flow?**
> **Respuesta Modelo:**  
> `--no-ff` (*No Fast-Forward*) fuerza a Git a **crear siempre un commit de fusión dedicado (*merge commit*)**, incluso cuando la rama destino podría simplemente avanzar el puntero de manera lineal. Esto garantiza la trazabilidad histórica, documentando explícitamente cuándo se integró una característica (`feature`) en la rama de desarrollo (`develop`) o de producción (`main`).

---

#### ❓ Pregunta 10:
**¿Por qué es imprescindible configurar reglas de reescritura (*rewrites*) en `vercel.json` para desplegar una aplicación Angular SPA?**
> **Respuesta Modelo:**  
> Porque en una **Single Page Application (SPA)** no existen archivos HTML físicos para cada ruta (no existe un `dashboard.html` en el servidor). Todo el enrutamiento se simula en el cliente mediante la API de History del navegador.  
> La regla de reescritura redirige internamente cualquier petición que no sea un archivo estático hacia `/index.html`. De este modo, si el usuario recarga la página en `/dashboard`, el servidor devuelve `index.html` en lugar de un error HTTP 404, permitiendo que el enrutador de Angular arranque y active el componente correspondiente.
