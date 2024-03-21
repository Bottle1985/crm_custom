# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
# Bottle added    
    table_payment = fields.One2many(
        comodel_name='payment.table.line',
        inverse_name='payment_id',
        string='Payment Lines'
    ) 
    
    amount_total = fields.Float(string="Total Amount", store=True, compute='_compute_amounts', tracking=5)
    # @api.depends('order_line.price_subtotal', 'order_line.price_tax', 'order_line.price_total')
    def _compute_amounts(self):
        """Compute the total amounts of the SO."""
        # for order in self:
            # order_lines = order.order_line.filtered(lambda x: not x.display_type)

            # if order.company_id.tax_calculation_rounding_method == 'round_globally':
                # tax_results = self.env['account.tax']._compute_taxes([
                    # line._convert_to_tax_base_line_dict()
                    # for line in order_lines
                # ])
                # totals = tax_results['totals']
                # amount_untaxed = totals.get(order.currency_id, {}).get('amount_untaxed', 0.0)
                # amount_tax = totals.get(order.currency_id, {}).get('amount_tax', 0.0)
            # else:
                # amount_untaxed = sum(order_lines.mapped('price_subtotal'))
                # amount_tax = sum(order_lines.mapped('price_tax'))

            # order.amount_untaxed = amount_untaxed
            # order.amount_tax = amount_tax
            # order.amount_total = order.amount_untaxed + order.amount_tax

    def write(self, vals):      
        if self.user_id != self.env.user and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError("You cannot edit Opp/Lead of other person")
        else:
            return super(CrmLead, self).write(vals)
