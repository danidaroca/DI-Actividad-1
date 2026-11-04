import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\GUIA_ESTUDIO_EXAMEN.pdf"
DOCS_PDF_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\docs\GUIA_ESTUDIO_EXAMEN.pdf"

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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        if self._pageNumber > 1:
            self.drawString(44, 800, "DI (0488) - DAM 2 | Guía de Estudio Rápido para Examen (10 Preguntas Cortas)")
            self.drawRightString(551, 800, "Teoría Clave del Proyecto: Ionic 9 + Angular 22 Standalone")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(44, 792, 551, 792)

        # Running Footer
        self.line(44, 42, 551, 42)
        self.drawString(44, 30, "Guía de Examen - Daniel Daroca | Repositorio: github.com/danidaroca/DI-Actividad-1")
        page_text = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(551, 30, page_text)

        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=44,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    navy_blue = colors.HexColor("#0F172A")
    primary_blue = colors.HexColor("#1E40AF")
    accent_blue = colors.HexColor("#2563EB")
    slate_dark = colors.HexColor("#1E293B")
    border_color = colors.HexColor("#CBD5E1")
    code_bg = colors.HexColor("#F8FAFC")
    q_bg = colors.HexColor("#EFF6FF")
    ans_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=primary_blue,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=slate_dark,
        spaceAfter=5
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=primary_blue,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=accent_blue,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.2,
        textColor=slate_dark,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.8,
        textColor=colors.HexColor("#0F172A")
    )

    q_title_style = ParagraphStyle(
        'QTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E3A8A")
    )

    ans_style = ParagraphStyle(
        'AnsText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.8,
        textColor=colors.HexColor("#1E293B")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=slate_dark
    )

    story = []

    # ================= PAGE 1 =================
    header_box = [
        [Paragraph("<b>MÓDULO: DESARROLLO DE INTERFACES (CÓDIGO 0488) - DAM 2 | GUÍA DE EXAMEN</b>", ParagraphStyle('HBox', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#1E3A8A"), alignment=1))]
    ]
    t_header = Table(header_box, colWidths=[515])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Hojas de Estudio y Preparación de Examen Teórico-Práctico", title_style))
    story.append(Paragraph("<b>Resumen de Conceptos Clave y Simulacro de 10 Preguntas Cortas Resueltas</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=4, spaceBefore=1))

    meta_info = [
        [Paragraph("<b>Ciclo / Asignatura:</b>", table_cell_style), Paragraph("DAM 2 - Desarrollo de Interfaces (0488)", table_cell_style),
         Paragraph("<b>Despliegue Vercel:</b>", table_cell_style), Paragraph("<b>https://di-actividad-1.vercel.app</b>", table_cell_style)],
        [Paragraph("<b>Alumno / Repositorio:</b>", table_cell_style), Paragraph("Daniel Daroca | <u>github.com/danidaroca/DI-Actividad-1</u>", table_cell_style),
         Paragraph("<b>Stack Tecnológico:</b>", table_cell_style), Paragraph("Ionic 9, Angular 22, Chart.js, RxJS, Git Flow", table_cell_style)]
    ]
    t_meta = Table(meta_info, colWidths=[105, 185, 95, 130])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    story.append(Paragraph("BLOQUE 1: Arquitectura y Componentes Standalone", h1_style))
    story.append(Paragraph(
        "• <b>Standalone Components:</b> Componentes independientes sin <code>NgModule</code> (propiedad <code>standalone: true</code>). Importan sus dependencias en <code>imports: [...]</code> y se arrancan con <code>bootstrapApplication()</code>.<br/>"
        "• <b>Ventajas Técnicas:</b> Reducción drástica de código boilerplate, menor consumo de memoria y optimización del <b>Tree-Shaking</b> al eliminar módulos estáticos pesados.",
        body_style
    ))

    story.append(Paragraph("BLOQUE 2: Enrutamiento, Functional Guards y Rendimiento", h1_style))
    story.append(Paragraph(
        "• <b>Functional Guards (Angular 15+):</b> Funciones puras tipadas (<code>CanActivateFn</code>, <code>CanMatchFn</code>) que usan <code>inject()</code> sin clases ni constructores.<br/>"
        "• <b>DIFERENCIA CRÍTICA: <code>CanMatchFn</code> vs <code>CanActivateFn</code>:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b><code>CanMatchFn</code>:</b> Se evalúa <i>antes</i> de descargar el chunk JS lazy (<code>loadComponent</code>). Si retorna <code>false</code>, <b>el fichero JS jamás se descarga por red</b> (Zero-Leakage y ahorro de datos móviles).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b><code>CanActivateFn</code>:</b> Se evalúa <i>después</i> de que el chunk ya está descargado en memoria. Determina si el componente se inicializa en el DOM; se usa para comprobar sesión y redirigir con <code>returnUrl</code>.<br/>"
        "• <b>Redirección Contextual (<code>returnUrl</code>):</b> Guarda la ruta que el usuario intentó acceder (<code>state.url</code>) para navegar a ella tras el login exitoso.",
        body_style
    ))

    story.append(Paragraph("BLOQUE 3: HTTP Interceptors Funcionales (HttpInterceptorFn)", h1_style))
    story.append(Paragraph(
        "• <b>Mecanismo de Pipeline:</b> Middleware en cadena (<i>Chain of Responsibility</i>) registrado en <code>provideHttpClient(withInterceptors([...]))</code>.<br/>"
        "• <b>Inmutabilidad de HttpRequest:</b> Las peticiones salientes son inmutables. Para agregar la cabecera <code>Authorization: Bearer &lt;token&gt;</code> se debe invocar obligatoriamente <code>req.clone({ setHeaders: { ... } })</code>.<br/>"
        "• <b>Manejo de Errores de Red con RxJS <code>catchError</code>:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>HTTP 401 (Unauthorized):</b> Sesión inválida/expirada. Limpia el token y redirige a <code>/login?returnUrl=...</code> (o dispara Silent Refresh Token).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>HTTP 403 (Forbidden):</b> Sesión válida pero sin rol autorizado (violación de RBAC). Redirige a ruta segura (<code>/inventory</code>) sin cerrar la sesión.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("BLOQUE 4: Modelo de Control de Acceso (RBAC vs ABAC vs Flag)", h1_style))
    story.append(Paragraph(
        "• <b>Autenticación (AuthN) vs. Autorización (AuthZ):</b> AuthN comprueba '¿quién eres?' (credenciales/firma de JWT). AuthZ comprueba '¿qué tienes permitido hacer?' (permisos del rol en cada vista o acción).<br/>"
        "• <b>Modelo RBAC (Role-Based Access Control):</b> Mapea $Usuario \\to Rol (ADMIN, SUPERVISOR, USER) \\to Permisos Granulares$. Desacopla la lógica de permisos de las identidades de usuario.<br/>"
        "• <b>Comparativa frente a Alternativas:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>Frente a flag booleano (<code>isAdmin: boolean</code>):</b> El flag es frágil, no escala con roles intermedios y mezcla lógica de negocio.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- <b>Frente a ABAC (Attribute-Based):</b> ABAC evalúa contexto dinámico (IP, horario) con sobrecarga pesada. RBAC ofrece complejidad $O(1)$ en consultas locales de interfaz mediante Signals.<br/>"
        "• <b>Control Visual Condicional (UI/UX Preventivo):</b> Ocultar elementos antes de interactuar:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Menú lateral: <code>@if (user.role === 'ADMIN')</code> para enlace al Cuadro de Mando.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;- Tabla de datos: <code>[canDelete]='isAdmin'</code> para no renderizar el botón rojo de papelera a usuarios estándar.",
        body_style
    ))

    story.append(Paragraph("BLOQUE 5: Formularios Reactivos y Validación Asíncrona", h1_style))
    story.append(Paragraph(
        "• <b>Validador Asíncrono (<code>AsyncValidatorFn</code>):</b> Función que devuelve <code>Observable&lt;ValidationErrors | null&gt;</code> para comprobar datos en el backend con latencia simulada.<br/>"
        "• <b>Estados de Validación en Angular:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <b><code>PENDING</code>:</b> Petición en curso contra el servidor. La UI muestra <code>&lt;ion-spinner&gt;</code> y deshabilita el envío.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <b><code>INVALID</code>:</b> Email/código duplicado. Muestra aviso de error rojo y bloquea el botón.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. <b><code>VALID</code>:</b> Dato disponible (<code>null</code>). Muestra check verde y habilita el botón de envío.",
        body_style
    ))

    story.append(Paragraph("BLOQUE 6: Programación Reactiva con RxJS y Concurrencia", h1_style))
    story.append(Paragraph(
        "• <b><code>BehaviorSubject</code>:</b> Subject con valor inicial que emite inmediatamente el último estado registrado a cualquier nuevo suscriptor. Ideal para estado de sesión y catálogo reactivo.<br/>"
        "• <b><code>forkJoin</code> (Orquestación Concurrente):</b> Ejecuta múltiples Observables en paralelo y espera a que <b>todos completen</b> para emitir un único array con sus últimos valores (equivalente a <code>Promise.all</code>). Se usa en el Dashboard para consultar simultáneamente métricas, catálogo y alertas con un solo spinner.<br/>"
        "• <b>Angular Signals:</b> Reactividad fina $O(1)$ sin sobrecarga de Zone.js (<code>signal()</code>, <code>computed()</code>).",
        body_style
    ))

    story.append(Paragraph("BLOQUE 7: Visualización (Chart.js), Exportación y Despliegue", h1_style))
    story.append(Paragraph(
        "• <b>Fugas de Memoria en Chart.js (Memory Leaks):</b> Chart.js mantiene referencias vivas al Canvas 2D y suscriptores a eventos de ventana (resize/hover). <b>Es obligatorio destruirlo en <code>ngOnDestroy()</code> con <code>chart.destroy()</code></b>.<br/>"
        "• <b>Exportación PDF y CSV con UTF-8 BOM:</b> PDF horizontal maquetado con <code>jsPDF</code> y <code>jspdf-autotable</code>. En CSV se añade la marca <b>BOM (<code>\\uFEFF</code>)</b> para que Microsoft Excel reconozca tildes y el símbolo del euro (€).<br/>"
        "• <b>Git Flow:</b> Ramas <code>main</code>, <code>develop</code> y <code>feature/*</code> fusionadas con <code>--no-ff</code> (No Fast-Forward) para preservar la trazabilidad.<br/>"
        "• <b>Despliegue SPA en Vercel (<code>vercel.json</code>):</b> Regla <code>rewrites: [{\"source\": \"/(.*)\", \"destination\": \"/index.html\"}]</code> para que al recargar rutas profundas (ej. <code>/dashboard</code>) no dé error 404.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("PARTE 2: SIMULACRO DE EXAMEN (10 PREGUNTAS CORTAS RESUELTAS)", h1_style))
    story.append(Paragraph("Respuestas modelo oficiales con las palabras técnicas clave exigidas en evaluación de DAM:", subtitle_style))

    # Helper function to generate Q&A box
    def make_qa_box(num, q_text, a_text):
        qa_data = [
            [Paragraph(f"<b>❓ PREGUNTA {num}: {q_text}</b>", q_title_style)],
            [Paragraph(f"<b>Respuesta Modelo:</b> {a_text}", ans_style)]
        ]
        t = Table(qa_data, colWidths=[515])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), q_bg),
            ('BACKGROUND', (0,1), (-1,1), ans_bg),
            ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ('LINEBELOW', (0,0), (-1,0), 0.5, colors.HexColor("#BFDBFE")),
            ('PADDING', (0,0), (-1,-1), 3.5),
        ]))
        return t

    q1_text = "¿Cuál es la diferencia fundamental entre proteger una ruta con CanMatchFn frente a hacerlo con CanActivateFn?"
    a1_text = "La diferencia radica en la fase de enrutamiento y en el impacto de red sobre el <i>Lazy Loading</i>. <b><code>CanMatchFn</code></b> se evalúa <u>antes</u> de cargar el componente perezoso (<code>loadComponent</code>); si devuelve <code>false</code>, <b>el navegador jamás descarga el chunk JS por red</b>, garantizando <i>Zero-Leakage</i> y ahorro de ancho de banda móvil. En cambio, <b><code>CanActivateFn</code></b> se ejecuta <u>después</u> de haber descargado el chunk en memoria para comprobar si se inicializa en el DOM, usándose para validación de sesión y redirección contextual con <code>returnUrl</code>."
    story.append(make_qa_box(1, q1_text, a1_text))
    story.append(Spacer(1, 4))

    q2_text = "¿Por qué las peticiones en un HttpInterceptorFn deben clonarse y no modificarse directamente?"
    a2_text = "Porque las instancias de <code>HttpRequest</code> en Angular son <b>inmutables por diseño</b> para asegurar determinismo frente a reintentos concurrentes y cachés intermedias. Para propagar cabeceras de autorización (<code>Authorization: Bearer &lt;token&gt;</code>) es obligatorio invocar el método de clonación inmutable <b><code>req.clone({ setHeaders: { ... } })</code></b>."
    story.append(make_qa_box(2, q2_text, a2_text))
    story.append(Spacer(1, 4))

    q3_text = "¿Qué estrategia de manejo centralizado de errores debe aplicar un interceptor ante códigos HTTP 401 y 403?"
    a3_text = "Mediante el operador <code>catchError</code>: ante un <b>HTTP 401 (Unauthorized)</b> asume sesión expirada, revoca el token local de <code>localStorage</code> y redirige al usuario a <code>/login</code> guardando la ruta actual como <code>returnUrl</code> (o dispara un flujo de <i>Silent Refresh</i>). Ante un <b>HTTP 403 (Forbidden)</b> reconoce identidad válida pero sin permisos de rol suficientes (violación de RBAC); redirige a una ruta operativa segura (ej. <code>/inventory</code>) mostrando una alerta sin cerrar la sesión."
    story.append(make_qa_box(3, q3_text, a3_text))
    story.append(Spacer(1, 4))

    q4_text = "En el modelo de seguridad RBAC, ¿cuál es la diferencia técnica entre Autenticación y Autorización?"
    a4_text = "<b>Autenticación (AuthN):</b> Responde a <i>'¿Quién eres?'</i>. Comprueba criptográficamente la identidad declarada mediante credenciales (login) o la firma y vigencia de un token JWT. <b>Autorización (AuthZ):</b> Responde a <i>'¿Qué tienes permitido hacer?'</i>. Evalúa los privilegios o permisos asignados al rol del usuario autenticado (extraídos de los <i>claims</i> del token) para autorizar accesos a vistas (ej. <code>/dashboard</code>) o acciones operativas (ej. borrar registros)."
    story.append(make_qa_box(4, q4_text, a4_text))
    story.append(Spacer(1, 4))

    q5_text = "¿Cuáles son los tres estados de un formulario reactivo durante la validación asíncrona y qué debe mostrar la UI?"
    a5_text = "1. <b><code>PENDING</code>:</b> Petición en curso contra el servidor. La UI bloquea el botón y muestra un indicador de espera (<code>&lt;ion-spinner&gt;</code>).<br/>2. <b><code>INVALID</code>:</b> Validación fallida (ej. <code>{ emailTaken: true }</code>). La UI despliega alerta roja de error y mantiene deshabilitado el envío.<br/>3. <b><code>VALID</code>:</b> Validación superada con <code>null</code>. La UI muestra confirmación visual (check verde) y habilita el botón de envío."
    story.append(make_qa_box(5, q5_text, a5_text))

    story.append(PageBreak())

    # ================= PAGE 4 =================
    q6_text = "¿Qué problema crítico de rendimiento provoca no destruir una instancia de Chart.js y cómo se resuelve?"
    a6_text = "Provoca una <b>fuga de memoria (<i>Memory Leak</i>)</b>, ya que Chart.js retiene referencias al contexto 2D del Canvas y suscriptores a eventos globales de la ventana (<code>resize</code>, animaciones y puntero). Debe resolverse obligatoriamente en el hook de ciclo de vida <b><code>ngOnDestroy()</code></b> invocando el método <b><code>chartInstance.destroy()</code></b>."
    story.append(make_qa_box(6, q6_text, a6_text))
    story.append(Spacer(1, 4))

    q7_text = "¿Para qué se utiliza el operador forkJoin de RxJS en el servicio de datos del Dashboard?"
    a7_text = "Para <b>orquestar peticiones asíncronas concurrentes</b> en paralelo (métricas globales, catálogo SQL y notificaciones NoSQL). <code>forkJoin</code> espera a que <b>todos los Observables completen</b> y emite una única respuesta agregada, permitiendo mostrar un único spinner de carga y renderizar el Dashboard en un solo ciclo atómico."
    story.append(make_qa_box(7, q7_text, a7_text))
    story.append(Spacer(1, 4))

    q8_text = "¿Por qué es necesario anteponer la marca BOM (\\uFEFF) al generar un archivo CSV para su descarga?"
    a8_text = "El <b>Byte Order Mark (BOM: <code>\\uFEFF</code>)</b> indica explícitamente a aplicaciones cliente como <b>Microsoft Excel</b> que el contenido entrante está codificado en UTF-8. Sin esta marca inicial, Excel asume por defecto codificación ANSI/Windows-1252, corrompiendo caracteres con tildes, la letra 'ñ' y el símbolo del euro (€)."
    story.append(make_qa_box(8, q8_text, a8_text))
    story.append(Spacer(1, 4))

    q9_text = "¿Qué función cumple la opción --no-ff al fusionar ramas en la metodología Git Flow?"
    a9_text = "La opción <code>--no-ff</code> (<i>No Fast-Forward</i>) fuerza a Git a <b>crear siempre un commit de fusión dedicado (<i>merge commit</i>)</b>, evitando que avance el puntero de forma lineal. Esto preserva de forma explícita la trazabilidad histórica de cuándo una rama de característica (<code>feature/*</code>) se integró en <code>develop</code> o <code>main</code>."
    story.append(make_qa_box(9, q9_text, a9_text))
    story.append(Spacer(1, 4))

    q10_text = "¿Por qué es imprescindible configurar reglas de reescritura (rewrites) en vercel.json para desplegar una SPA?"
    a10_text = "Porque en una <b>Single Page Application (SPA)</b> no existen archivos físicos HTML para cada ruta en el servidor. La regla de reescritura redirige internamente cualquier petición que no sea un archivo estático hacia <b><code>/index.html</code></b>. De este modo, si el usuario recarga la página en rutas profundas como <code>/dashboard</code>, el servidor entrega <code>index.html</code> en lugar de devolver error HTTP 404, permitiendo que el enrutador de Angular tome el control."
    story.append(make_qa_box(10, q10_text, a10_text))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Consejo de Examen:</b> En preguntas cortas, prioriza siempre las palabras clave técnicas (<i>Zero-Leakage, inmutabilidad, Memory Leak, ngOnDestroy, BehaviorSubject, forkJoin, BOM UTF-8, RBAC, --no-ff, SPA rewrites</i>). ¡Mucho éxito en el examen!", ParagraphStyle('ExamTip', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=primary_blue)))

    doc.build(story, canvasmaker=NumberedCanvas)

    import shutil
    shutil.copyfile(PDF_OUTPUT_PATH, DOCS_PDF_PATH)
    print(f"Guía de estudio generada con éxito en:\n1. {PDF_OUTPUT_PATH}\n2. {DOCS_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
