from odoo import models, fields, api


class BillingSummary(models.Model):
    _name = 'project.billing.summary'
    _description = 'Resumen de Facturación del Proyecto'
    _order = 'date desc'
    _rec_name = 'project_id'

    # ── Campos ──────────────────────────────────────────────────────────

    project_id = fields.Many2one(
        'project.project',
        string='Proyecto',
        required=True,
        ondelete='cascade',
    )

    partner_id = fields.Many2one(
        related='project_id.partner_id',
        string='Cliente',
        store=True,
    )

    date = fields.Date(
        string='Fecha',
        default=fields.Date.today,
        required=True,
    )

    hours_billed = fields.Float(
        string='Horas facturadas',
        required=True,
    )

    hourly_rate = fields.Float(
        string='Tarifa aplicada (€/h)',
        required=True,
    )

    total_amount = fields.Float(
        string='Importe total (€)',
        compute='_compute_total_amount',
        store=True,
    )

    invoice_id = fields.Many2one(
        'account.move',
        string='Factura',
        readonly=True,
    )

    state = fields.Selection(
        related='invoice_id.payment_state',
        string='Estado de pago',
        store=True,
    )

    notes = fields.Text(
        string='Notas',
    )

    # ── Lógica ──────────────────────────────────────────────────────────

    @api.depends('hours_billed', 'hourly_rate')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.hours_billed * record.hourly_rate

    # ── Métodos SQL para estadísticas ───────────────────────────────────

    def get_project_stats(self, project_id):
        """
        Usa SQL directo para obtener estadísticas agregadas
        de facturación de un proyecto.
        Demuestra conocimiento de env.cr.execute() y PostgreSQL.
        """
        self.env.cr.execute("""
            SELECT
                COUNT(*)                    AS total_invoices,
                SUM(hours_billed)           AS total_hours,
                SUM(total_amount)           AS total_revenue,
                AVG(hourly_rate)            AS avg_rate
            FROM project_billing_summary
            WHERE project_id = %s
        """, [project_id])

        result = self.env.cr.dictfetchone()
        return result or {
            'total_invoices': 0,
            'total_hours': 0.0,
            'total_revenue': 0.0,
            'avg_rate': 0.0,
        }