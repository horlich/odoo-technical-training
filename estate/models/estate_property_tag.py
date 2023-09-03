from odoo import fields, models

class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Modul intern Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'This tag name exists already!')
    ]

    