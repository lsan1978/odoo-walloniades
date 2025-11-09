from odoo import fields, models, api
from odoo.exceptions import UserError , ValidationError

class InheritedPartner(models.Model):
    
    _inherit = "res.partner"
    

    equipe_id=fields.Many2one("walloniades.equipe", string="Equipe")