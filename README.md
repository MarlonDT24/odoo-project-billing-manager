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
