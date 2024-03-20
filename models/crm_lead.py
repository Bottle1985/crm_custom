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
    dang_thanh_toan = fields.Selection([('0','Chưa thanh toán'),('1','Chuyển khoản'),('2','Tiền mặt'),('3','Viettelpay')], string='Phương thức thanh toán',tracking=True)
    # dang_thanh_toan = fields.Text(string='Dạng thanh toán')
    noi_dung_thanh_toan = fields.Selection([('1','Học phí học kỳ 1 (09 tín chỉ x 740,000)'),('2','Lệ phí nhập học (bắt buộc 490,000)'),('3','Bảo hiểm y tế (bắt buộc - 705,000)'),('4','Lệ phí khám sức khỏe (bắt buộc - 150,000)'), ('5','Bảo hiểm thân thể (tự nguyện - 150,000)')],string='Nội dung cần thanh toán', tracking=True)
    # noi_dung_thanh_toan = fields.Text(string='Nội dung thanh toán')
    ghi_chu = fields.Text(string='Ghi chú')