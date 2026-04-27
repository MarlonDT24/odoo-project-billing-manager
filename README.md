# Project Billing Manager — Odoo 17

Módulo personalizado para Odoo 17 que extiende la gestión de proyectos 
añadiendo control de facturación basado en partes de horas.

## ¿Qué hace este módulo?

Permite a las consultoras y empresas de servicios gestionar el ciclo 
completo de facturación de proyectos directamente desde Odoo:

- Configura una tarifa por hora para cada proyecto
- Calcula automáticamente el importe facturable según las horas registradas
- Genera facturas de cliente con un solo clic
- Registra el historial completo de facturación por proyecto

## Técnicas demostradas

| Técnica | Implementación |
|---|---|
| Herencia de modelos | `_inherit = 'project.project'` |
| Campos computados | `@api.depends('timesheet_ids', 'hourly_rate')` |
| Validaciones | `ValidationError` con lógica de negocio |
| Creación via ORM | `env['account.move'].create()` |
| Herencia de vistas XML | `xpath` sobre vistas estándar de Odoo |
| QWeb (reportes PDF) | Template de resumen de facturación |
| SQL directo | `env.cr.execute()` para estadísticas agregadas |
| Seguridad | `ir.model.access.csv` con roles diferenciados |

## Estructura del módulo

```
project_billing_manager/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── project_project.py      # Herencia + lógica de facturación
│   └── billing_summary.py      # Modelo propio de historial
├── views/
│   ├── project_project_views.xml
│   ├── billing_summary_views.xml
│   └── menu.xml
├── report/
│   ├── billing_report.xml
│   └── billing_report_action.xml
└── security/
    └── ir.model.access.csv
```

## Instalación

### Requisitos
- Odoo 17 Community
- Módulos: `project`, `account`, `hr_timesheet`

### Con Docker (recomendado)

```bash
git clone https://github.com/MarlonDT24/odoo-project-billing-manager.git
cd odoo-project-billing-manager
docker-compose up -d
```

Accede a `http://localhost:8069` e instala el módulo 
`project_billing_manager` desde Aplicaciones.

### Manual

Copia la carpeta `addons/project_billing_manager` a tu directorio 
de addons y actualiza la lista de módulos.

## Flujo de uso

1. Abre un proyecto en Odoo
2. Ve a la pestaña **Facturación**
3. Asigna un cliente y configura la tarifa por hora
4. Registra horas en los partes de horas del proyecto
5. Pulsa **Generar Factura** — se crea automáticamente con las horas y tarifa

## Autor

**Marlon Torres** — Desarrollador Odoo & FullStack  
[LinkedIn](https://www.linkedin.com/in/marlon-torres-982a17305) · 
[GitHub](https://github.com/MarlonDT24) · 
[Portfolio](https://marlondev-portfolio.vercel.app)
