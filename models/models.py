from odoo import models, fields, api
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class OrderCancellation(models.Model):
    _name = 'order.cancellation'
    _description = 'Order Cancellation'

    @api.model
    def cancel_overdue_orders(self):
        if self.env.company.overdue_cancel_activate and self.env.company.overdue_cancel_days:

            overdue_cancel_days = self.env.company.overdue_cancel_days
            today = fields.Date.today()
            days_ago = today - timedelta(days=overdue_cancel_days)

            # Find delivery orders to cancel
            pickings_to_cancel = self.env['stock.picking'].search([
                ('state', 'not in', ['done', 'cancel']),
                ('scheduled_date', '<', days_ago),
                ('picking_type_code', '=', 'outgoing')
            ])

            # Get the Odoo bot user
            bot_user = self.env.ref('base.user_root')

            cancellation_note = "Cancelled automatically: Overdue for more than 7 days without validation."

            for picking in pickings_to_cancel:
                # Cancel the delivery order
                if picking.state not in ['done', 'cancel']:
                    picking.with_user(bot_user).action_cancel()
                    picking.message_post(body=cancellation_note, author_id=bot_user.partner_id.id)
                    _logger.info(f"Cancelled delivery order {picking.name}")

                # Cancel the related sale order
                sale_order = picking.sale_id
                if sale_order and sale_order.state not in ['done', 'cancel']:
                    try:
                        sale_order.with_user(bot_user)._action_cancel()
                        sale_order.message_post(body=cancellation_note, author_id=bot_user.partner_id.id)
                        _logger.info(f"Cancelled sale order {sale_order.name}")
                    except Exception as e:
                        _logger.error(f"Failed to cancel sale order {sale_order.name}: {str(e)}")

                # Reset related invoices to draft and cancel them
                invoices = sale_order.invoice_ids if sale_order else self.env['account.move']
                for invoice in invoices.filtered(lambda inv: inv.state != 'cancel'):
                    try:
                        invoice.with_user(bot_user).button_draft()
                        invoice.with_user(bot_user).button_cancel()
                        invoice.message_post(body=cancellation_note, author_id=bot_user.partner_id.id)
                        _logger.info(f"Cancelled invoice {invoice.name}")
                    except Exception as e:
                        _logger.error(f"Failed to cancel invoice {invoice.name}: {str(e)}")

        return True
