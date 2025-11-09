from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero


class WalloniadesClassementLine(models.Model):
    _name = 'walloniades.classement.line'
    _description = 'Ligne de classement d''une épreive d''une walloniade'
    _order = "position asc"

    epreuve_instance_id = fields.Many2one("walloniades.epreuve.instance", ondelete="cascade")
    equipe_instance_id = fields.Many2one("walloniades.equipe.instance", required=True, ondelete="cascade")
    points = fields.Integer('Points')
    niveau = fields.Integer('Niveau')
    temps_final = fields.Float('Temps final')
    temps_final_string = fields.Char(string="Temps")
    position = fields.Integer('Position/Points', default=1, required=True)
    walloniade_id = fields.Many2one("walloniades.walloniade", required=True, ondelete='cascade')
    epreuve_concerned = fields.Boolean(string="Ligne concernant une epreuve ?", default=True)
    nbre_victoire = fields.Integer("Nombre d'épreuves remportées", default=0)
    nbre_seconde_place = fields.Integer("Nombre de secondes places", default=0)
    nbre_troisieme_place = fields.Integer("Nombre de troisièmes places", default=0)
    
