from odoo import fields, models, api


class WalloniadesTypeEpreuve(models.Model):
    _name = "walloniades.type.epreuve"
    _description = "Les différents type d'épreuves d'une Walloniade"
    
    '''_order = "sequence asc, name asc"'''
    

    name = fields.Char('Type d''épreuve', required=True)




    '''
    properties_ids = fields.One2many("estate.property", "property_type_id", string = "Properties related to type")
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower will appear on top.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string = "Offers related to type")
    offer_count = fields.Integer('Number of related offers',compute="_compute_offer_count")

    _sql_constraints = [
        ('name_uniq', 'unique(name)',
         'A property type with the same name already exists !')

    ]

    @api.depends ("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids.mapped('price'))
    '''
           