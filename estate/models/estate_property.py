from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils
import datetime
from datetime import timedelta
import logging

class PropertyModel(models.Model):
    _name = "estate.property"
    _description = "Modul intern"
    _order = "id desc"

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
    total_area = fields.Float(compute="_compute_total_area")
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
    best_price = fields.Float(compute="_compute_best_price")


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for data in self:
            data.total_area = data.living_area + data.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for data in self:
            if (len(data.offer_ids)):
                data.best_price = max(data.offer_ids.mapped("price"))
            else:
                data.best_price = 0
            

    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'n'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_cancel_pressed(self):
        if (self.state == 's'):
            raise UserError("A sold property cannot be canceled.")
        else:
            self.state = 'c'
        return True

    def action_sold_pressed(self):
        if (self.state == 'c'):
            raise UserError("A canceled property cannot be sold.")
        else:
            self.state = 's'
        return True
    
    def exists_accepted_offer(self):
        for status in self.offer_ids.mapped("status"):
            if (status == 'a'):
                return True
        return False
    
    def get_highest_offer(self):
        highest = 0.0
        for price in self.offer_ids.mapped("price"):
            if (price > highest):
                highest = price
        return highest
    
    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be positive!'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive!')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if (float_utils.float_is_zero(record.selling_price, None, 2)):
                return
            elif (record.selling_price < (record.expected_price * 0.9)):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price!")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_state(self):
        for record in self:
            if ((record.state != 'n') and (record.state != 'c')):
                raise UserError("Only properties with new oder cancelled state can be deleted."); 
