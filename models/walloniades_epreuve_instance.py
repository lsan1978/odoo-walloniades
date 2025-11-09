from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError , ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.float_utils import float_is_zero

class WalloniadesEpreuveInstance(models.Model):
    _name = "walloniades.epreuve.instance"
    _description = "Une épreuve d'une édition des walloniades"
    _order = "sequence asc"
    

    
    epreuve_id = fields.Many2one("walloniades.epreuve", required=True)
    walloniade_id = fields.Many2one("walloniades.walloniade", required=True, ondelete='cascade')
    name = fields.Char(related='epreuve_id.name', store=True)
    type_epreuve_id = fields.Many2one(related='epreuve_id.type_epreuve_id', store=True)
    resultat_point_ids = fields.One2many("walloniades.resultat.point", "epreuve_instance_id")
    resultat_temps_penalite_ids = fields.One2many("walloniades.resultat.temps.penalite", "epreuve_instance_id")
    resultat_temps_positif_negatif_ids = fields.One2many("walloniades.resultat.temps.positif.negatif", "epreuve_instance_id")
    resultat_temps_niveau_ids = fields.One2many("walloniades.resultat.temps.niveau", "epreuve_instance_id")
    sequence = fields.Integer('Sequence', default=1)
    classement_line_ids = fields.One2many("walloniades.classement.line", "epreuve_instance_id")
    temps_de_penalite = fields.Float("Temps de pénalité (en secondes)", default=5)
    type_epreuve_name = fields.Char(related="type_epreuve_id.name",store=True)
    

    


    def action_compute_classement(self):
        for record in self:
            if (record.resultat_point_ids):
                resultats = record.resultat_point_ids.filtered(lambda r: r.points_set)
                resultats_trie = resultats.sorted(key=lambda r: r.points, reverse=True)
                for ligne in record.walloniade_id.classement_line_ids:
                    if (ligne.epreuve_instance_id == record):
                        ligne.unlink()
                i=1
                j=1
                
                for res in resultats_trie:
                    if (i==1):
                        values = {
                                'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                'equipe_instance_id' : res.equipe_instance_id.id,
                                'walloniade_id' : res.walloniade_id.id,
                                'position' : i,
                                'points' : res.points,
                                }
                        self.env['walloniades.classement.line'].create(values)
                        previous_points = res.points
                        #res.equipe_instance_id.nbre_victoire = res.equipe_instance_id.nbre_victoire + 1
                    else:
                        if (res.points==previous_points):
            
                            values = {
                                    'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                    'equipe_instance_id' : res.equipe_instance_id.id,
                                    'walloniade_id' : res.walloniade_id.id,
                                    'position' : j,
                                    'points' : res.points,
                                    }
                            self.env['walloniades.classement.line'].create(values)
                            
                        else:
                            
                            values = {
                                    'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                    'equipe_instance_id' : res.equipe_instance_id.id,
                                    'walloniade_id' : res.walloniade_id.id,
                                    'position' : i,
                                    'points' : res.points,
                                    }
                            self.env['walloniades.classement.line'].create(values)
                            previous_points = res.points
                            j=i
                    i=i+1        

            if (record.resultat_temps_penalite_ids):
                resultats = record.resultat_temps_penalite_ids.filtered(lambda r: r.reso_set)
                temp_resultats = []
                for res in resultats:

                    if (float_is_zero(res.temps_total_secondes,2)):
                        temps = 600
                    else:
                        temps = res.temps_total_secondes
                    temp_resultats.append((res, temps))

                resultats_trie = sorted(temp_resultats, key=lambda x: x[1])

                for ligne in record.walloniade_id.classement_line_ids:
                    if (ligne.epreuve_instance_id == record):
                        ligne.unlink()
                i=1
                j=1
                
                for res, tps in resultats_trie:
                
                    
                    if (i==1):
                        values = {
                                'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                'equipe_instance_id' : res.equipe_instance_id.id,
                                'walloniade_id' : res.walloniade_id.id,
                                'position' : i,
                                'temps_final_string' : res.temps_final_char,
                                }
                        self.env['walloniades.classement.line'].create(values)
                        previous_temps_total_secondes = res.temps_total_secondes
                    else:
                        
                        if (float_compare(res.temps_total_secondes, previous_temps_total_secondes, precision_digits=2)==0):
            
                            values = {
                                    'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                    'equipe_instance_id' : res.equipe_instance_id.id,
                                    'walloniade_id' : res.walloniade_id.id,
                                    'position' : j,
                                    'temps_final_string' : res.temps_final_char,
                                    }
                            self.env['walloniades.classement.line'].create(values)
                            
                        else:
                            
                            values = {
                                    'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                    'equipe_instance_id' : res.equipe_instance_id.id,
                                    'walloniade_id' : res.walloniade_id.id,
                                    'position' : i,
                                    'temps_final_string' : res.temps_final_char,
                                    }
                            self.env['walloniades.classement.line'].create(values)
                            previous_temps_total_secondes = res.temps_total_secondes
                            j=i
                    i=i+1
                          
            if (record.resultat_temps_positif_negatif_ids):
                resultats = record.resultat_temps_positif_negatif_ids.filtered(lambda r: r.reso_set)
                
                temps_positifs = []
                for res in resultats:
                    if (res.est_negatif == False):
                        temps_positifs.append((res, res.secondes))
                temps_positifs_trie = sorted(temps_positifs, key=lambda x: x[1])
                        

                temps_negatifs = []
                for res in resultats:
                    if (res.est_negatif == True):
                        temps_negatifs.append((res, res.secondes))
                temps_negatifs_trie = sorted(temps_negatifs, key=lambda x: -x[1])

                resultat_trie = []
                for resul, sec in temps_positifs_trie:
                    resultat_trie.append((resul,sec))
                for resul, sec in temps_negatifs_trie:
                    resultat_trie.append((resul,sec))

                for ligne in record.walloniade_id.classement_line_ids:
                    if (ligne.epreuve_instance_id == record):
                        ligne.unlink()
                i=1
                j=1
                
                for res, tps in resultat_trie:
                
                    
                    if (i==1):
                        values = {
                                'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                'equipe_instance_id' : res.equipe_instance_id.id,
                                'walloniade_id' : res.walloniade_id.id,
                                'position' : i,
                                'temps_final_string' : res.temps_final_char,
                                }
                        self.env['walloniades.classement.line'].create(values)
                        previous_temps_total_secondes = res.secondes
                        previous_temps_brut = res.temps_brut
                    else:
                        
                        if (float_compare(res.secondes, previous_temps_total_secondes, precision_digits=2)==0 and float_compare(res.temps_brut, previous_temps_brut, precision_digits=2)==0):
            
                            values = {
                                    'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                    'equipe_instance_id' : res.equipe_instance_id.id,
                                    'walloniade_id' : res.walloniade_id.id,
                                    'position' : j,
                                    'temps_final_string' : res.temps_final_char,
                                    }
                            self.env['walloniades.classement.line'].create(values)
                            
                        else:
                            
                            values = {
                                    'epreuve_instance_id' : res.epreuve_instance_id._origin.id,
                                    'equipe_instance_id' : res.equipe_instance_id.id,
                                    'walloniade_id' : res.walloniade_id.id,
                                    'position' : i,
                                    'temps_final_string' : res.temps_final_char,
                                    }
                            self.env['walloniades.classement.line'].create(values)
                            previous_temps_total_secondes = res.secondes
                            previous_temps_brut = res.temps_brut
                            j=i
                    i=i+1

                  
                


            if (record.resultat_temps_niveau_ids):
                
                resultats = record.resultat_temps_niveau_ids.filtered(lambda r: r.reso_set)
                #resultats_trie = resultats.sorted(key=lambda r: (r.secondes, -r.niveau))
                temp_resultat = []
                for res in resultats:
                    if (res.niveau or res.temps_brut):
                        if (res.niveau):
                            sec = 600.00
                            niv = res.niveau
                        else :
                            sec = res.secondes
                            niv = 10
                        
                    else:
                        sec = 650.00
                        niv = -1
                    temp_resultat.append((res,sec,niv))

                    
                resultat_trie = sorted(temp_resultat, key=lambda x: (x[1],-x[2]))
                for ligne in record.walloniade_id.classement_line_ids:
                    if (ligne.epreuve_instance_id == record):
                        ligne.unlink()
                i=1
                j=1

                for reso,seco,nivo in resultat_trie:
                    
                    if (i==1):

                        if (float_compare(seco, 600.00, precision_digits=2)<0):
                            
                            values = {
                                'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                'equipe_instance_id' : reso.equipe_instance_id.id,
                                'walloniade_id' : reso.walloniade_id.id,
                                'position' : i,
                                'temps_final_string' : reso.temps_final_char,
                                }
                            self.env['walloniades.classement.line'].create(values)
                            previous_temps = reso.secondes
                            previous_niveau=-1

                        elif (float_compare(seco, 600.00, precision_digits=2)==0):
                            values = {
                                'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                'equipe_instance_id' : reso.equipe_instance_id.id,
                                'walloniade_id' : reso.walloniade_id.id,
                                'position' : i,
                                'temps_final_string' : f"{reso.niveau:02d}",
                                }
                            self.env['walloniades.classement.line'].create(values)
                            previous_niveau = reso.niveau
                        else:
                            values = {
                                'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                'equipe_instance_id' : reso.equipe_instance_id.id,
                                'walloniade_id' : reso.walloniade_id.id,
                                'position' : i,
                                'temps_final_string' : reso.temps_final_char,
                                }
                            self.env['walloniades.classement.line'].create(values)
                            previous_temps = reso.secondes
                            previous_niveau=-1
                        i=i+1

                    else:
                    
                        if (float_compare(seco, 600.00, precision_digits=2)<0):

                            if (float_compare(reso.secondes, previous_temps, precision_digits=2)==0):
            
                                values = {
                                        'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                        'equipe_instance_id' : reso.equipe_instance_id.id,
                                        'walloniade_id' : reso.walloniade_id.id,
                                        'position' : j,
                                        'temps_final_string' : reso.temps_final_char,
                                    }
                                self.env['walloniades.classement.line'].create(values)
                            
                            else:
                            
                                values = {
                                        'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                        'equipe_instance_id' : reso.equipe_instance_id.id,
                                        'walloniade_id' : reso.walloniade_id.id,
                                        'position' : i,
                                        'temps_final_string' : reso.temps_final_char,
                                        }
                                self.env['walloniades.classement.line'].create(values)
                                previous_temps = reso.secondes
                                j=i
                            i=i+1
                        elif (float_compare(seco, 600.00, precision_digits=2)==0):

                            if (previous_niveau!=-1):

                                if (nivo==previous_niveau):

                                    values = {
                                        'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                        'equipe_instance_id' : reso.equipe_instance_id.id,
                                        'walloniade_id' : reso.walloniade_id.id,
                                        'position' : j,
                                        'temps_final_string' : f"{reso.niveau:02d}",
                                    }
                                    self.env['walloniades.classement.line'].create(values)
                                
                                else:
                                    values = {
                                        'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                        'equipe_instance_id' : reso.equipe_instance_id.id,
                                        'walloniade_id' : reso.walloniade_id.id,
                                        'position' : i,
                                        'temps_final_string' : f"{reso.niveau:02d}",
                                        }
                                    self.env['walloniades.classement.line'].create(values)
                                    previous_niveau = reso.niveau
                                    j=i
                                i=i+1    
                            else:
                                values = {
                                        'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                        'equipe_instance_id' : reso.equipe_instance_id.id,
                                        'walloniade_id' : reso.walloniade_id.id,
                                        'position' : i,
                                        'temps_final_string' : f"{reso.niveau:02d}",
                                        }
                                self.env['walloniades.classement.line'].create(values)
                                previous_niveau = reso.niveau
                                j=i
                                i=i+1
                        else:
                            j=i
                            values = {
                                        'epreuve_instance_id' : reso.epreuve_instance_id._origin.id,
                                        'equipe_instance_id' : reso.equipe_instance_id.id,
                                        'walloniade_id' : reso.walloniade_id.id,
                                        'position' : j,
                                        'temps_final_string' : reso.temps_final_char,
                                    }
                            self.env['walloniades.classement.line'].create(values)

                            
                            
    def action_compute_classement_general(self):
        for record in self:
            for ligne in record.walloniade_id.classement_general_line_ids:
                    ligne.unlink()
            lignes_de_classement = record.walloniade_id.classement_line_ids
            if (len(lignes_de_classement)!=0):

                points_par_equipe = {}
                nbre_premiere_place_par_equipe = {}
                nbre_seconde_place_par_equipe = {}
                nbre_troisieme_place_par_equipe = {}

                for line in lignes_de_classement:
                    equipe = line.equipe_instance_id
                    points_par_equipe[equipe] = points_par_equipe.get(equipe, 0) + line.position
                    if (line.position==1):
                        nbre_premiere_place_par_equipe[equipe] = nbre_premiere_place_par_equipe.get(equipe, 0) + 1
                    if (line.position==2):
                        nbre_seconde_place_par_equipe[equipe] = nbre_seconde_place_par_equipe.get(equipe, 0) + 1
                    if (line.position==3):
                        nbre_troisieme_place_par_equipe[equipe] = nbre_troisieme_place_par_equipe.get(equipe, 0) + 1


                for equipe, pts in points_par_equipe.items():
                    values = {
                        'equipe_instance_id': equipe.id,
                        'walloniade_id': equipe.walloniade_id.id,
                        'points': pts,
                        'nbre_victoire' : nbre_premiere_place_par_equipe.get(equipe, 0),
                        'nbre_seconde_place' : nbre_seconde_place_par_equipe.get(equipe, 0),
                        'nbre_troisieme_place' : nbre_troisieme_place_par_equipe.get(equipe, 0)

                    }
                    self.env['walloniades.classement.general.line'].create(values)

                

                lignes_classement_general=record.walloniade_id.classement_general_line_ids
                lignes_classement_general_trie = lignes_classement_general.sorted(key=lambda r: (r.points, -r.nbre_victoire, -r.nbre_seconde_place, -r.nbre_troisieme_place))
                i=1
                j=1
                for line in lignes_classement_general_trie:
                    if (i==1):
                        line.position = i
                        previous_points = line.points
                        previous_nbre_victoire = line.nbre_victoire
                        previous_nbre_seconde_place = line.nbre_seconde_place
                        previous_nbre_troisieme_place = line.nbre_troisieme_place
                        i=i+1
                        
                    else:
                        if (line.points == previous_points and line.nbre_victoire == previous_nbre_victoire and line.nbre_seconde_place == previous_nbre_seconde_place and line.nbre_troisieme_place == previous_nbre_troisieme_place):
                            line.position = j
                            
                        else:
                            j=i
                            line.position = j
                            previous_points = line.points
                            previous_nbre_victoire = line.nbre_victoire
                            previous_nbre_seconde_place = line.nbre_seconde_place
                            previous_nbre_troisieme_place = line.nbre_troisieme_place
                        i=i+1
            else:

                raise UserError("Aucun classement d'épreuve n'est présent. Il n'est pas possible  de calculer un classement général de la Walloniade.")

            
                    


                    
                   
                


    
