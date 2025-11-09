from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero


class WalloniadesResultatPoint(models.Model):
    _name = 'walloniades.resultat.point'
    _description = 'Résultat d\'une équipe à une épreuve de type point'
    #_order = "sequence asc"

    epreuve_instance_id = fields.Many2one("walloniades.epreuve.instance", required=True, ondelete="cascade")
    equipe_instance_id = fields.Many2one("walloniades.equipe.instance", required=True, ondelete="cascade")
    points = fields.Integer('Points', default=False)
    points_set = fields.Boolean(string="Résultat saisi ?", default=False)
    sequence = fields.Integer('Sequence', default=1, required=True)
    walloniade_id = fields.Many2one("walloniades.walloniade", required=True, ondelete='cascade')

    @api.onchange('points')
    def _onchange_points(self):
        for rec in self:
            rec._origin.points_set = True  # même si c'est 0, ça veut dire "saisi"

   
                

                
                

            



