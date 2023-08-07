from odoo import fields, models

class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Modul intern Tag"

    name = fields.Char(required=True)

    