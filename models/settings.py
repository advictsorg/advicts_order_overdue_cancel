import datetime
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InventorySetting(models.TransientModel):
    _inherit = 'res.config.settings'

    overdue_cancel_activate = fields.Boolean(string='Order Overdue Cancel',
                                             default=lambda self: self.env.company.overdue_cancel_activate)

    def set_values(self):
        super(InventorySetting, self).set_values()
        self.env.company.overdue_cancel_activate = self.overdue_cancel_activate

    @api.model
    def get_values(self):
        res = super(InventorySetting, self).get_values()
        res.update(
            overdue_cancel_activate=self.env.company.overdue_cancel_activate
        )
        return res


class InventorySettings(models.TransientModel):
    _inherit = 'res.config.settings'

    overdue_cancel_days = fields.Integer(string='Overdue Cancel Days')

    def set_values(self):
        super(InventorySettings, self).set_values()
        self.env.company.overdue_cancel_days = self.overdue_cancel_days

    @api.model
    def get_values(self):
        res = super(InventorySettings, self).get_values()
        res.update(
            overdue_cancel_days=self.env.company.overdue_cancel_days
        )
        return res
