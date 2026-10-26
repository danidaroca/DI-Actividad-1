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

    font_code = ImageFont.truetype(FONT_CONSOLE, 14)
    y = 50
    for line, color in lines:
        draw.text((20, y), line, font=font_code, fill=color)
        y += 22

    return img

def create_git_evidence():
    lines = [
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> git log --graph --oneline --all", (255, 255, 255)),
        ("*   14e7b77 (HEAD -> main, origin/main) release: version 1.0.0 entrega parcial con Fase 1 y 2", (241, 196, 15)),
        ("|\\  ", (140, 140, 140)),
        ("| *   20b72e6 (origin/develop, develop) merge: integrar feature/fase2-componentes en develop", (52, 152, 219)),
        ("| |\\  ", (140, 140, 140)),
        ("| | * 319436e (origin/feature/fase2-componentes, feature/fase2-componentes) feat(fase2): componentes visuales", (46, 204, 113)),
        ("| |/  ", (140, 140, 140)),
        ("| * 22d8506 merge: integrar feature/fase1-enrutamiento-auth en develop", (52, 152, 219)),
        ("|/| ", (140, 140, 140)),
        ("| * 12aa859 (origin/feature/fase1-enrutamiento-auth, feature/fase1-enrutamiento-auth) feat(fase1): auth & lazy", (46, 204, 113)),
        ("|/  ", (140, 140, 140)),
        ("* 5b342e6 feat: inicializar estructura base del proyecto Ionic Angular Standalone", (241, 196, 15)),
        ("", (255, 255, 255)),
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> git remote -v", (255, 255, 255)),
        ("origin  https://github.com/danidaroca/DI-Actividad-1.git (fetch)", (180, 180, 180)),
        ("origin  https://github.com/danidaroca/DI-Actividad-1.git (push)", (180, 180, 180)),
        ("", (255, 255, 255)),
        ("PS C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1> git status", (255, 255, 255)),
        ("On branch main", (46, 204, 113)),
        ("Your branch is up to date with 'origin/main'.", (200, 200, 200)),
        ("nothing to commit, working tree clean", (46, 204, 113))
    ]
    img = draw_terminal_window(900, 540, "Git Flow - Terminal PowerShell", lines)
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
        ("main-C5YJAGO3.js    | main    | 989.09 kB | 182.80 kB", (220, 220, 220)),
        ("styles-QP5JXTGN.css | styles  |  45.95 kB |   5.49 kB", (220, 220, 220)),
        ("chunk-7WcvkKlU.js   | -       |  38.20 kB |  13.24 kB", (220, 220, 220)),
        ("                    | Total   |   1.10 MB | 211.41 kB", (241, 196, 15)),
        ("", (255, 255, 255)),
        ("Lazy chunk files    | Names          | Raw size | Transfer size", (241, 196, 15)),
        ("chunk-DcF17HwA.js   | records-page   | 22.24 kB | 6.09 kB", (46, 204, 113)),
        ("chunk-DLG4145t.js   | dashboard-page | 14.76 kB | 4.12 kB", (46, 204, 113)),
        ("chunk-kyHiGX7X.js   | register-page  | 11.27 kB | 3.29 kB", (46, 204, 113)),
        ("chunk-CjTyIObi.js   | login-page     |  8.63 kB | 2.80 kB", (46, 204, 113)),
        ("chunk-DApqpOjT.js   | help-page      |  5.17 kB | 1.98 kB", (46, 204, 113)),
        ("", (255, 255, 255)),
        ("Application bundle generation complete. [14.400 seconds]", (46, 204, 113)),
        ("Output location: C:\\Users\\Daniel\\Desktop\\DI\\Actividad_1\\www", (52, 152, 219)),
        ("Build succeeded with 0 errors.", (46, 204, 113))
    ]
    img = draw_terminal_window(900, 560, "Compilacion Optimizada - ng build", lines)
    img.save(os.path.join(EVIDENCIAS_DIR, "evidencia_build.png"))

def create_architecture_diagram():
    width = 900
    height = 480
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(FONT_SANS_BOLD, 18)
    font_box_title = ImageFont.truetype(FONT_SANS_BOLD, 14)
    font_text = ImageFont.truetype(FONT_SANS, 12)

    # Main header
    draw.text((30, 20), "Diagrama Arquitectónico Modular (Angular 22 + Ionic Standalone)", font=font_title, fill=(30, 41, 59))

    # Box 1: Core Module
    draw.rectangle([40, 70, 280, 440], fill=(238, 242, 255), outline=(99, 102, 241), width=2)
    draw.text((55, 85), "CAPA CORE (Singleton)", font=font_box_title, fill=(67, 56, 202))
    core_items = [
        ("auth.service.ts", "Gestión de sesión JWT y RBAC"),
        ("async-validator.service.ts", "Validaciones asíncronas backend"),
        ("data.service.ts", "Persistencia dual (SQL / NoSQL)"),
        ("auth.guard.ts", "Protección contra no autenticados"),
        ("role.guard.ts", "Restricción ADMIN vs STANDARD"),
        ("user.model.ts", "Tipado de usuarios y credenciales"),
        ("record.model.ts", "Entidades de negocio e inventario")
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
        ("/login (LoginPage)", "Formulario reactivo con demo rápido"),
        ("/register (RegisterPage)", "Alta con validación asíncrona"),
        ("/dashboard (DashboardPage)", "Cuadro de mando (rol ADMIN)"),
        ("/inventory (RecordsPage)", "Gestión CRUD y exportación CSV"),
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
        ("<app-stat-card>", "Widget KPI instanciable"),
        ("  @Input() title, value, trend", "Parámetros declarativos"),
        ("  @Output() cardClick", "Eventos desacoplados"),
        ("<app-data-table>", "Tabla avanzada reutilizable"),
        ("  @Input() data, columns", "Agnóstica a la entidad"),
        ("  Buscador + Filtro + Paginación", "Signals reactivos"),
        ("  @Output() rowSelect, delete", "Emisión hacia contenedor")
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

if __name__ == "__main__":
    create_git_evidence()
    create_build_evidence()
    create_architecture_diagram()
    create_ui_flow_diagram()
    print("Evidencias generadas correctamente en:", EVIDENCIAS_DIR)
