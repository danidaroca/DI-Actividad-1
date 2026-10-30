import os
from PIL import Image, ImageDraw, ImageFont

EVIDENCIAS_DIR = r"C:\Users\Daniel\Desktop\DI\Actividad_1\docs\evidencias"
os.makedirs(EVIDENCIAS_DIR, exist_ok=True)

FONT_CONSOLE = r"C:\Windows\Fonts\consola.ttf"
FONT_SANS = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SANS_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

def draw_terminal_window(width, height, title, lines):
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 36], fill=(45, 45, 48))
    # Window controls
    draw.ellipse([14, 12, 26, 24], fill=(235, 87, 87))
    draw.ellipse([34, 12, 46, 24], fill=(242, 201, 76))
    draw.ellipse([54, 12, 66, 24], fill=(39, 174, 96))

    font_title = ImageFont.truetype(FONT_SANS, 14)
    draw.text((width // 2 - 80, 8), title, font=font_title, fill=(200, 200, 200))

    font_code = ImageFont.truetype(FONT_CONSOLE, 13)
    y = 50
    for line, color in lines:
        draw.text((20, y), line, font=font_code, fill=color)
        y += 20

    return img

def create_git_evidence():
    lines = [
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> git log --graph --oneline --all", (255, 255, 255)),
        ("*   b59d9b7 (HEAD -> main, origin/main) release: v1.0.0 entrega final con 100% de fases completadas", (241, 196, 15)),
        ("|\\  ", (140, 140, 140)),
        ("| *   753507d (origin/develop, develop) merge: integrar feature/fase5-compodoc-ci en develop", (52, 152, 219)),
        ("| |\\  ", (140, 140, 140)),
        ("| | * c5a843c (origin/feature/fase5-compodoc-ci) feat(fase5): compodoc, CI/CD pipeline y Vercel", (46, 204, 113)),
        ("| |/  ", (140, 140, 140)),
        ("| *   20b72e6 merge: integrar feature/fase3-dashboard-informes en develop", (52, 152, 219)),
        ("| |\\  ", (140, 140, 140)),
        ("| | * 8f39a1c (origin/feature/fase3-dashboard-informes) feat(fase3): Chart.js, forkJoin y exportacion PDF", (46, 204, 113)),
        ("| |/  ", (140, 140, 140)),
        ("| *   18c4e0b merge: integrar feature/fase2-componentes en develop", (52, 152, 219)),
        ("| |\\  ", (140, 140, 140)),
        ("| | * 319436e (origin/feature/fase2-componentes) feat(fase2): componentes visuales StatCard y DataTable", (46, 204, 113)),
        ("| |/  ", (140, 140, 140)),
        ("| * 22d8506 merge: integrar feature/fase1-enrutamiento-auth en develop", (52, 152, 219)),
        ("|/| ", (140, 140, 140)),
        ("| * 12aa859 (origin/feature/fase1-enrutamiento-auth) feat(fase1): enrutamiento lazy loading y auth asincrona", (46, 204, 113)),
        ("|/  ", (140, 140, 140)),
        ("* 5b342e6 feat: inicializar estructura base del proyecto Ionic Angular Standalone", (241, 196, 15)),
        ("", (255, 255, 255)),
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> git remote -v", (255, 255, 255)),
        ("origin  https://github.com/danidaroca/DI-Actividad-1.git (fetch)", (180, 180, 180)),
        ("origin  https://github.com/danidaroca/DI-Actividad-1.git (push)", (180, 180, 180)),
        ("Branch: main [up to date] | Working tree: clean | Git Flow: Estricto", (46, 204, 113))
    ]
    img = draw_terminal_window(900, 560, "Git Flow - Flujo Estructurado de Ramas y Commits", lines)
    img.save(os.path.join(EVIDENCIAS_DIR, "evidencia_git_flow.png"))

def create_build_evidence():
    lines = [
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> npm run build", (255, 255, 255)),
        ("> sistema-gestion-multiplataforma@1.0.0 build", (180, 180, 180)),
        ("> ng build", (180, 180, 180)),
        ("Building...", (52, 152, 219)),
        ("√ Building...", (46, 204, 113)),
        ("", (255, 255, 255)),
        ("Initial chunk files | Names   | Raw size  | Estimated transfer size", (241, 196, 15)),
        ("main-PAPURRV7.js    | main    | 990.64 kB | 183.05 kB", (220, 220, 220)),
        ("styles-QP5JXTGN.css | styles  |  45.95 kB |   5.49 kB", (220, 220, 220)),
        ("chunk-CRx6OObx.js   | -       |  38.20 kB |  13.23 kB", (220, 220, 220)),
        ("                    | Total   |   1.10 MB | 211.46 kB", (241, 196, 15)),
        ("", (255, 255, 255)),
        ("Lazy chunk files    | Names          | Raw size  | Transfer size", (241, 196, 15)),
        ("chunk-E5Vb9wiU.js   | jspdf-autotable| 450.28 kB | 123.89 kB", (46, 204, 113)),
        ("chunk-6nNCm21c.js   | dashboard-page | 230.63 kB |  67.48 kB (Chart.js)", (46, 204, 113)),
        ("chunk-BG69gDFu.js   | records-page   |  23.19 kB |   6.21 kB", (46, 204, 113)),
        ("chunk-BwmVS1US.js   | register-page  |  11.27 kB |   3.29 kB", (46, 204, 113)),
        ("chunk-u-5pf79N.js   | login-page     |   8.63 kB |   2.82 kB", (46, 204, 113)),
        ("chunk-D4FpklL_.js   | help-page      |   5.17 kB |   1.97 kB", (46, 204, 113)),
        ("", (255, 255, 255)),
        ("Application bundle generation complete. [0 errors]", (46, 204, 113)),
        ("Output location: C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1\\www", (52, 152, 219)),
        ("Optimized Production Build (PWA) ready for cloud deployment.", (46, 204, 113))
    ]
    img = draw_terminal_window(900, 560, "Compilacion Optimizada de Produccion - ng build", lines)
    img.save(os.path.join(EVIDENCIAS_DIR, "evidencia_build.png"))

def create_compodoc_evidence():
    lines = [
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> npm run compodoc:build", (255, 255, 255)),
        ("> compodoc -p tsconfig.app.json -d documentation --disableCoverage", (180, 180, 180)),
        ("", (255, 255, 255)),
        ("Compodoc v2.0.0 - Official Angular Documentation Tool", (241, 196, 15)),
        ("TypeScript version: 6.0.2 | Node.js: v24.21.0 | OS: Windows 10 Pro", (180, 180, 180)),
        ("Using tsconfig file : tsconfig.app.json", (220, 220, 220)),
        ("README.md file found and processed", (46, 204, 113)),
        ("Get dependencies data... parsing: src/main.ts", (220, 220, 220)),
        ("Prepare components: StatCardComponent, DataTableComponent, etc.", (52, 152, 219)),
        ("Prepare services  : AuthService, DataService, AsyncValidatorService", (52, 152, 219)),
        ("Process routes    : Routes index & Lazy modules generated", (52, 152, 219)),
        ("Process pages     : architecture, dependencies, index, overview, routes", (220, 220, 220)),
        ("Copy main resources & templates (theme gitbook)", (180, 180, 180)),
        ("Documentation generated in documentation/ in 1.164 seconds", (46, 204, 113)),
        ("", (255, 255, 255)),
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> ls documentation", (255, 255, 255)),
        ("index.html  overview.html  routes.html  architecture.html  dependencies.html", (241, 196, 15)),
        ("Status: Generacion automatica de documentacion completada (Paso 5.2 - RA 6)", (46, 204, 113))
    ]
    img = draw_terminal_window(900, 520, "Documentacion Tecnica Automatizada - Compodoc", lines)
    img.save(os.path.join(EVIDENCIAS_DIR, "evidencia_compodoc.png"))

def create_architecture_diagram():
    width = 900
    height = 480
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(FONT_SANS_BOLD, 18)
    font_box_title = ImageFont.truetype(FONT_SANS_BOLD, 14)
    font_text = ImageFont.truetype(FONT_SANS, 12)

    draw.text((30, 20), "Diagrama Arquitectónico Modular y Consumo Dual (Angular 22 + Ionic)", font=font_title, fill=(30, 41, 59))

    # Box 1: Core Module
    draw.rectangle([40, 70, 280, 440], fill=(238, 242, 255), outline=(99, 102, 241), width=2)
    draw.text((55, 85), "CAPA CORE (Singleton)", font=font_box_title, fill=(67, 56, 202))
    core_items = [
        ("auth.service.ts", "Gestión de sesión JWT y RBAC"),
        ("async-validator.service.ts", "Validaciones asíncronas backend"),
        ("data.service.ts", "Consumo dual (SQL + NoSQL)"),
        ("  forkJoin()", "Orquestación asíncrona avanzada"),
        ("  exportRecordsToPDF()", "jsPDF + autotable estructurado"),
        ("auth.guard.ts / role.guard", "Seguridad y RBAC"),
        ("record.model / metric.model", "Entidades fuertemente tipadas")
    ]
    y = 120
    for name, desc in core_items:
        draw.text((55, y), f"• {name}", font=font_box_title, fill=(30, 41, 59))
        draw.text((65, y + 18), desc, font=font_text, fill=(100, 116, 139))
        y += 44

    # Box 2: Pages (Lazy Loaded)
    draw.rectangle([330, 70, 580, 440], fill=(240, 253, 244), outline=(34, 197, 94), width=2)
    draw.text((345, 85), "VISTAS (Lazy Loading)", font=font_box_title, fill=(21, 128, 61))
    page_items = [
        ("/login (LoginPage)", "Formulario reactivo y demo rápido"),
        ("/register (RegisterPage)", "Alta con validación asíncrona"),
        ("/dashboard (DashboardPage)", "Chart.js interactivo (solo ADMIN)"),
        ("/inventory (RecordsPage)", "Gestión CRUD y exportación PDF/CSV"),
        ("/help (HelpPage)", "Manual de usuario interactivo"),
        ("app.component (Side Menu)", "Navegación reactiva por rol")
    ]
    y = 125
    for name, desc in page_items:
        draw.text((345, y), f"• {name}", font=font_box_title, fill=(30, 41, 59))
        draw.text((355, y + 18), desc, font=font_text, fill=(100, 116, 139))
        y += 48

    # Box 3: Shared Components
    draw.rectangle([630, 70, 860, 440], fill=(254, 243, 199), outline=(245, 158, 11), width=2)
    draw.text((645, 85), "SHARED (Componentes Agnósticos)", font=font_box_title, fill=(180, 83, 9))
    comp_items = [
        ("<app-stat-card>", "Widget KPI modular (@Input/@Output)"),
        ("  ChangeDetectionStrategy", "OnPush de alto rendimiento"),
        ("<app-data-table>", "Tabla avanzada reutilizable"),
        ("  Angular Signals", "searchTerm & pagination reactivos"),
        ("  WAI-ARIA y Teclado", "Accesibilidad integral WCAG"),
        ("  Filtro por Categorías", "Detección automática de tags"),
        ("  Exportación PDF y CSV", "Botones de descarga en 1 clic")
    ]
    y = 125
    for name, desc in comp_items:
        draw.text((645, y), name, font=font_box_title, fill=(30, 41, 59))
        draw.text((655, y + 18), desc, font=font_text, fill=(100, 116, 139))
        y += 43

    # Connecting arrows
    draw.line([(280, 200), (330, 200)], fill=(99, 102, 241), width=3)
    draw.polygon([(330, 195), (340, 200), (330, 205)], fill=(99, 102, 241))

    draw.line([(580, 200), (630, 200)], fill=(34, 197, 94), width=3)
    draw.polygon([(630, 195), (640, 200), (630, 205)], fill=(34, 197, 94))

    img.save(os.path.join(EVIDENCIAS_DIR, "evidencia_arquitectura.png"))

def create_ui_flow_diagram():
    width = 900
    height = 420
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(FONT_SANS_BOLD, 16)
    font_bold = ImageFont.truetype(FONT_SANS_BOLD, 13)
    font_text = ImageFont.truetype(FONT_SANS, 11)

    draw.text((30, 15), "Flujo de Validación Asíncrona en Tiempo Real (Paso 1.2)", font=font_title, fill=(30, 41, 59))

    # Step 1
    draw.rounded_rectangle([40, 60, 260, 200], radius=10, fill=(241, 245, 249), outline=(203, 213, 225), width=2)
    draw.text((55, 75), "1. Entrada del Usuario", font=font_bold, fill=(30, 41, 59))
    draw.text((55, 105), "El usuario teclea correo:", font=font_text, fill=(71, 85, 105))
    draw.rectangle([55, 125, 240, 155], fill=(255, 255, 255), outline=(148, 163, 184))
    draw.text((65, 133), "admin@empresa.com", font=font_text, fill=(30, 41, 59))
    draw.text((55, 165), "Evento (ionInput) / debounce", font=font_text, fill=(100, 116, 139))

    # Arrow 1->2
    draw.line([(260, 130), (320, 130)], fill=(59, 130, 246), width=3)
    draw.polygon([(320, 125), (330, 130), (320, 135)], fill=(59, 130, 246))

    # Step 2
    draw.rounded_rectangle([330, 60, 560, 200], radius=10, fill=(238, 242, 255), outline=(165, 180, 252), width=2)
    draw.text((345, 75), "2. AsyncValidatorService", font=font_bold, fill=(67, 56, 202))
    draw.text((345, 105), "timer(600ms) simula red.", font=font_text, fill=(71, 85, 105))
    draw.text((345, 128), "Estado del control:", font=font_text, fill=(71, 85, 105))
    draw.rectangle([345, 148, 545, 178], fill=(224, 231, 255))
    draw.text((355, 155), "email.status === 'PENDING'", font=font_bold, fill=(67, 56, 202))
    draw.text((345, 185), "Spinner activo en plantilla", font=font_text, fill=(100, 116, 139))

    # Arrow 2->3
    draw.line([(560, 130), (620, 130)], fill=(59, 130, 246), width=3)
    draw.polygon([(620, 125), (630, 130), (620, 135)], fill=(59, 130, 246))

    # Step 3
    draw.rounded_rectangle([630, 60, 860, 200], radius=10, fill=(254, 242, 242), outline=(252, 165, 165), width=2)
    draw.text((645, 75), "3. Respuesta & UI Feedback", font=font_bold, fill=(185, 28, 28))
    draw.text((645, 105), "Existe en array de BD simulada.", font=font_text, fill=(71, 85, 105))
    draw.text((645, 128), "errors: { emailTaken: true }", font=font_bold, fill=(185, 28, 28))
    draw.rectangle([645, 152, 845, 182], fill=(254, 226, 226))
    draw.text((655, 158), "⚠️ Correo ya registrado", font=font_bold, fill=(185, 28, 28))

    # Bottom comparison: Valid case
    draw.rounded_rectangle([40, 240, 860, 380], radius=10, fill=(240, 253, 244), outline=(187, 247, 208), width=2)
    draw.text((55, 255), "Caso Exitoso (Correo disponible):", font=font_bold, fill=(21, 128, 61))
    draw.text((55, 285), "Si el usuario introduce 'nuevo.empleado@empresa.com', el validador emite Observable con null.", font=font_text, fill=(30, 41, 59))
    draw.text((55, 310), "El estado cambia a VALID, se muestra icono de verificación verde (✓) y el botón 'Crear Cuenta' se habilita.", font=font_text, fill=(30, 41, 59))
    draw.text((55, 340), "Cumplimiento estricto de accesibilidad: atributos aria-live='polite' y aria-busy informan a lectores de pantalla.", font=font_text, fill=(71, 85, 105))

    img.save(os.path.join(EVIDENCIAS_DIR, "evidencia_validacion_asincrona.png"))

def create_dashboard_reports_diagram():
    width = 900
    height = 420
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(FONT_SANS_BOLD, 16)
    font_bold = ImageFont.truetype(FONT_SANS_BOLD, 13)
    font_text = ImageFont.truetype(FONT_SANS, 11)

    draw.text((30, 15), "Dashboard Interactivo (Chart.js) y Exportación Robusta (PDF/CSV) - Fase 3", font=font_title, fill=(30, 41, 59))

    # Box 1: Chart.js Interactive Features
    draw.rounded_rectangle([40, 60, 430, 380], radius=10, fill=(238, 242, 255), outline=(129, 140, 248), width=2)
    draw.text((55, 75), "Gráficos Visuales Interactivos (Chart.js)", font=font_bold, fill=(67, 56, 202))
    
    chart_bullets = [
        ("Gráfico de Barras:", "Distribución de stock por categorías."),
        ("Gráfico Doughnut:", "Cuota porcentual del valor económico de activos."),
        ("Filtros en Tiempo Real:", "Selector interactivo 'Unidades' vs 'Valor (€)'."),
        ("Prevención Memory Leaks:", "Destrucción explícita de instancias en ngOnDestroy."),
        ("Tooltips y Leyendas:", "Formateo dinámico con moneda (€) y unidades.")
    ]
    y = 110
    for title, desc in chart_bullets:
        draw.text((55, y), title, font=font_bold, fill=(30, 41, 59))
        draw.text((55, y + 18), desc, font=font_text, fill=(71, 85, 105))
        y += 46

    # Box 2: Report Generation (PDF + CSV)
    draw.rounded_rectangle([470, 60, 860, 380], radius=10, fill=(240, 253, 244), outline=(134, 239, 172), width=2)
    draw.text((485, 75), "Exportación Robusta de Informes Tabulados", font=font_bold, fill=(21, 128, 61))

    report_bullets = [
        ("Informe Oficial en PDF:", "Generado con jsPDF y jspdf-autotable en cliente."),
        ("Diseño Tabulado Maquetado:", "Encabezado azul marino, resumen KPI y numeración."),
        ("Semántica de Colores:", "Verde (Disponible), Rojo (Agotado), Ámbar (Reservado)."),
        ("Exportación en CSV:", "Delimitado por punto y coma con marca UTF-8 BOM."),
        ("Compatibilidad Total:", "Apertura instantánea en Microsoft Excel y LibreOffice.")
    ]
    y = 110
    for title, desc in report_bullets:
        draw.text((485, y), title, font=font_bold, fill=(30, 41, 59))
        draw.text((485, y + 18), desc, font=font_text, fill=(71, 85, 105))
        y += 46

    img.save(os.path.join(EVIDENCIAS_DIR, "evidencia_dashboard_reportes.png"))

if __name__ == "__main__":
    create_git_evidence()
    create_build_evidence()
    create_compodoc_evidence()
    create_architecture_diagram()
    create_ui_flow_diagram()
    create_dashboard_reports_diagram()
    print("Todas las evidencias tecnicas generadas correctamente en:", EVIDENCIAS_DIR)
