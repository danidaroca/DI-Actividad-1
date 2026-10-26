import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage,
    KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\MEMORIA_TECNICA_ACTIVIDAD_1.pdf"
DOCS_PDF_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\docs\MEMORIA_TECNICA_ACTIVIDAD_1.pdf"
EVIDENCIAS_DIR = r"C:\Users\Daniel\Desktop\DI\Actividad_1\docs\evidencias"

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
        # We don't draw running header/footer on cover page (page 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#718096"))

            # Running Header
            self.drawString(54, 755, "DI (0488) - DAM | Sistema de Gestión Multiplataforma (Ionic + Angular)")
            self.drawRightString(540, 755, "Memoria Técnica de Proyecto")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 540, 747)

            # Running Footer
            self.line(54, 45, 540, 45)
            self.drawString(54, 32, "Entrega Individual - Daniel Daroca (Repositorio: github.com/danidaroca/DI-Actividad-1)")
            page_text = f"Página {self._pageNumber} de {total_pages}"
            self.drawRightString(540, 32, page_text)

            self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1E3A8A")   # Deep navy
    secondary_color = colors.HexColor("#2563EB") # Royal blue
    text_color = colors.HexColor("#1F2937")      # Dark slate
    light_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=0,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=0,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_color,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=text_color
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # ================= PAGE 1: PORTADA =================
    story.append(Spacer(1, 25))

    # Badge box
    badge_data = [[Paragraph("<b>DOCUMENTO DE ESPECIFICACIONES Y EVIDENCIAS TÉCNICAS</b>", ParagraphStyle('B', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#1E3A8A"), alignment=1))]]
    badge_table = Table(badge_data, colWidths=[490])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Diseño, Desarrollo y Despliegue de Sistema de Gestión Multiplataforma (PWA/Híbrida)", title_style))
    story.append(Paragraph("Memoria de Arquitectura, Componentización Reactiva, Validaciones Asíncronas y Control de Versiones Git Flow", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=secondary_color, spaceAfter=20, spaceBefore=5))

    # Meta Info Table
    meta_data = [
        [Paragraph("<b>Módulo Profesional:</b>", table_cell_style), Paragraph("Desarrollo de Interfaces (Código: 0488)", table_cell_style)],
        [Paragraph("<b>Ciclo Formativo:</b>", table_cell_style), Paragraph("Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM)", table_cell_style)],
        [Paragraph("<b>Tipo de Actividad:</b>", table_cell_style), Paragraph("Actividad Individual 1 - Proyecto de Evaluación Práctica", table_cell_style)],
        [Paragraph("<b>Alumno / Autor:</b>", table_cell_style), Paragraph("Daniel Daroca (Cuenta GitHub: <code>danidaroca</code>)", table_cell_style)],
        [Paragraph("<b>Stack Tecnológico:</b>", table_cell_style), Paragraph("Ionic Framework 9.0 + Angular 22 (Standalone) + TypeScript + RxJS", table_cell_style)],
        [Paragraph("<b>URL del Repositorio:</b>", table_cell_style), Paragraph("<b>https://github.com/danidaroca/DI-Actividad-1</b>", table_cell_style)],
        [Paragraph("<b>Estado de Entrega:</b>", table_cell_style), Paragraph("<b>Fase 1 y Fase 2 Completadas</b> (con cimientos de Fases 3, 4 y 5)", table_cell_style)]
    ]
    meta_table = Table(meta_data, colWidths=[150, 340])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))

    # Credenciales de Acceso
    story.append(Paragraph("1. Credenciales de Acceso para Evaluación", h2_style))
    story.append(Paragraph("La aplicación cuenta con botones de carga rápida en el Login para iniciar sesión con 1 clic en cualquiera de los dos perfiles:", body_style))

    cred_data = [
        [Paragraph("<b>Rol</b>", table_header_style), Paragraph("<b>Correo Electrónico</b>", table_header_style), Paragraph("<b>Contraseña</b>", table_header_style), Paragraph("<b>Alcance / Permisos</b>", table_header_style)],
        [Paragraph("<b>Administrador</b>", table_cell_style), Paragraph("admin@empresa.com", code_style), Paragraph("Admin123!", code_style), Paragraph("Cuadro de Mando, Gestión de Catálogo, Creación, Borrado y Exportación CSV.", table_cell_style)],
        [Paragraph("<b>Usuario Estándar</b>", table_cell_style), Paragraph("user@empresa.com", code_style), Paragraph("User123!", table_cell_style), Paragraph("Consulta de catálogo, Alta de nuevos productos, Manual de ayuda.", table_cell_style)]
    ]
    cred_table = Table(cred_data, colWidths=[95, 125, 80, 190])
    cred_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cred_table)
    story.append(Spacer(1, 15))

    # Alcance de la entrega
    story.append(Paragraph("2. Resumen del Alcance Implementado", h2_style))
    story.append(Paragraph("Siguiendo las directrices del enunciado, se ha desarrollado una solución funcional y limpia enfocada en los cimientos arquitectónicos:", body_style))
    
    scope_points = [
        "<b>Estructuración Declarativa (FASE 1 - RA 1 y 2):</b> Sistema de enrutamiento Lazy Loading, Guards (<code>authGuard</code> y <code>roleGuard</code>), y formularios reactivos con validación asíncrona de email en tiempo real contra backend simulado.",
        "<b>Componentización Visual (FASE 2 - RA 3):</b> Desarrollo de componentes desacoplados e instanciables (<code>StatCardComponent</code> y <code>DataTableComponent</code>) que operan mediante <code>@Input()</code> y <code>@Output()</code>.",
        "<b>Consumo Dual Asíncrono (FASE 3 - RA 5):</b> Servicio <code>DataService</code> que simula consumo de API REST relacional (SQL) y flujo de eventos en tiempo real (NoSQL Firestore) con exportación funcional a CSV.",
        "<b>Accesibilidad y Usabilidad (FASE 4 - RA 4):</b> Cumplimiento de normativas WCAG con atributos WAI-ARIA, contraste de color y navegación por teclado.",
        "<b>Control de Versiones (FASE 5 - RA 7):</b> Implementación estricta de <b>Git Flow</b> con ramas <code>main</code>, <code>develop</code> y feature branches sincronizadas en GitHub."
    ]
    for p in scope_points:
        story.append(Paragraph(f"• {p}", body_style))

    story.append(PageBreak())

    # ================= PAGE 2: GIT FLOW Y CONTROL DE VERSIONES =================
    story.append(Paragraph("3. Evidencia 1: Control de Versiones con Git Flow (RA 7)", h1_style))
    story.append(Paragraph("El proyecto ha sido gestionado íntegramente mediante Git desde el commit inicial, implementando la metodología <b>Git Flow</b> exigida en la rúbrica para alcanzar la máxima calificación:", body_style))

    git_table_data = [
        [Paragraph("<b>Rama</b>", table_header_style), Paragraph("<b>Propósito</b>", table_header_style), Paragraph("<b>Commits / Características</b>", table_header_style)],
        [Paragraph("<code>main</code>", code_style), Paragraph("Rama de entrega y producción.", table_cell_style), Paragraph("Release v1.0.0 que consolida las fases finalizadas.", table_cell_style)],
        [Paragraph("<code>develop</code>", code_style), Paragraph("Rama principal de integración.", table_cell_style), Paragraph("Fusión controlada sin avance rápido (<code>--no-ff</code>) de las features.", table_cell_style)],
        [Paragraph("<code>feature/fase1-enrutamiento-auth</code>", code_style), Paragraph("Feature branch de Fase 1.", table_cell_style), Paragraph("Arquitectura base, guards, sesión, login y alta reactiva con validación asíncrona.", table_cell_style)],
        [Paragraph("<code>feature/fase2-componentes</code>", code_style), Paragraph("Feature branch de Fase 2.", table_cell_style), Paragraph("Componentes agnósticos <code>StatCard</code> y <code>DataTable</code>, catálogo y dashboard.", table_cell_style)]
    ]
    git_table = Table(git_table_data, colWidths=[140, 150, 200])
    git_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(git_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Captura Técnica de Terminal: Árbol de Ramas y Commits</b>", h2_style))
    git_img_path = os.path.join(EVIDENCIAS_DIR, "evidencia_git_flow.png")
    if os.path.exists(git_img_path):
        story.append(RLImage(git_img_path, width=490, height=270))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Verificación del Remoto en GitHub:</b> El repositorio público se encuentra activo en <font color='#2563EB'><u>https://github.com/danidaroca/DI-Actividad-1</u></font> con todas sus ramas sincronizadas.", callout_style))

    story.append(PageBreak())

    # ================= PAGE 3: ARQUITECTURA Y CARGA DIFERIDA =================
    story.append(Paragraph("4. Evidencia 2: Base Arquitectónica y Carga Diferida (RA 1)", h1_style))
    story.append(Paragraph("Se ha configurado una arquitectura moderna basada en componentes autónomos (<b>Angular Standalone Components</b>) apoyados en la capa visual de Ionic Framework. La organización por capas asegura una separación estricta de responsabilidades:", body_style))

    arch_img_path = os.path.join(EVIDENCIAS_DIR, "evidencia_arquitectura.png")
    if os.path.exists(arch_img_path):
        story.append(RLImage(arch_img_path, width=490, height=250))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Sistema de Enrutamiento y Carga Diferida (Lazy Loading):</b>", h2_style))
    story.append(Paragraph("Cada vista se carga bajo demanda mediante <code>loadComponent()</code>, reduciendo significativamente el peso del paquete inicial (bundle) a transferir:", body_style))

    routes_data = [
        [Paragraph("<b>Ruta</b>", table_header_style), Paragraph("<b>Componente Lazy</b>", table_header_style), Paragraph("<b>Protección / Guards</b>", table_header_style), Paragraph("<b>Acceso por Rol</b>", table_header_style)],
        [Paragraph("<code>/login</code>", code_style), Paragraph("LoginPage", table_cell_style), Paragraph("Pública", table_cell_style), Paragraph("Todos", table_cell_style)],
        [Paragraph("<code>/register</code>", code_style), Paragraph("RegisterPage", table_cell_style), Paragraph("Pública", table_cell_style), Paragraph("Todos", table_cell_style)],
        [Paragraph("<code>/dashboard</code>", code_style), Paragraph("DashboardPage", table_cell_style), Paragraph("<code>authGuard</code>, <code>roleGuard</code>", code_style), Paragraph("<b>Solo ADMIN</b>", table_cell_style)],
        [Paragraph("<code>/inventory</code>", code_style), Paragraph("RecordsPage", table_cell_style), Paragraph("<code>authGuard</code>", code_style), Paragraph("ADMIN y STANDARD", table_cell_style)],
        [Paragraph("<code>/help</code>", code_style), Paragraph("HelpPage", table_cell_style), Paragraph("<code>authGuard</code>", code_style), Paragraph("ADMIN y STANDARD", table_cell_style)]
    ]
    routes_table = Table(routes_data, colWidths=[90, 110, 150, 140])
    routes_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(routes_table)

    story.append(PageBreak())

    # ================= PAGE 4: FORMULARIOS Y VALIDACIONES ASÍNCRONAS =================
    story.append(Paragraph("5. Evidencia 3: Formularios Declarativos y Validación Asíncrona (RA 2)", h1_style))
    story.append(Paragraph("El paso 1.2 exige la implementación de formularios reactivos con Data Binding (unidireccional y bidireccional) y validaciones asíncronas contra un servicio. Se ha implementado un servicio especializado <code>AsyncValidatorService</code> que simula una consulta asíncrona a la base de datos con una latencia de 600 ms:", body_style))

    val_img_path = os.path.join(EVIDENCIAS_DIR, "evidencia_validacion_asincrona.png")
    if os.path.exists(val_img_path):
        story.append(RLImage(val_img_path, width=490, height=225))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Gestión del Estado del Formulario en Plantilla:</b>", h2_style))
    form_states = [
        ("Estado PENDING", "Mientras la promesa/timer de red está en curso, <code>email?.status === 'PENDING'</code> activa automáticamente un <code>&lt;ion-spinner&gt;</code> con el texto 'Verificando disponibilidad en el servidor...'."),
        ("Estado INVALID (Duplicado)", "Si el email coincide con uno existente (ej. <code>admin@empresa.com</code>), el servicio emite <code>{ emailTaken: true }</code>. La interfaz muestra un aviso en rojo con icono de alerta y bloquea el botón de envío."),
        ("Estado VALID (Disponible)", "Si el correo está libre, emite <code>null</code>. El control pasa a estado válido, mostrando un check verde (✓) y permitiendo continuar."),
        ("Alta de Registros", "En el catálogo de inventario se replica esta arquitectura: el código de producto (ej. <code>PROD-001</code>) se valida asíncronamente para evitar colisiones de stock.")
    ]
    for title, desc in form_states:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", body_style))

    story.append(PageBreak())

    # ================= PAGE 5: COMPONENTES REUTILIZABLES Y SERVICIOS =================
    story.append(Paragraph("6. Evidencia 4: Componentes Visuales Desacoplados (RA 3)", h1_style))
    story.append(Paragraph("En cumplimiento estricto de la Fase 2, se han diseñado e implementado dos componentes completamente independientes del contenedor padre, con estrategia de detección de cambios <code>ChangeDetectionStrategy.OnPush</code>:", body_style))

    comp_spec_data = [
        [Paragraph("<b>Componente</b>", table_header_style), Paragraph("<b>Propiedades de Entrada (@Input)</b>", table_header_style), Paragraph("<b>Eventos de Salida (@Output)</b>", table_header_style), Paragraph("<b>Responsabilidad Visual</b>", table_header_style)],
        [
            Paragraph("<b>StatCardComponent</b><br/><code>&lt;app-stat-card&gt;</code>", code_style),
            Paragraph("• title: string<br/>• value: string|number<br/>• subtitle?: string<br/>• changePercentage?: number<br/>• trend: 'up'|'down'|'neutral'<br/>• colorTheme: string", table_cell_style),
            Paragraph("• cardClick: EventEmitter&lt;void&gt;", code_style),
            Paragraph("Widget métrico / KPI modular con insignias dinámicas de tendencia y paleta temática.", table_cell_style)
        ],
        [
            Paragraph("<b>DataTableComponent</b><br/><code>&lt;app-data-table&gt;</code>", code_style),
            Paragraph("• data: any[]<br/>• columns: TableColumn[]<br/>• searchPlaceholder: string<br/>• pageSize: number<br/>• canDelete: boolean", table_cell_style),
            Paragraph("• rowSelect: EventEmitter<br/>• rowEdit: EventEmitter<br/>• rowDelete: EventEmitter", code_style),
            Paragraph("Tabla avanzada con barra de búsqueda instantánea, filtrado automático por categorías, paginación y acciones CRUD.", table_cell_style)
        ]
    ]
    comp_spec_table = Table(comp_spec_data, colWidths=[115, 140, 115, 120])
    comp_spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(comp_spec_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("7. Evidencia 5: Persistencia Dual Asíncrona y Exportación (RA 5)", h1_style))
    story.append(Paragraph("El servicio <code>DataService</code> orquesta dos canales de información complementarios:", body_style))
    data_points = [
        "<b>Fuente 1 (API REST SQL Mock):</b> Gestiona los registros transaccionales (artículos de inventario) simulando llamadas HTTP asíncronas con operadores RxJS (<code>delay(450ms)</code>, <code>tap</code>, <code>map</code>). Permite listar, agregar y eliminar registros.",
        "<b>Fuente 2 (NoSQL Firestore Mock en Tiempo Real):</b> Canal de eventos reactivo basado en <code>BehaviorSubject&lt;SystemNotification[]&gt;</code>. Cada mutación en el catálogo (creación, edición, alertas de stock) genera un evento emitido instantáneamente a los suscriptores.",
        "<b>Exportación CSV Normalizada:</b> Método <code>exportRecordsToCSV()</code> que genera un archivo tabulado con cabeceras, delimitador estándar y codificación <code>UTF-8 BOM</code> (\uFEFF) para visualización inmediata en Microsoft Excel y suites ofimáticas."
    ]
    for dp in data_points:
        story.append(Paragraph(f"• {dp}", body_style))

    story.append(PageBreak())

    # ================= PAGE 6: COMPILACIÓN Y EVALUACIÓN =================
    story.append(Paragraph("8. Evidencia 6: Compilación de Producción y Verificación (RA 4, 6 y 7)", h1_style))
    story.append(Paragraph("Se ejecutó la compilación de producción mediante <code>ng build</code> con optimizaciones de tree-shaking, minificación y generación de chunks lazy. La compilación finalizó con <b>código de salida 0 y sin errores de presupuesto</b>:", body_style))

    build_img_path = os.path.join(EVIDENCIAS_DIR, "evidencia_build.png")
    if os.path.exists(build_img_path):
        story.append(RLImage(build_img_path, width=490, height=270))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Accesibilidad y Usabilidad WCAG 2.1 (RA 4):</b>", h2_style))
    story.append(Paragraph("La aplicación incorpora atributos semánticos <code>WAI-ARIA</code> (<code>role='table'</code>, <code>role='region'</code>, <code>aria-label</code>, <code>aria-busy</code>), soporte de navegación secuencial por tabulación (<code>tabindex='0'</code> con manejo de evento <code>Enter</code>) y alto contraste de color según directrices WCAG.", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("9. Matriz de Estado de las Fases del Proyecto", h2_style))
    phase_data = [
        [Paragraph("<b>Fase del Proyecto</b>", table_header_style), Paragraph("<b>Criterio Oficial</b>", table_header_style), Paragraph("<b>Estado en este Entregable</b>", table_header_style)],
        [Paragraph("FASE 1: Estructuración y Renderizado", table_cell_style), Paragraph("RA 1 y RA 2 (Enrutamiento, Guards, Form Reactivos, Validación Asíncrona)", table_cell_style), Paragraph("<b>COMPLETADA (100%)</b>", table_cell_style)],
        [Paragraph("FASE 2: Componentización Visual", table_cell_style), Paragraph("RA 3 (Componentes desacoplados, Inputs/Outputs, Signals, OnPush)", table_cell_style), Paragraph("<b>COMPLETADA (100%)</b>", table_cell_style)],
        [Paragraph("FASE 3: Consumo de Datos e Informes", table_cell_style), Paragraph("RA 5 (Persistencia dual SQL/NoSQL, Exportación CSV/PDF, Charts)", table_cell_style), Paragraph("<b>PARCIAL</b> (Servicio dual y CSV listos; Charts pendientes)", table_cell_style)],
        [Paragraph("FASE 4: Usabilidad y Accesibilidad", table_cell_style), Paragraph("RA 4 (Responsive Mobile-First, WCAG, ARIA, Teclado)", table_cell_style), Paragraph("<b>INTEGRADA</b> (Semántica ARIA y diseño adaptativo)", table_cell_style)],
        [Paragraph("FASE 5: Control de Versiones y Despliegue", table_cell_style), Paragraph("RA 6 y RA 7 (Git Flow, README, Manual, CI/CD Cloud)", table_cell_style), Paragraph("<b>PARCIAL</b> (Git Flow y Manual listos; Despliegue cloud pendiente)", table_cell_style)]
    ]
    phase_table = Table(phase_data, colWidths=[150, 210, 130])
    phase_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(phase_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Conclusión:</b> Se entrega un artefacto de software modular, estructurado con buenas prácticas de ingeniería de interfaces y con trazabilidad completa en GitHub.", callout_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)

    # Copy to docs/ as well
    import shutil
    shutil.copyfile(PDF_OUTPUT_PATH, DOCS_PDF_PATH)
    print(f"PDF generado con éxito en:\n1. {PDF_OUTPUT_PATH}\n2. {DOCS_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
