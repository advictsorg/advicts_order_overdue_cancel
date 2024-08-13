from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    overdue_cancel_activate = fields.Boolean(string='Order Overdue Cancel')
    overdue_cancel_days = fields.Integer(string='Overdue Cancel Days')
