# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    def write(self, vals):      
        team_lead = self.env['crm.team'].search([('user_id', '=', self.env.uid)])            
        # if self.user_id != self.env.user:
        if self.user_id != self.env.user and len(team_lead)==0:
            raise UserError("You cannot edit Opp/Lead of other person")
        else:
            return super(CrmLead, self).write(vals)

        # _logger.info('Tala and Boong Check save lead', len(team_lead))
