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
    # tuition_ids = fields.Many2one('crm.cost', string='Tuitions', compute='_load_payment_fee')
    tuition_ids = fields.Many2one('crm.cost', string='Tuitions', help="Tổng tiền đóng = Lệ phí nhập học + Lệ phí khám sức khỏe + Bảo hiểm y tế + Tổng học phí học kì 1")
    save_cost_id = fields.Many2one('crm.save.cost', string='Save Cost')
    
    amount_total = fields.Float(string="Total Amount", store=True, compute='_compute_amounts')
    total_fee = fields.Float(string='Total Fee', compute='_compute_total_fees')
    reduced_fee = fields.Float(string='Reduced Fee', compute='_compute_reduced_fees')
    remain_fee = fields.Float(string='Remain Fee', compute='_compute_remain_fees')
      
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
            tuition = student.tuition_ids
            if tuition:
                total_fee = tuition.admission_fee + tuition.health_check_fee + tuition.insurance + tuition.total_course_cost
            student.total_fee = total_fee  
    # """Load all payment fee to table. This function set table to readonly"""             
    # def _load_payment_fee(self):  
        # first_payment = self.env['crm.cost'].search([], limit=1, order='id')
        # if first_payment: 
            # self.tuition_ids = first_payment.id
        # else:
            # self.tuition_ids = False    
    """Compute total fee reduced when have scholarship"""
    @api.depends('save_cost_id')
    def _compute_reduced_fees(self):
       for record in self:
            reduced_fee = 0.0
            if record.save_cost_id:
                reduced_fee = record.save_cost_id.corporate_scholarship + record.save_cost_id.admission_offer
         
            record.reduced_fee = reduced_fee
    """Compute the remain fee to pay"""        
    @api.depends('total_fee', 'amount_total', 'reduced_fee')
    def _compute_remain_fees(self):
        for record in self:
            remain_fee = record.total_fee - record.amount_total - record.reduced_fee
            record.remain_fee = remain_fee
            
    def write(self, vals):      
        if self.user_id != self.env.user and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError("You cannot edit Opp/Lead of other person")
        else:
            return super(CrmLead, self).write(vals)
