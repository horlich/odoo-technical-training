from odoo import fields, models

class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Modul intern Type"

    name = fields.Char(required=True)

    