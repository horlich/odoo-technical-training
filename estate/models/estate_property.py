from odoo import fields, models
import datetime
from datetime import timedelta

class PropertyModel(models.Model):
    _name = "estate.property"
    _description = "Modul intern"

    name = fields.Char(required=True, string='Title')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: (fields.Date.today() + datetime.timedelta(90)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('n', "North"), ('s', "South"), ('e', "East"), ('w', "West")]
    )
    state = fields.Selection(
        selection = [('n', "New"), ('r', "Offer Received"), ('a', "Offer Accepted"), ('s', "Sold"), ('c', "Cancelled")],
        default = 'n'
    )
    active = fields.Boolean(default=True)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    