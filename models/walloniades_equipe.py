from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero

class WalloniadesEquipe(models.Model):
    _name = "walloniades.equipe"
    _description = "Une équipe des walloniades"
    #_order = "id desc"
    

    
    name = fields.Char(string="Nom de l'équipe", copy=True)
    capitaine_id= fields.Many2one("res.partner", string = "Capitaine", copy = True, required=True)
    participant_ids = fields.Many2many("res.partner",  string = "Participants", copy=True)
    #walloniade_id = fields.Many2one("walloniades.walloniade", string = "Walloniade", required=True, ondelete="cascade")
    