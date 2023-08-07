from odoo import fields, models

class PropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Modul intern Offer"

    price = fields.Float()
    status = fields.Selection(
        selection = [('a', 'Accepted'), ('r', 'Refused'), ('p', 'Pending')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    