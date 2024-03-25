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
    
    amount_total = fields.Float(string="Total Amount", store=True, compute='_compute_amounts')
    # amount_total = fields.Monetary(string="Total Amount", store=True, compute='_compute_amounts', tracking=5)
    
    """Compute the total amounts of the fee payment."""
    @api.depends('table_payment.so_tien')
    def _compute_amounts(self):
        for lead in self:
            total_amount = 0.0
            for payment_line in lead.table_payment:
                total_amount += payment_line.so_tien
            lead.amount_total = total_amount
    def write(self, vals):      
        if self.user_id != self.env.user and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError("You cannot edit Opp/Lead of other person")
        else:
            return super(CrmLead, self).write(vals)
