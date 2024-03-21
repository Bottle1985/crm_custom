# -*- coding: utf-8 -*-

from odoo import fields, models

# Bottle added
class PaymentInfo(models.Model):
    _name = 'payment.table.line'

    payment_id = fields.Many2one('crm.lead', string='Model')
    ngay = fields.Datetime(string='Ngày')
    so_tien = fields.Float(string='Số tiền')
    dang_thanh_toan = fields.Selection([('0','Chưa thanh toán'),('1','Chuyển khoản'),('2','Tiền mặt'),('3','Viettelpay')], string='Phương thức thanh toán',tracking=True)
    noi_dung_thanh_toan = fields.Selection([('1','Học phí học kỳ 1 (09 tín chỉ x 740,000)'),('2','Lệ phí nhập học (bắt buộc 490,000)'),('3','Bảo hiểm y tế (bắt buộc - 705,000)'),('4','Lệ phí khám sức khỏe (bắt buộc - 150,000)'), ('5','Bảo hiểm thân thể (tự nguyện - 150,000)')],string='Nội dung cần thanh toán', tracking=True)
    ghi_chu = fields.Text(string='Ghi chú')
    
   