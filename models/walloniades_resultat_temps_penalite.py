from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero


class WalloniadesResultatTempsPenalite(models.Model):
    _name = 'walloniades.resultat.temps.penalite'
    _description = 'Résultat d\'une équipe à une épreuve de type temps et pénalités'
    _order = "sequence asc"

    epreuve_instance_id = fields.Many2one("walloniades.epreuve.instance", required=True, ondelete="cascade")
    equipe_instance_id = fields.Many2one("walloniades.equipe.instance", required=True, ondelete="cascade")
    temps_brut = fields.Float('Temps Brut')
    penalites = fields.Integer('Pénalités')
    sequence = fields.Integer('Sequence', default=1, required=True)
    walloniade_id = fields.Many2one("walloniades.walloniade", required=True, ondelete='cascade')
    secondes = fields.Float('Temps brut en secondes', compute="_compute_secondes", store=True)
    temps_total_secondes = fields.Float('Temps total en secondes', compute="_compute_temps_total_secondes", store=True)
    minutes_final = fields.Integer('Minutes du temps final', default = 0, compute = "_compute_minutes_final", store=True)
    secondes_final = fields.Float('Secondes du temps final', default = 0, compute = "_compute_secondes_final", store=True)
    temps_final_char = fields.Char('Temps final', compute = "_compute_temps_final_char", store=True)
    reso_set = fields.Boolean(string="Résultat saisi ?", default=False)

    @api.onchange('temps_brut')
    def _onchange_temps_brut(self):
        for rec in self:
            rec._origin.reso_set = True  # même si c'est 0, ça veut dire "saisi"

    @api.onchange('penalites')
    def _onchange_penalites(self):
        for rec in self:
            rec._origin.reso_set = True  # même si c'est 0, ça veut dire "saisi"

    @api.depends ("temps_brut")
    def _compute_secondes(self):
        for record in self:
            temps=record.temps_brut
            s=0.00
            while (float_compare(temps, 100.00, precision_digits=2)>=0):
                s=s+60.00
                temps=temps-100.00
            s=s+temps
            record.secondes = s

        
    @api.depends ("secondes")
    def _compute_temps_total_secondes(self):
        for record in self:
            record.temps_total_secondes = record.secondes + (record.penalites * record.epreuve_instance_id.temps_de_penalite)
            

    @api.depends ("temps_total_secondes")
    def _compute_minutes_final(self):
        for record in self:
            m=0
            temps=record.temps_total_secondes
            while (float_compare(temps, 60.00, precision_digits=2)>=0):
                m=m+1
                temps=temps-60.00
            record.minutes_final = m
            

    @api.depends ("temps_total_secondes")
    def _compute_secondes_final(self):
        for record in self:
            temps=record.temps_total_secondes
            while (float_compare(temps, 60.00, precision_digits=2)>=0):
                temps=temps-60.00
            record.secondes_final = temps
            

    @api.depends ("minutes_final" , "secondes_final")
    def _compute_temps_final_char(self):
        for record in self:
            ss = int(record.secondes_final)  # partie entière des secondes
            cc = int(round((record.secondes_final - ss) * 100))
            record.temps_final_char = f"{record.minutes_final:02d}'{ss:02d}''{cc:02d}"
            
          