# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    def write(self, vals):      
        if self.user_id != self.env.user and not self.env.user.has_group('sales_team.group_sale_manager'):
            raise UserError("You cannot edit Opp/Lead of other person")
        else:
            return super(CrmLead, self).write(vals)
