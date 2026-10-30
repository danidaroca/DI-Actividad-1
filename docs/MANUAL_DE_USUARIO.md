# Manual de Usuario y Guía de Operación
## Sistema de Gestión Empresarial Multiplataforma (Ionic 9 + Angular 22 Standalone)

**Módulo Profesional:** Desarrollo de Interfaces (Código: 0488)  
**Ciclo Formativo:** Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM 2)  
**Autor:** Daniel Daroca  
**Repositorio GitHub:** [https://github.com/danidaroca/DI-Actividad-1](https://github.com/danidaroca/DI-Actividad-1)  
**Despliegue Oficial en Producción:** [https://di-actividad-1.vercel.app](https://di-actividad-1.vercel.app)  

---

## 1. Introducción y Descripción del Sistema

El **Sistema de Gestión Empresarial Multiplataforma** es una Progressive Web App (PWA) de alto rendimiento diseñada con un enfoque **Mobile-First**, construida sobre el framework **Ionic 9** y **Angular 22** utilizando una arquitectura moderna basada exclusivamente en **Standalone Components**, **Angular Signals** y orquestación reactiva con **RxJS**.

La aplicación proporciona un entorno integral para la monitorización de indicadores clave (KPIs), visualización gráfica de métricas de stock y facturación, administración de catálogo de inventario con validaciones asíncronas en tiempo real, control de acceso basado en roles (RBAC) y generación automatizada de informes oficiales en formatos PDF y CSV.

---

## 2. Acceso al Sistema y Gestión de Sesión

### 2.1. Pantalla de Inicio de Sesión (`/login`)
Para acceder a la plataforma, el usuario debe autenticarse introduciendo sus credenciales o utilizando los **botones de acceso rápido de un clic** diseñados específicamente para facilitar la evaluación y auditoría docente:

| Botón de Prueba | Correo Electrónico | Contraseña | Rol Asignado | Alcance y Permisos |
| :--- | :--- | :--- | :--- | :--- |
| **Acceso Rápido Administrador** | `admin@empresa.com` | `Admin123!` | `ADMIN` | Acceso irrestricto: Cuadro de Mando con Chart.js, Gestión de Catálogo, Altas, Edición, Borrado destructivo y Exportación de Informes. |
| **Acceso Rápido Estándar** | `user@empresa.com` | `User123!` | `STANDARD_USER` | Acceso operativo: Catálogo de Inventario, Alta de nuevos productos, Exportación de informes y Manual de Ayuda. *(Ruta `/dashboard` bloqueada por `roleGuard`)*. |

### 2.2. Registro de Nuevos Usuarios (`/register`)
Si el usuario no dispone de cuenta, puede registrarse desde el enlace habilitado en el login:
* **Validación Asíncrona de Email:** Al introducir el correo electrónico, el formulario interactúa de forma asíncrona contra el backend simulado (`AsyncValidatorService`).
  * **Estado PENDING:** Se activa un indicador de carga (`ion-spinner`) con el texto *"Comprobando disponibilidad del correo en el servidor..."*.
  * **Estado INVALID:** Si el correo ya existe en el sistema (ej. `admin@empresa.com`), se despliega una alerta semántica roja impidiendo el registro.
  * **Estado VALID:** Si el correo está libre, se muestra una confirmación visual verde y se habilita el botón de envío.

---

## 3. Cuadro de Mando y Analítica (`/dashboard`)
*Exclusivo para usuarios con rol `ADMIN`. Si un usuario estándar intenta navegar directamente a esta URL, el `roleGuard` intercepta la petición y redirige a `/inventory`.*

### 3.1. Indicadores Clave de Rendimiento (KPIs)
En la parte superior se renderizan tarjetas de métricas mediante el componente reutilizable `<app-stat-card>`:
* **Total de Artículos en Catálogo:** Suma agregada de registros en inventario.
* **Valoración Económica Total:** Importe total en euros (€) calculado en tiempo real.
* **Alertas de Stock Crítico:** Identificación de productos con existencias bajo mínimos.
* **Categorías Activas:** Total de sectores de catálogo gestionados.

### 3.2. Gráficos Interactivos con Chart.js
El cuadro de mando integra dos visualizaciones gráficas avanzadas:
1. **Gráfico de Barras por Categoría:** Desglose comparativo entre Tecnología, Mobiliario, Oficina, etc.
2. **Gráfico Doughnut de Cuota Porcentual:** Distribución proporcional de recursos.
3. **Selector Dinámico de Métrica:** Un conmutador interactivo permite alternar en tiempo real entre:
   * **Unidades en Stock:** Volumen físico de existencias.
   * **Valoración Económica (€):** Impacto monetario de los activos.

---

## 4. Gestión de Catálogo e Inventario (`/inventory`)
Accesible para todos los usuarios autenticados (`ADMIN` y `STANDARD_USER`).

### 4.1. Tabla Avanzada de Datos (`<app-data-table>`)
Construida con **Angular Signals** para un rendimiento ultrarrápido sin recargas:
* **Búsqueda Reactiva en Tiempo Real:** Filtra instantáneamente por código de producto, nombre o categoría a medida que se escribe.
* **Filtro por Categorías:** Selector desplegable para acotar los resultados.
* **Paginación Dinámica:** Controles de avance, retroceso y selector de elementos por página (5, 10, 20).
* **Navegación Accesible por Teclado:** Soporte completo de accesibilidad WCAG 2.1 AA (foco con `Tab`, selección con `Enter` o barra espaciadora).

### 4.2. Alta de Nuevos Registros (Formulario Modal)
Pulsando en el botón **"Nuevo Registro"**, se abre un diálogo modal reactivo:
* **Código de Artículo:** Validación de patrón (`PROD-XXX`) y comprobación asíncrona de disponibilidad para evitar códigos duplicados en el catálogo.
* **Nombre / Descripción:** Mínimo 4 caracteres requeridos.
* **Categoría, Stock y Precio:** Controles numéricos validados con restricciones semánticas.

### 4.3. Acciones por Fila y Control Condicional de Permisos (RBAC)
* **Ver / Seleccionar:** Notificación emergente Toast con el detalle del producto.
* **Editar:** Habilitado para Administradores y Supervisores.
* **Eliminar Registro:** Gracias al control visual en plantilla `[canDelete]="isAdmin"`, el botón de borrado (icono de papelera en color rojo) **únicamente es visible y ejecutable para el Administrador**, previniendo eliminaciones accidentales por parte de usuarios estándar.

---

## 5. Exportación de Informes y Datos

Desde la barra superior de acciones o desde la cabecera de la tabla de inventario, se dispone de dos opciones de descarga inmediata:

### 5.1. Exportación a PDF Oficial Maquetado
* Desarrollada con las librerías `jsPDF` y `jspdf-autotable`.
* **Formato:** Orientación horizontal (*Landscape*) adaptada para visualización clara de datos tabulares.
* **Estructura del Informe:**
  * Membrete corporativo superior con fecha y hora exacta de emisión.
  * Bloque de tarjetas KPI con resumen consolidado (Total de activos, Valoración en €, Alertas de stock).
  * Tabla de inventario estilizada con bandas grises alternas, cabeceras en azul corporativo y celdas de estado coloreadas semánticamente (Verde: Disponible, Amarillo: Bajo Stock, Rojo: Agotado).
  * Pie de página institucional con numeración de página automática (*Página X de Y*).

### 5.2. Exportación a CSV Normalizado
* Genera un fichero `.csv` estructurado con cabeceras estándar y delimitador por punto y coma (`;`).
* **Codificación UTF-8 con BOM (Byte Order Mark):** Garantiza que caracteres especiales, tildes y símbolos de moneda (`€`) se abran correctamente en **Microsoft Excel** sin deformaciones de texto.

---

## 6. Menú Lateral Global y Opciones de Sesión

El menú lateral desplegable (`ion-menu`) proporciona navegación fluida y contextual:
* **Perfil de Usuario Conectado:** Tarjeta superior con avatar, nombre, correo y un badge distintivo del rol (`ADMINISTRADOR` en color rojo o `USUARIO ESTÁNDAR` en color azul).
* **Enlaces Dinámicos:** La opción *"Cuadro de Mando"* se oculta automáticamente para usuarios sin privilegios administrativos.
* **Manual y Ayuda (`/help`):** Vista interactiva integrada con acordeones que explica el funcionamiento paso a paso.
* **Cerrar Sesión:** Limpia el token y datos de sesión de `localStorage` y redirige al `/login`.

---

## 7. Preguntas Frecuentes y Soporte Técnico

* **¿Por qué no puedo acceder al Cuadro de Mando con `user@empresa.com`?**  
  Por diseño de seguridad (RBAC). El Cuadro de Mando está restringido por `roleGuard` exclusivamente al perfil de Administrador. Para explorarlo, inicia sesión con `admin@empresa.com`.
* **¿Qué ocurre si expira la sesión?**  
  El interceptor de red funcional (`errorInterceptor`) detectará el error HTTP 401 y redirigirá de forma segura al usuario a la pantalla de login, recordando la URL a la que intentaba acceder (`returnUrl`).
* **¿Es compatible con dispositivos móviles?**  
  Sí, la aplicación está diseñada con enfoque Mobile-First y cuenta con diseño responsivo completo, adaptando menús, tablas y modales al tamaño exacto de la pantalla.
