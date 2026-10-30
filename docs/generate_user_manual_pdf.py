import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\MANUAL_DE_USUARIO.pdf"
DOCS_PDF_PATH = r"C:\Users\Daniel\Desktop\DI\Actividad_1\docs\MANUAL_DE_USUARIO.pdf"

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
            self.drawString(48, 800, "DI (0488) - DAM 2 | Manual de Usuario y Guía de Operación")
            self.drawRightString(547, 800, "Sistema de Gestión Multiplataforma (Ionic + Angular)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(48, 792, 547, 792)

        # Running Footer
        self.line(48, 42, 547, 42)
        self.drawString(48, 30, "Manual de Usuario - Daniel Daroca | Repositorio: github.com/danidaroca/DI-Actividad-1")
        page_text = f"Página {self._pageNumber} de {total_pages}"
        self.drawRightString(547, 30, page_text)

        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=44,
        rightMargin=44,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    navy_blue = colors.HexColor("#0F172A")
    primary_blue = colors.HexColor("#1E40AF")
    accent_blue = colors.HexColor("#2563EB")
    slate_dark = colors.HexColor("#1E293B")
    border_color = colors.HexColor("#CBD5E1")
    code_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_blue,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=slate_dark,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=primary_blue,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=12,
        textColor=accent_blue,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=slate_dark,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.8,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.5,
        textColor=slate_dark
    )

    story = []

    # ================= PAGE 1 =================
    header_box = [
        [Paragraph("<b>MÓDULO PROFESIONAL: DESARROLLO DE INTERFACES (CÓDIGO 0488) - DAM 2</b>", ParagraphStyle('HBox', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#1E3A8A"), alignment=1))]
    ]
    t_header = Table(header_box, colWidths=[507])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C7D2FE")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Manual de Usuario y Guía de Operación", title_style))
    story.append(Paragraph("<b>Sistema de Gestión Empresarial Multiplataforma</b> | PWA Mobile-First con Ionic 9 y Angular 22 Standalone", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=accent_blue, spaceAfter=5, spaceBefore=1))

    meta_info = [
        [Paragraph("<b>Autor / Alumno:</b>", table_cell_style), Paragraph("Daniel Daroca (DAM 2)", table_cell_style),
         Paragraph("<b>Despliegue Vercel:</b>", table_cell_style), Paragraph("<b>https://di-actividad-1.vercel.app</b>", table_cell_style)],
        [Paragraph("<b>Repositorio GitHub:</b>", table_cell_style), Paragraph("<u>https://github.com/danidaroca/DI-Actividad-1</u>", table_cell_style),
         Paragraph("<b>Manual en Repo:</b>", table_cell_style), Paragraph("<code>docs/MANUAL_DE_USUARIO.md</code>", table_cell_style)]
    ]
    t_meta = Table(meta_info, colWidths=[95, 185, 95, 132])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Introducción y Descripción General", h1_style))
    story.append(Paragraph(
        "El presente manual describe el funcionamiento, navegación y características operativas del <b>Sistema de Gestión Empresarial Multiplataforma</b>. La solución está desarrollada sobre <b>Ionic Framework 9</b> y <b>Angular 22</b> con arquitectura Standalone Components, garantizando accesibilidad WCAG 2.1 AA, adaptabilidad responsiva completa y control de acceso basado en roles (RBAC).",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("2. Acceso al Sistema y Gestión de Identidades", h1_style))
    story.append(Paragraph("2.1. Pantalla de Inicio de Sesión (/login)", h2_style))
    story.append(Paragraph(
        "La pantalla de login cuenta con validación reactiva en tiempo real y <b>botones de acceso rápido de un clic</b> diseñados específicamente para agilizar la evaluación de ambos perfiles:",
        body_style
    ))

    cred_data = [
        [Paragraph("<b>Perfil / Rol</b>", table_header_style), Paragraph("<b>Correo Electrónico</b>", table_header_style), Paragraph("<b>Contraseña</b>", table_header_style), Paragraph("<b>Privilegios y Alcance en el Sistema</b>", table_header_style)],
        [Paragraph("<b>Administrador</b>", table_cell_style), Paragraph("admin@empresa.com", code_style), Paragraph("Admin123!", code_style), Paragraph("Acceso completo: Cuadro de Mando con Chart.js, Gestión de Catálogo, Creación, Borrado y Exportación de Informes.", table_cell_style)],
        [Paragraph("<b>Usuario Estándar</b>", table_cell_style), Paragraph("user@empresa.com", code_style), Paragraph("User123!", code_style), Paragraph("Acceso operativo: Consulta de catálogo, Alta de productos, Exportación de informes y Manual de ayuda. (Ruta /dashboard restringida por RoleGuard).", table_cell_style)]
    ]
    t_cred = Table(cred_data, colWidths=[80, 115, 75, 237])
    t_cred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_blue),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cred)
    story.append(Spacer(1, 3))

    story.append(Paragraph("2.2. Registro de Nuevos Usuarios (/register) con Validación Asíncrona", h2_style))
    story.append(Paragraph(
        "Al registrar un nuevo usuario, el campo de correo electrónico activa comprobación asíncrona contra el backend simulado (<code>AsyncValidatorService</code> con 600 ms de latencia):<br/>"
        "• <b>Estado PENDING:</b> Muestra un <code>ion-spinner</code> indicando <i>'Comprobando disponibilidad...'</i>.<br/>"
        "• <b>Estado INVALID:</b> Si el email ya existe (ej. <code>admin@empresa.com</code>), emite error semántico rojo y bloquea el botón.<br/>"
        "• <b>Estado VALID:</b> Si está libre, muestra un icono verde de confirmación y permite el registro.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("3. Cuadro de Mando y Analítica (/dashboard)", h1_style))
    story.append(Paragraph(
        "Vista analítica de alto nivel disponible exclusivamente para el perfil de <b>Administrador</b>. Si un usuario no administrador intenta forzar el acceso a través de la URL, el <code>roleGuard</code> lo intercepta de inmediato redirigiéndolo a <code>/inventory</code> con un mensaje informativo.",
        body_style
    ))

    story.append(Paragraph("3.1. Tarjetas de Indicadores Clave (KPIs)", h2_style))
    story.append(Paragraph(
        "En la zona superior se muestran 4 tarjetas construidas con el componente reutilizable <code>&lt;app-stat-card&gt;</code> con estrategia <code>ChangeDetectionStrategy.OnPush</code>:<br/>"
        "• <b>Total de Artículos:</b> Cantidad total de registros en el catálogo.<br/>"
        "• <b>Valoración Económica Total:</b> Sumatorio del valor de inventario calculado en euros (€).<br/>"
        "• <b>Alertas de Stock Crítico:</b> Artículos con existencias inferiores a 5 unidades.<br/>"
        "• <b>Categorías Activas:</b> Sectores industriales cubiertos en el almacén.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("3.2. Gráficos Interactivos con Chart.js", h2_style))
    story.append(Paragraph(
        "El cuadro de mando integra dos componentes visuales de datos impulsados por <b>Chart.js</b>:<br/>"
        "1. <b>Gráfico de Barras por Categoría:</b> Comparativa directa de existencias por familia de producto.<br/>"
        "2. <b>Gráfico Circular Doughnut:</b> Porcentaje de distribución del inventario.<br/>"
        "3. <b>Conmutador Interactivo de Métricas:</b> Permite alternar dinámicamente entre el modo <i>'Unidades en Stock'</i> y <i>'Valoración Económica (€)'</i>, recalculando y redibujando los gráficos sin recargar la página.<br/>"
        "4. <b>Gestión de Memoria:</b> Ambas instancias de gráficos se destruyen explícitamente en el hook <code>ngOnDestroy()</code> para prevenir fugas de memoria en cambios de vista.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Gestión de Catálogo e Inventario (/inventory)", h1_style))
    story.append(Paragraph("4.1. Componente de Tabla Avanzada (&lt;app-data-table&gt;)", h2_style))
    story.append(Paragraph(
        "Desarrollado con <b>Angular Signals</b> (<code>searchTerm</code>, <code>currentPage</code>, <code>selectedCategory</code>) para respuesta instantánea $O(1)$:<br/>"
        "• <b>Búsqueda en Tiempo Real:</b> Filtra sobre la marcha por código, denominación o familia.<br/>"
        "• <b>Filtro por Categoría:</b> Desplegable para segmentar por Tecnología, Mobiliario, Oficina, etc.<br/>"
        "• <b>Paginación Dinámica:</b> Selector de elementos por página (5, 10, 20) y botones de navegación rápida.<br/>"
        "• <b>Accesibilidad WAI-ARIA:</b> Soporte íntegro para navegación por teclado (foco con <code>Tab</code>, activación con <code>Enter</code> o <code>Espacio</code>).",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("4.2. Formulario Modal de Alta de Registros", h2_style))
    story.append(Paragraph(
        "Al pulsar el botón <b>'Nuevo Registro'</b>, se abre una ventana modal con formulario reactivo validado:<br/>"
        "• <b>Código de Artículo:</b> Validación asíncrona para impedir códigos duplicados (formato <code>PROD-XXX</code>).<br/>"
        "• <b>Descripción / Nombre:</b> Longitud mínima de 4 caracteres.<br/>"
        "• <b>Stock y Precio:</b> Controles numéricos con restricciones de valores positivos.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("4.3. Control de Acceso Condicional a Acciones (RBAC en UI)", h2_style))
    story.append(Paragraph(
        "Para ofrecer una experiencia de usuario preventiva y segura, las acciones destructivas se condicionan visualmente:<br/>"
        "• <b>Eliminación de Registros:</b> El botón de borrado (icono de papelera rojo) <b>únicamente es visible para el Administrador</b> (<code>[canDelete]='isAdmin'</code>). Para usuarios estándar, el control ni siquiera se renderiza en el DOM, imposibilitando la acción.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5. Generación y Exportación de Informes", h1_style))
    story.append(Paragraph(
        "Desde la barra superior o desde la cabecera del catálogo, se dispone de dos canales de exportación inmediata:",
        body_style
    ))

    export_data = [
        [Paragraph("<b>Formato de Exportación</b>", table_header_style), Paragraph("<b>Tecnología Empleada</b>", table_header_style), Paragraph("<b>Características del Informe Generado</b>", table_header_style)],
        [Paragraph("<b>Informe PDF Maquetado</b>", table_cell_style), Paragraph("<code>jsPDF</code> + <code>jspdf-autotable</code>", code_style), Paragraph("Orientación horizontal (Landscape), membrete corporativo, fecha de emisión, tarjetas resumen de KPIs, tabla con bandas alternas, colores semánticos por estado y numeración de página automática (Página X de Y).", table_cell_style)],
        [Paragraph("<b>Exportación CSV Normalizada</b>", table_cell_style), Paragraph("Codificación nativa TypeScript", code_style), Paragraph("Archivo delimitado por punto y coma (;) con cabeceras estándar y marca UTF-8 BOM para apertura directa y sin distorsión de caracteres en Microsoft Excel.", table_cell_style)]
    ]
    t_exp = Table(export_data, colWidths=[110, 120, 277])
    t_exp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_blue),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_exp)
    story.append(Spacer(1, 4))

    story.append(Paragraph("6. Navegación Global y Menú Lateral (IonMenu)", h1_style))
    story.append(Paragraph(
        "El menú lateral adaptativo (<code>ion-split-pane</code>) permite la navegación entre las secciones del sistema:<br/>"
        "• <b>Widget de Perfil:</b> Muestra el avatar, nombre, correo y un badge indicativo del rol activo.<br/>"
        "• <b>Enlaces Contextuales:</b> La opción <i>'Cuadro de Mando'</i> se oculta automáticamente para usuarios sin privilegios administrativos mediante directivas condicionales <code>@if (user.role === 'ADMIN')</code>.<br/>"
        "• <b>Manual Embebido (/help):</b> Sección de ayuda interactiva integrada directamente en la aplicación mediante acordeones expandibles.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 4 =================
    story.append(Paragraph("7. Preguntas Frecuentes y Solución de Problemas (FAQ)", h1_style))

    faq_data = [
        [Paragraph("<b>Pregunta / Escenario</b>", table_header_style), Paragraph("<b>Solución / Comportamiento del Sistema</b>", table_header_style)],
        [Paragraph("¿Por qué no aparece el enlace al Cuadro de Mando en el menú?", table_cell_style),
         Paragraph("El Cuadro de Mando está restringido por política RBAC exclusivamente al rol de Administrador. Si has iniciado sesión como usuario estándar (<code>user@empresa.com</code>), la opción no se renderiza. Para acceder a la analítica, inicia sesión con <code>admin@empresa.com</code>.", table_cell_style)],
        [Paragraph("¿Qué sucede si mi sesión expira mientras utilizo la aplicación?", table_cell_style),
         Paragraph("El interceptor de red funcional (<code>errorInterceptor</code>) interceptará automáticamente el código HTTP 401, revocará el token local y redirigirá de forma segura al usuario a la pantalla de login, recordando la URL de destino original (<code>returnUrl</code>) para restaurar el flujo tras identificarse.", table_cell_style)],
        [Paragraph("¿Cómo descargo el informe de inventario en Excel?", table_cell_style),
         Paragraph("Haz clic en el botón <b>'CSV'</b> en la barra superior o cabecera del inventario. El archivo descargado incorpora la firma UTF-8 BOM, por lo que abrirá con tildes, símbolos de euro (€) y columnas perfectamente ordenadas en Microsoft Excel.", table_cell_style)],
        [Paragraph("¿La aplicación es accesible desde dispositivos móviles o tablets?", table_cell_style),
         Paragraph("Sí, la aplicación ha sido diseñada con metodología <b>Mobile-First</b>. El menú lateral se convierte automáticamente en menú desplegable táctil, y las tablas y modales adaptan su densidad para uso cómodo en pantallas táctiles.", table_cell_style)]
    ]
    t_faq = Table(faq_data, colWidths=[150, 357])
    t_faq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy_blue),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_faq)
    story.append(Spacer(1, 6))

    story.append(Paragraph("8. Resumen de Enlaces y Recursos del Proyecto", h1_style))
    links_data = [
        [Paragraph("<b>Recurso Oficial</b>", table_header_style), Paragraph("<b>Dirección URL / Ubicación en el Proyecto</b>", table_header_style)],
        [Paragraph("Despliegue en Producción (Vercel):", table_cell_style), Paragraph("<font color='#2563EB'><u>https://di-actividad-1.vercel.app</u></font>", table_cell_style)],
        [Paragraph("Repositorio de Código (GitHub):", table_cell_style), Paragraph("<font color='#2563EB'><u>https://github.com/danidaroca/DI-Actividad-1</u></font>", table_cell_style)],
        [Paragraph("Memoria Técnica Oficial (Actividad 1):", table_cell_style), Paragraph("<code>MEMORIA_TECNICA_ACTIVIDAD_1.pdf</code> (7 páginas con evidencias)", table_cell_style)],
        [Paragraph("Anexo de Seguridad (RBAC & Guards):", table_cell_style), Paragraph("<code>Memoria_Seguridad_Ionic_Daroca_Daniel.pdf</code> (4 páginas con rúbrica)", table_cell_style)],
        [Paragraph("Manual de Usuario en Markdown:", table_cell_style), Paragraph("<code>docs/MANUAL_DE_USUARIO.md</code>", table_cell_style)]
    ]
    t_links = Table(links_data, colWidths=[160, 347])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_blue),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_links)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Fin del Manual de Usuario.</b> Para más detalles sobre el diseño técnico o arquitectura de software, consulte la memoria técnica del proyecto.", ParagraphStyle('Callout', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=primary_blue)))

    doc.build(story, canvasmaker=NumberedCanvas)

    import shutil
    shutil.copyfile(PDF_OUTPUT_PATH, DOCS_PDF_PATH)
    print(f"Manual de Usuario generado con éxito en:\n1. {PDF_OUTPUT_PATH}\n2. {DOCS_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
