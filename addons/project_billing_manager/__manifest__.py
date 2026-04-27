{
    'name': 'Project Billing Manager',
    'version': '17.0.1.0.0',
    'category': 'Project',
    'summary': 'Gestión de proyectos con facturación automática',
    'description': """
        Módulo que extiende la gestión de proyectos de Odoo añadiendo
        control de horas trabajadas, cálculo automático de importes
        facturables y generación de facturas desde el proyecto.
    """,
    'author': 'Marlon Torres',
    'website': 'https://github.com/MarlonDT24',
    'depends': ['project', 'account', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_project_views.xml',
        'views/billing_summary_views.xml',
        'views/menu.xml',
        'report/billing_report.xml',
        'report/billing_report_action.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}