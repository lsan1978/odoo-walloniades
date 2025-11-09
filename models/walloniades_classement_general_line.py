from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero


class WalloniadesClassemenGeneralLine(models.Model):
    _name = 'walloniades.classement.general.line'
    _description = 'Ligne de classement général d''une walloniade'
    _order = "position asc"

    
    equipe_instance_id = fields.Many2one("walloniades.equipe.instance", required=True, ondelete="cascade")
    points = fields.Integer('Points')
    position = fields.Integer('Position/Points', default=1, required=True)
    walloniade_id = fields.Many2one("walloniades.walloniade", required=True, ondelete='cascade')
    nbre_victoire = fields.Integer("Nombre d'épreuves remportées", default=0)
    nbre_seconde_place = fields.Integer("Nombre de secondes places", default=0)
    nbre_troisieme_place = fields.Integer("Nombre de troisièmes places", default=0)
    