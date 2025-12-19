from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero

class WalloniadesEquipeInstance(models.Model):
    _name = "walloniades.equipe.instance"
    _description = "Une équipe d'une édition des walloniades"
    _order = "sequence asc"
    

    equipe_id=fields.Many2one("walloniades.equipe", required=True)
    walloniade_id = fields.Many2one("walloniades.walloniade", string = "Walloniade", required=True, ondelete="cascade")
    name = fields.Char(related="equipe_id.name", store=True)
    capitaine_id= fields.Many2one(related="equipe_id.capitaine_id", store=True)
    participant_ids = fields.One2many("res.partner",compute="_compute_participant_ids",string="Participants",readonly=True)
    numero = fields.Integer('Numéro attribué')
    sequence = fields.Integer('Sequence', default=1)
    #nbre_victoire = fields.Integer("Nombre d'épreuves remportées", default=0)
    #nbre_seconde_place = fields.Integer("Nombre de secondes places", default=0)
    #nbre_troisieme_place = fields.Integer("Nombre de troisièmes places", default=0)
                              
    @api.depends("equipe_id")
    def _compute_participant_ids(self):
        for rec in self:
            rec.participant_ids = rec.equipe_id.participant_ids

    @api.onchange("equipe_id")
    def _onchange_equipe_id(self):
        self._compute_participant_ids()
    
    