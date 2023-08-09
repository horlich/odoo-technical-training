from odoo import api,fields, models
import datetime
from datetime import date, timedelta


class PropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Modul intern Offer"

    price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    status = fields.Selection(
        selection = [('a', 'Accepted'), ('r', 'Refused'), ('p', 'Pending')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for data in self:
            if (data.create_date != None):
                date_from = data.create_date
            else:
                date_from = date.today()
            data.date_deadline = date_from + timedelta(days=data.validity) 
            
    def _inverse_deadline(self):
        for data in self:
            if (data.date_deadline == None):
                continue
            if (data.create_date != None):
                date_from = data.create_date
            else:
                date_from = date.today()
            data.validity = (data.date_deadline - data.create_date.date()).days

 

