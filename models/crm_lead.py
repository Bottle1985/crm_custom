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
    tuition_ids = fields.Many2many('crm.cost', string='Tuitions', compute='_load_payment_fee')
    save_cost_id = fields.Many2one('crm.save.cost', string='Save Cost')
    
    amount_total = fields.Float(string="Total Amount", store=True, compute='_compute_amounts')
    total_fee = fields.Float(string='Total Fee', compute='_compute_total_fees')
   
    
    """Compute the total amounts of the fee payment."""
    @api.depends('table_payment.so_tien')
    def _compute_amounts(self):
        for lead in self:
            total_amount = 0.0
            for payment_line in lead.table_payment:
                total_amount += payment_line.so_tien
            lead.amount_total = total_amount
            
    """Compute the total fee need to pay when first year."""        
    @api.depends('tuition_ids')
    def _compute_total_fees(self):
        for student in self:
            total_fee = 0.0
            for tuition in student.tuition_ids:
                total_fee += tuition.admission_fee + tuition.health_check_fee + tuition.insurance
            student.total_fee = total_fee  
    """Load all payment fee to table. This function set table to readonly"""             
    def _load_payment_fee(self):  
        all_payment = self.env['crm.cost'].search([])
        for lead in self:            
            lead.tuition_ids = all_payment 

    def write(self, vals):      
        if self.user_id != self.env.user and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError("You cannot edit Opp/Lead of other person")
        else:
            return super(CrmLead, self).write(vals)
