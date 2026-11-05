import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\TEORIA_EXAMEN_DESARROLLO_INTERFACES.pdf"
DOCS_PDF_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\docs\TEORIA_EXAMEN_DESARROLLO_INTERFACES.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header (from page 1 onwards or page 2 onwards)
        if self._pageNumber > 1:
            self.drawString(42, 804, "TEORÍA Y APUNTES DE EXAMEN | DESARROLLO DE INTERFACES (CÓDIGO 0488) - DAM 2")
            self.drawRightString(553, 804, "VERSIÓN OFICIAL PARA IMPRESIÓN")
            self.setStrokeColor(colors.HexColor("#94A3B8"))
            self.setLineWidth(0.5)
            self.line(42, 796, 553, 796)

        # Running Footer
        self.line(42, 38, 553, 38)
        self.drawString(42, 26, "Daniel Daroca - Proyecto de Gestión Multiplataforma (Ionic 9 + Angular 22) | Repositorio: github.com/danidaroca/DI-Actividad-1")
        page_text = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(553, 26, page_text)

        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Printer-friendly color palette (high contrast, crisp text, ink efficient)
    c_primary = colors.HexColor("#0F172A")    # Almost black / deep slate for crisp print
    c_blue = colors.HexColor("#1E3A8A")       # Dark corporate navy
    c_accent = colors.HexColor("#2563EB")     # Bright accent blue
    c_text = colors.HexColor("#0F172A")       # Maximum contrast body text
    c_border = colors.HexColor("#CBD5E1")     # Light clean borders
    c_box_bg = colors.HexColor("#F8FAFC")     # Ultra light slate background
    c_highlight = colors.HexColor("#EFF6FF")  # Very pale blue tint for key definitions

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14.5,
        leading=17.5,
        textColor=c_blue,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=12.5,
        textColor=c_blue,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_accent,
        spaceBefore=3,
        spaceAfter=1.5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.2,
        textColor=c_text,
        spaceAfter=2.5
    )

    bold_body_style = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=10.2,
        textColor=c_blue,
        spaceAfter=2
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.6,
        textColor=colors.HexColor("#0F172A")
    )

    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#1E3A8A")
    )

    ans_style = ParagraphStyle(
        'AnsText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=c_text
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=c_text
    )

    story = []

    # ================= PAGE 1: ARQUITECTURA Y ENRUTAMIENTO =================
    header_box = [
        [Paragraph("<b>TEMARIO OFICIAL DE EXAMEN - DESARROLLO DE INTERFACES (CÓDIGO 0488) | DAM 2</b>", ParagraphStyle('HBox', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#1E3A8A"), alignment=1))]
    ]
    t_header = Table(header_box, colWidths=[519])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 3))

    story.append(Paragraph("Teoría de Examen y Preguntas Cortas (Versión Imprimible)", title_style))
    story.append(Paragraph("<b>Conceptos Clave de Calificación, Arquitectura Técnica y Simulacro de Examen Resuelto</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=4, spaceBefore=1))

    meta_info = [
        [Paragraph("<b>Módulo Profesional:</b>", table_cell_style), Paragraph("Desarrollo de Interfaces (0488)", table_cell_style),
         Paragraph("<b>Ciclo Formativo:</b>", table_cell_style), Paragraph("DAM 2 (Grado Superior)", table_cell_style)],
        [Paragraph("<b>Alumno / Autor:</b>", table_cell_style), Paragraph("Daniel Daroca", table_cell_style),
         Paragraph("<b>Repositorio / Despliegue:</b>", table_cell_style), Paragraph("github.com/danidaroca/DI-Actividad-1 | di-actividad-1.vercel.app", table_cell_style)]
    ]
    t_meta = Table(meta_info, colWidths=[95, 175, 105, 144])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_box_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 3))

    story.append(Paragraph("TEMA 1: Arquitectura Angular Standalone e Ionic Framework", h1_style))
    story.append(Paragraph(
        "• <b>Definición de Standalone Component:</b> Componente independiente que no pertenece a ningún <code>NgModule</code>. Se declara con <code>standalone: true</code> en su decorador <code>@Component</code> e importa explícitamente sus propias dependencias en la propiedad <code>imports: [...]</code>.<br/>"
        "• <b>Ventajas Técnicas Fundamentales:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <b>Eliminación de Boilerplate:</b> Se prescinde de <code>AppModule</code> y módulos intermediarios complejos.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <b>Tree-Shaking Optimizado:</b> El compilador detecta y elimina código no invocado de manera mucho más granular.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. <b>Carga Perezosa Directa (Lazy Loading):</b> Permite enrutar hacia el componente directamente con <code>loadComponent: () => import(...)</code>.<br/>"
        "• <b>Punto de Entrada:</b> El arranque se ejecuta en <code>main.ts</code> mediante <code>bootstrapApplication(AppComponent, { providers: [...] })</code>.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("TEMA 2: Sistema de Enrutamiento y Functional Guards", h1_style))
    story.append(Paragraph(
        "A partir de Angular 15+, los guards basados en clases con <code>implements CanActivate</code> se consideran obsoletos. Se emplean <b>Functional Guards</b> tipados (funciones puras) que resuelven servicios con <code>inject()</code>.",
        body_style
    ))

    # Box highlight canMatch vs canActivate
    guard_compare = [
        [Paragraph("<b>DIFERENCIA TÉCNICA CLAVE DE EXAMEN: CanMatchFn vs CanActivateFn</b>", ParagraphStyle('GH', fontName='Helvetica-Bold', fontSize=7.5, textColor=c_blue))],
        [Paragraph(
            "• <b><code>CanMatchFn</code> (Fase de Emparejamiento):</b> Se evalúa <u>antes</u> de que el enrutador intente resolver el componente perezoso. Si devuelve <code>false</code>, <b>el navegador NUNCA descarga el bundle JavaScript por la red</b>. Esto logra <b>Zero-Leakage</b> (evita que usuarios no autorizados descarguen código confidencial) y ahorra datos móviles.<br/>"
            "• <b><code>CanActivateFn</code> (Fase de Activación):</b> Se ejecuta <u>después</u> de que el bundle ya ha sido descargado en memoria. Comprueba si el componente se puede instanciar en el DOM; se utiliza para validar sesión y ejecutar la <b>redirección contextual</b> guardando la URL intentada (<code>queryParams: { returnUrl: state.url }</code>).",
            body_style
        )]
    ]
    t_guards = Table(guard_compare, colWidths=[519])
    t_guards.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_highlight),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_guards)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "• <b>Ciclo de Vida de Navegación:</b> <code>canMatch</code> (descarta ruta y bloquea descarga de chunk) &rarr; Descarga perezosa (<code>loadComponent</code>) &rarr; <code>canActivate</code> (valida permisos de sesión en memoria) &rarr; Inicialización del Componente &rarr; <code>canDeactivate</code> (previene abandono con datos sin guardar).",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 2: INTERCEPTORES Y SEGURIDAD RBAC =================
    story.append(Paragraph("TEMA 3: HTTP Interceptors Funcionales (HttpInterceptorFn)", h1_style))
    story.append(Paragraph(
        "• <b>Concepto y Registro Global:</b> Middleware basado en el patrón <i>Chain of Responsibility</i> configurado en <code>main.ts</code> mediante <code>provideHttpClient(withInterceptors([authInterceptor, errorInterceptor]))</code>.<br/>"
        "• <b>Inmutabilidad Obligatoria:</b> Las instancias de <code>HttpRequest</code> son inmutables por diseño para garantizar determinismo en reintentos y cachés. Para inyectar cabeceras es imprescindible clonar la petición: <code>const clon = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });</code>.<br/>"
        "• <b>Manejo Centralizado de Errores de Seguridad (RxJS <code>catchError</code>):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>HTTP 401 (Unauthorized):</b> Token inválido o expirado. Limpia <code>localStorage</code> y redirige al usuario a <code>/login?returnUrl=...</code> (o dispara el flujo de <i>Silent Refresh Token</i> si el backend lo soporta).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>HTTP 403 (Forbidden):</b> Sesión válida pero carece de permisos de rol (violación de RBAC). Redirige a ruta segura (<code>/inventory</code>) mostrando aviso sin destruir la sesión.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("TEMA 4: Control de Acceso Basado en Roles (RBAC) y Seguridad", h1_style))
    story.append(Paragraph(
        "• <b>Autenticación (AuthN) frente a Autorización (AuthZ):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <i>Autenticación:</i> Responde a '¿Quién eres?'. Verifica la identidad declarada mediante credenciales (login) o la firma digital y expiración de un JWT.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <i>Autorización:</i> Responde a '¿Qué tienes permitido hacer?'. Comprueba los privilegios o permisos asignados al rol en cada vista o endpoint.<br/>"
        "• <b>Modelo RBAC Formal:</b> Mapea $Usuario \\to Rol (ADMIN, SUPERVISOR, USER) \\to Permisos Granulares$. Desacopla permisos de los usuarios concretos.<br/>"
        "• <b>Claims del Token JWT:</b> Datos estructurados en el payload (<code>sub</code>: ID de usuario, <code>email</code>, <code>role</code>, <code>permissions</code>, <code>exp</code>, <code>iat</code>). Se decodifican en <code>AuthService</code> para exponer Signals reactivas.",
        body_style
    ))

    # RBAC Alternatives Comparison Table
    alt_box = [
        [Paragraph("<b>Enfoque de Seguridad</b>", table_header_style), Paragraph("<b>Descripción Técnica</b>", table_header_style), Paragraph("<b>Evaluación / Decisión Arquitectónica</b>", table_header_style)],
        [Paragraph("<b>Flag Booleano Simple</b><br/>(<code>isAdmin: boolean</code>)", table_cell_style),
         Paragraph("Flag binario en el objeto usuario.", table_cell_style),
         Paragraph("<b>Frágil y no escalable:</b> Colapsa al añadir roles intermedios (ej. Supervisor, Auditor) y obliga a alterar el modelo de datos.", table_cell_style)],
        [Paragraph("<b>ABAC (Attribute-Based)</b><br/>(Control por Atributos)", table_cell_style),
         Paragraph("Evalúa reglas dinámicas por contexto en runtime (IP, horario, departamento).", table_cell_style),
         Paragraph("<b>Sobrecarga excesiva:</b> Complejidad computacional desproporcionada para clientes móviles y PWAs.", table_cell_style)],
        [Paragraph("<b>RBAC Formal con Signals</b><br/>(Solución Implementada)", table_cell_style),
         Paragraph("Roles asociados a matrices de permisos estructurados con Angular Signals.", table_cell_style),
         Paragraph("<b>Óptimo para producción:</b> Escalable, claro y resolución instantánea $O(1)$ en consultas locales de interfaz.", table_cell_style)]
    ]
    t_alt = Table(alt_box, colWidths=[105, 160, 254])
    t_alt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_blue),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_box_bg]),
        ('PADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_alt)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "• <b>Control Visual Condicional (UI/UX Preventivo):</b> Ocultar opciones en lugar de bloquear tras el clic:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Menú lateral: <code>@if (user.role === 'ADMIN')</code> para ocultar la opción del Cuadro de Mando.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Tabla de datos: <code>[canDelete]='isAdmin'</code> para no dibujar el botón rojo de borrado a usuarios estándar.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 3: FORMULARIOS, RXJS, SIGNALS Y CHART.JS =================
    story.append(Paragraph("TEMA 5: Formularios Reactivos y Validación Asíncrona", h1_style))
    story.append(Paragraph(
        "• <b>Validador Asíncrono (<code>AsyncValidatorFn</code>):</b> Función que retorna <code>Observable&lt;ValidationErrors | null&gt;</code> para comprobar datos contra el backend con latencia simulada.<br/>"
        "• <b>Los 3 Estados del Control (<code>AbstractControl.status</code>):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <b><code>PENDING</code>:</b> Comprobando en el servidor. La UI bloquea el botón y muestra <code>&lt;ion-spinner&gt;</code>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <b><code>INVALID</code>:</b> Duplicado (ej. <code>{ emailTaken: true }</code>). La UI muestra alerta roja y deshabilita el botón.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. <b><code>VALID</code>:</b> Dato disponible (<code>null</code>). La UI muestra check verde y activa el botón de envío.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("TEMA 6: Programación Reactiva con RxJS y Angular Signals", h1_style))
    story.append(Paragraph(
        "• <b><code>BehaviorSubject</code>:</b> Subject con valor inicial que emite de inmediato su último valor a cualquier suscriptor. Se usa para la sesión de usuario y flujo de datos reactivo.<br/>"
        "• <b><code>forkJoin</code> (Orquestación Concurrente):</b> Recibe múltiples Observables (métricas, catálogo SQL y notificaciones NoSQL), los ejecuta en paralelo y espera a que <b>todos completen</b> para emitir un único resultado agregado (equivalente a <code>Promise.all</code>). Permite usar un único spinner de carga para todo el Dashboard.<br/>"
        "• <b>Angular Signals:</b> Primitivo reactivo que almacena un valor y notifica directamente a la vista sin sobrecarga de Zone.js (<code>signal()</code>, <code>computed()</code>). Complejidad algorítmica $O(1)$.<br/>"
        "• <b>Componentes Desacoplados y <code>ChangeDetectionStrategy.OnPush</code>:</b> Componentes reutilizables que solo reciben <code>@Input()</code> y emiten <code>@Output()</code>. <code>OnPush</code> indica a Angular que solo compruebe cambios si cambian las referencias de los Inputs, ahorrando ciclos de CPU.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("TEMA 7: Visualización con Chart.js y Prevención de Fugas de Memoria", h1_style))
    story.append(Paragraph(
        "• <b>Integración:</b> Se asocia a un elemento <code>&lt;canvas #chartCanvas&gt;</code> en el DOM mediante <code>@ViewChild</code> y se instancia en el hook <code>ngAfterViewInit()</code>.<br/>"
        "• <b>PREGUNTA CRÍTICA: Fugas de Memoria (Memory Leaks):</b> Chart.js mantiene referencias internas al contexto 2D del Canvas y suscriptores a eventos de ventana (<code>resize</code>, tooltips, animaciones). <b>Es obligatorio invocar explícitamente <code>chartInstance.destroy()</code> en el hook <code>ngOnDestroy()</code></b>. De lo contrario, cada navegación acumula instancias en RAM hasta colapsar el navegador.",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("TEMA 8: Exportación de Informes, Git Flow y Despliegue SPA", h1_style))
    story.append(Paragraph(
        "• <b>Exportación a PDF:</b> Generación en cliente con <code>jsPDF</code> y <code>jspdf-autotable</code> en formato horizontal (<i>Landscape</i>) con membrete corporativo, bloques de KPIs y tabla con bandas alternas.<br/>"
        "• <b>Exportación a CSV con UTF-8 BOM:</b> Se antepone la marca <b>BOM (<code>\\uFEFF</code>)</b> al crear el <code>Blob</code> de datos para que <b>Microsoft Excel</b> reconozca tildes, caracteres especiales y el símbolo del euro (€) sin corromper el texto.<br/>"
        "• <b>Metodología Git Flow (Opción <code>--no-ff</code>):</b> <i>No Fast-Forward</i> fuerza a Git a crear siempre un commit de fusión explícito, preservando la trazabilidad del árbol histórico de ramas (<code>main</code>, <code>develop</code>, <code>feature/*</code>).<br/>"
        "• <b>Despliegue SPA en Vercel (<code>vercel.json</code>):</b> En una SPA, el enrutador de Angular opera en el navegador. La regla <code>rewrites: [{\"source\": \"/(.*)\", \"destination\": \"/index.html\"}]</code> fuerza al servidor web a entregar siempre <code>index.html</code> para que al recargar en rutas profundas (ej. <code>/dashboard</code>) no se produzca un error HTTP 404.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 4: SIMULACRO PREGUNTAS 1 A 5 =================
    story.append(Paragraph("PARTE 2: SIMULACRO DE EXAMEN (10 PREGUNTAS CORTAS RESUELTAS)", h1_style))
    story.append(Paragraph("Respuestas modelo oficiales con los términos técnicos y justificaciones que exigen los correctores de DAM:", subtitle_style))
    story.append(Spacer(1, 2))

    def make_print_qa(num, q_text, a_text):
        qa_data = [
            [Paragraph(f"<b>❓ PREGUNTA {num}: {q_text}</b>", q_title_style)],
            [Paragraph(f"<b>Respuesta Modelo:</b> {a_text}", ans_style)]
        ]
        t = Table(qa_data, colWidths=[519])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
            ('BACKGROUND', (0,1), (-1,1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor("#94A3B8")),
            ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 3),
        ]))
        return t

    q1_t = "¿Cuál es la diferencia fundamental entre CanMatchFn y CanActivateFn en Angular?"
    a1_t = "La diferencia radica en la fase de enrutamiento y en el impacto de red sobre el <i>Lazy Loading</i>. <b><code>CanMatchFn</code></b> se evalúa <u>antes</u> de cargar el componente perezoso (<code>loadComponent</code>); si devuelve <code>false</code>, <b>el navegador jamás descarga el chunk JS por la red</b>, garantizando <i>Zero-Leakage</i> y ahorro de ancho de banda móvil. En cambio, <b><code>CanActivateFn</code></b> se ejecuta <u>después</u> de haber descargado el chunk en memoria para comprobar si se inicializa en el DOM, usándose para validación de sesión y redirección contextual con <code>returnUrl</code>."
    story.append(make_print_qa(1, q1_t, a1_t))
    story.append(Spacer(1, 4))

    q2_t = "¿Por qué las peticiones HTTP en un HttpInterceptorFn deben clonarse y no modificarse directamente?"
    a2_t = "Porque las instancias de <code>HttpRequest</code> en Angular son <b>inmutables por diseño</b> para asegurar determinismo frente a reintentos concurrentes y respuestas cacheadas. Para propagar cabeceras de autorización (<code>Authorization: Bearer &lt;token&gt;</code>) es obligatorio invocar el método de clonación inmutable <b><code>req.clone({ setHeaders: { ... } })</code></b>."
    story.append(make_print_qa(2, q2_t, a2_t))
    story.append(Spacer(1, 4))

    q3_t = "¿Qué estrategia de manejo centralizado de errores debe aplicar un interceptor ante códigos HTTP 401 y 403?"
    a3_t = "Mediante <code>catchError</code>: ante un <b>HTTP 401 (Unauthorized)</b> asume sesión expirada, revoca el token local de <code>localStorage</code> y redirige al usuario a <code>/login</code> guardando la ruta actual como <code>returnUrl</code> (o dispara un flujo de <i>Silent Refresh</i>). Ante un <b>HTTP 403 (Forbidden)</b> reconoce identidad válida pero sin permisos de rol suficientes (violación de RBAC); redirige a una ruta operativa segura (ej. <code>/inventory</code>) mostrando una alerta sin cerrar la sesión."
    story.append(make_print_qa(3, q3_t, a3_t))
    story.append(Spacer(1, 4))

    q4_t = "En el modelo de seguridad RBAC, ¿cuál es la diferencia técnica entre Autenticación y Autorización?"
    a4_t = "<b>Autenticación (AuthN):</b> Responde a <i>'¿Quién eres?'</i>. Comprueba criptográficamente la identidad declarada mediante credenciales (login) o la firma y vigencia de un token JWT. <b>Autorización (AuthZ):</b> Responde a <i>'¿Qué tienes permitido hacer?'</i>. Evalúa los privilegios o permisos asignados al rol del usuario autenticado (extraídos de los <i>claims</i> del token) para autorizar accesos a vistas (ej. <code>/dashboard</code>) o acciones operativas (ej. borrar registros)."
    story.append(make_print_qa(4, q4_t, a4_t))
    story.append(Spacer(1, 4))

    q5_t = "¿Cuáles son los tres estados de un formulario reactivo durante la validación asíncrona y qué debe mostrar la UI?"
    a5_t = "1. <b><code>PENDING</code>:</b> Petición en curso contra el servidor. La UI bloquea el botón y muestra un indicador de espera (<code>&lt;ion-spinner&gt;</code>).<br/>2. <b><code>INVALID</code>:</b> Validación fallida (ej. <code>{ emailTaken: true }</code>). La UI despliega alerta roja de error y mantiene deshabilitado el envío.<br/>3. <b><code>VALID</code>:</b> Validación superada con <code>null</code>. La UI muestra confirmación visual (check verde) y habilita el botón de envío."
    story.append(make_print_qa(5, q5_t, a5_t))

    story.append(PageBreak())

    # ================= PAGE 5: SIMULACRO PREGUNTAS 6 A 10 =================
    q6_t = "¿Qué problema crítico de rendimiento provoca no destruir una instancia de Chart.js y cómo se resuelve?"
    a6_t = "Provoca una <b>fuga de memoria (<i>Memory Leak</i>)</b>, ya que Chart.js retiene referencias al contexto 2D del Canvas y suscriptores a eventos globales de la ventana (<code>resize</code>, animaciones y puntero). Debe resolverse obligatoriamente en el hook de ciclo de vida <b><code>ngOnDestroy()</code></b> invocando el método <b><code>chartInstance.destroy()</code></b>."
    story.append(make_print_qa(6, q6_t, a6_t))
    story.append(Spacer(1, 4))

    q7_t = "¿Para qué se utiliza el operador forkJoin de RxJS en el servicio de datos del Dashboard?"
    a7_t = "Para <b>orquestar peticiones asíncronas concurrentes</b> en paralelo (métricas globales, catálogo SQL y notificaciones NoSQL). <code>forkJoin</code> espera a que <b>todos los Observables completen</b> y emite una única respuesta agregada, permitiendo mostrar un único spinner de carga y renderizar el Dashboard en un solo ciclo atómico."
    story.append(make_print_qa(7, q7_t, a7_t))
    story.append(Spacer(1, 4))

    q8_t = "¿Por qué es necesario anteponer la marca BOM (\\uFEFF) al generar un archivo CSV para su descarga?"
    a8_t = "El <b>Byte Order Mark (BOM: <code>\\uFEFF</code>)</b> indica explícitamente a aplicaciones cliente como <b>Microsoft Excel</b> que el contenido entrante está codificado en UTF-8. Sin esta marca inicial, Excel asume por defecto codificación ANSI/Windows-1252, corrompiendo caracteres con tildes, la letra 'ñ' y el símbolo del euro (€)."
    story.append(make_print_qa(8, q8_t, a8_t))
    story.append(Spacer(1, 4))

    q9_t = "¿Qué función cumple la opción --no-ff al fusionar ramas en la metodología Git Flow?"
    a9_t = "La opción <code>--no-ff</code> (<i>No Fast-Forward</i>) fuerza a Git a <b>crear siempre un commit de fusión dedicado (<i>merge commit</i>)</b>, evitando que avance el puntero de forma lineal. Esto preserva de forma explícita la trazabilidad histórica de cuándo una rama de característica (<code>feature/*</code>) se integró en <code>develop</code> o <code>main</code>."
    story.append(make_print_qa(9, q9_t, a9_t))
    story.append(Spacer(1, 4))

    q10_t = "¿Por qué es imprescindible configurar reglas de reescritura (rewrites) en vercel.json para desplegar una SPA?"
    a10_t = "Porque en una <b>Single Page Application (SPA)</b> no existen archivos físicos HTML para cada ruta en el servidor. La regla de reescritura redirige internamente cualquier petición que no sea un archivo estático hacia <b><code>/index.html</code></b>. De este modo, si el usuario recarga la página en rutas profundas como <code>/dashboard</code>, el servidor entrega <code>index.html</code> en lugar de devolver error HTTP 404, permitiendo que el enrutador de Angular tome el control."
    story.append(make_print_qa(10, q10_t, a10_t))
    story.append(Spacer(1, 6))

    # Final summary tip box
    summary_box = [
        [Paragraph("<b>💡 GLOSARIO RÁPIDO DE PALABRAS CLAVE QUE SUMAN PUNTOS EN EL EXAMEN</b>", ParagraphStyle('ST', fontName='Helvetica-Bold', fontSize=7.5, textColor=c_blue))],
        [Paragraph(
            "• <b>Zero-Leakage:</b> Con <code>CanMatchFn</code> no se descarga el bundle por red si no tiene permisos.<br/>"
            "• <b>Inmutabilidad:</b> Con <code>req.clone({ setHeaders: ... })</code> en interceptores HTTP.<br/>"
            "• <b>Memory Leak:</b> Fuga de memoria si no se llama a <code>chart.destroy()</code> en <code>ngOnDestroy()</code>.<br/>"
            "• <b>BehaviorSubject:</b> Mantiene el último valor y lo emite inmediatamente a nuevos suscriptores.<br/>"
            "• <b>forkJoin:</b> Espera a que todos los Observables en paralelo completen (equivalente a <code>Promise.all</code>).<br/>"
            "• <b>BOM UTF-8 (<code>\\uFEFF</code>):</b> Evita caracteres corruptos al abrir CSV en Microsoft Excel.<br/>"
            "• <b>No Fast-Forward (<code>--no-ff</code>):</b> Crea merge commits explícitos para trazabilidad en Git Flow.<br/>"
            "• <b>SPA Rewrites:</b> Redirige a <code>index.html</code> en el hosting para evitar error 404 al recargar.",
            body_style
        )]
    ]
    t_summary = Table(summary_box, colWidths=[519])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#64748B")),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_summary)

    doc.build(story, canvasmaker=NumberedCanvas)

    import shutil
    shutil.copyfile(PDF_OUTPUT_PATH, DOCS_PDF_PATH)
    print(f"PDF imprimible de teoria generado con éxito en:\n1. {PDF_OUTPUT_PATH}\n2. {DOCS_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
