from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero

class WalloniadesEpreuve(models.Model):
    _name = "walloniades.epreuve"
    _description = "Une épreuve des walloniades"
    #_order = "id desc"
    

    
    name = fields.Char(string="Nom de l'épreuve", copy=True)
    type_epreuve_id = fields.Many2one("walloniades.type.epreuve", string = "Type d'épreuve")
    
    