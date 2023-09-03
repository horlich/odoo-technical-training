from odoo import fields, models

class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Modul intern Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Sequence Help Text")

    property_ids = fields.One2many('estate.property', 'property_type_id')

    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'Type name exists already!')
    ]

    