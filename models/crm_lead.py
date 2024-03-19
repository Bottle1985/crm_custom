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
    def write(self, vals):      
        if self.user_id != self.env.user and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError("You cannot edit Opp/Lead of other person")
        else:
            return super(CrmLead, self).write(vals)
# Bottle added
class PaymentInfo(models.Model):
    _name = 'payment.table.line'

    payment_id = fields.Many2one('crm.lead', string='Model')
    ngay = fields.Datetime(string='Ngày')
    so_tien = fields.Float(string='Số tiền')
    noi_dung_thanh_toan = fields.Text(string='Nội dung thanh toán')
    dang_thanh_toan = fields.Text(string='Dạng thanh toán')
    ghi_chu = fields.Text(string='Ghi chú')