from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    hourly_rate = fields.Float(
        string='Tarifa por hora (€)',
        default=50.0,
    )

    billing_status = fields.Selection(
        selection=[
            ('pending', 'Pendiente de facturar'),
            ('invoiced', 'Facturado'),
            ('cancelled', 'Cancelado'),
        ],
        string='Estado de facturación',
        default='pending',
        tracking=True,
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
    )

    total_hours = fields.Float(
        string='Total horas trabajadas',
        compute='_compute_billing_totals',
        store=True,
    )

    billable_amount = fields.Float(
        string='Importe facturable (€)',
        compute='_compute_billing_totals',
        store=True,
    )

    invoice_count = fields.Integer(
        string='Facturas generadas',
        compute='_compute_invoice_count',
    )

    @api.depends('timesheet_ids', 'hourly_rate')
    def _compute_billing_totals(self):
        for project in self:
            total = sum(project.timesheet_ids.mapped('unit_amount'))
            project.total_hours = total
            project.billable_amount = total * project.hourly_rate

    def _compute_invoice_count(self):
        for project in self:
            invoices = self.env['account.move'].search([
                ('invoice_origin', '=', project.name),
                ('move_type', '=', 'out_invoice'),
            ])
            project.invoice_count = len(invoices)

    def action_generate_invoice(self):
        self.ensure_one()

        if not self.partner_id:
            raise ValidationError(
                'El proyecto no tiene cliente asignado. '
                'Asigna un cliente antes de generar la factura.'
            )

        if self.billable_amount <= 0:
            raise ValidationError(
                'No hay horas registradas en este proyecto. '
                'Registra partes de horas antes de facturar.'
            )

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': f'Servicios del proyecto: {self.name}',
                'quantity': self.total_hours,
                'price_unit': self.hourly_rate,
            })],
        })

        self.billing_status = 'invoiced'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Factura generada',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facturas del proyecto',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [
                ('invoice_origin', '=', self.name),
                ('move_type', '=', 'out_invoice'),
            ],
            'target': 'current',
        }

    @api.constrains('hourly_rate')
    def _check_hourly_rate(self):
        for project in self:
            if project.hourly_rate < 0:
                raise ValidationError(
                    'La tarifa por hora no puede ser negativa.'
                )