from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero

class WalloniadesWalloniade(models.Model):
    _name = "walloniades.walloniade"
    _description = "Une Walloniade"
    #_order = "id desc"
    

    
    name = fields.Char(string="Année", copy=False)
    equipe_instance_ids=fields.One2many("walloniades.equipe.instance", "walloniade_id", string="Equipes")
    state = fields.Selection(string='Status', selection=[('ungenerated', 'Ungenerated'), ('generated', 'Generated')], default='ungenerated', required=True, copy=False)
    epreuve_instance_ids = fields.One2many("walloniades.epreuve.instance", "walloniade_id", string="Epreuves")
    classement_line_ids = fields.One2many("walloniades.classement.line", "walloniade_id", string="Lignes de classement")
    classement_general_line_ids = fields.One2many("walloniades.classement.general.line", "walloniade_id", string="Lignes de classement general")

    @api.constrains('name')
    def _check_name_is_valid_year(self):
        for record in self:
            if not record.name:
                continue  # facultatif selon ton besoin
            try:
                year = int(record.name)
            except ValueError:
                raise ValidationError("L'année doit être un nombre (ex : 2024).")

            if year < 2024:
                raise ValidationError("L'année doit être postérieure à 2023.")
            

    def action_generer_resultat(self):
        for record in self:
            for epreuve in record.epreuve_instance_ids:
                if (epreuve.type_epreuve_id.name=="Epreuve à points"):
                    for equipe in record.equipe_instance_ids:
                        
                        values = {
                            'epreuve_instance_id' : epreuve.id,
                            'equipe_instance_id' : equipe.id,
                            'walloniade_id' : record.id,
                            'sequence' : 1,
                        }
                        self.env['walloniades.resultat.point'].create(values)
                        

                if (epreuve.type_epreuve_id.name=="Epreuve à temps et pénalités"):
                    for equipe in record.equipe_instance_ids:
                        values = {
                            'epreuve_instance_id' : epreuve.id,
                            'equipe_instance_id' : equipe.id,
                            'walloniade_id' : record.id,
                            'sequence' : 1,
                        }
                        self.env['walloniades.resultat.temps.penalite'].create(values)

                if (epreuve.type_epreuve_id.name=="Epreuve à temps positif et négatif"):
                    for equipe in record.equipe_instance_ids:
                        values = {
                            'epreuve_instance_id' : epreuve.id,
                            'equipe_instance_id' : equipe.id,
                            'walloniade_id' : record.id,
                            'sequence' : 1,
                        }
                        self.env['walloniades.resultat.temps.positif.negatif'].create(values)

                if (epreuve.type_epreuve_id.name=="Epreuve à temps et niveau"):
                    for equipe in record.equipe_instance_ids:
                        values = {
                            'epreuve_instance_id' : epreuve.id,
                            'equipe_instance_id' : equipe.id,
                            'walloniade_id' : record.id,
                            'sequence' : 1,
                        }
                        self.env['walloniades.resultat.temps.niveau'].create(values)

        record.state='generated'

    def action_debug(self):
        for record in self:
            print(record.id)
            for equipe in record.equipe_instance_ids:
                print(equipe.id)
                print(equipe.name)

            for epreuve in record.epreuve_instance_ids:
                print(epreuve.id)
                print(epreuve.name)
                for resultat in epreuve.resultat_point_ids:
                    print(resultat.epreuve_instance_id.id)