# -*- coding: utf-8 -*-

import re
import secrets
import string
from odoo.exceptions import ValidationError
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

# class devmeet(models.Model):
#     _name = 'devmeet.devmeet'
#     _description = 'devmeet.devmeet'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class developer(models.Model):
     _name = 'devmeet.developer'
     _description = 'devmeet.developer'

     name = fields.Char()
     surname = fields.Char()
     dni = fields.Char(string='DNI')
     email = fields.Char()
     photo = fields.Image(max_width=200,max_height=200)
     last_login = fields.Datetime(default=lambda d: fields.Datetime.now())

     technologies = fields.Many2many(comodel_name='devmeet.technology', relation='developers_technology',column1='developer_id',column2='technology_id')
     technologies_of_interest = fields.Many2many(comodel_name='devmeet.technology', relation='developers_technology_interest',column1='developer_id',column2='technology_id')

     events_as_speaker = fields.Many2many(comodel_name='devmeet.event', relation='developers_event', column1='developer_id', column2='event_id')
     events_as_assistant = fields.Many2many(comodel_name='devmeet.event', relation='developers_event_assistant', column1='developer_id', column2='event_id')

     
     @api.constrains('dni')
     def _check_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z',re.I) #I es IGNORECASE
        for dev in self:
            if regex.match(dev.dni):
                _logger.info('DNI correcto')
            else:
                raise ValidationError('Wrong format: DNI')

     _sql_constraints = [('dni_uniq','unique(dni)','DNI can\'t be repeated')]

     @api.constrains('email')
     def _check_email(self):
        regex = re.compile('^\w+@\w+.\w+$',re.I) #I es IGNORECASE
        for dev in self:
            if regex.match(dev.email):
                _logger.info('email correcto')
            else:
                raise ValidationError('Wrong format: email')


     #password Con lambda
     password = fields.Char(default=lambda p: secrets.token_urlsafe(12))


class technology(models.Model):
     _name = 'devmeet.technology'
     _description = 'devmeet.technology'

     name = fields.Char()
     official_page = fields.Char()
     logo = fields.Image(max_width=200,max_height=200)

     developers = fields.Many2many(comodel_name='devmeet.developer', relation='developers_technology',column1='technology_id',column2='developer_id')
     interested_developers = fields.Many2many(comodel_name='devmeet.developer', relation='developers_technology_interest',column1='technology_id',column2='developer_id')

     events = fields.Many2many(comodel_name='devmeet.event', relation='technologies_event',column1='technology_id',column2='event_id')

     _sql_constraints = [('tech_name_uniq','unique(name)','This technology is already registered')]

    
class event(models.Model):
     _name = 'devmeet.event'
     _description = 'devmeet.event'

     name = fields.Char()
     start_date = fields.Date(default=lambda d: fields.Date.today())
     end_date = fields.Date()
     type = fields.Char() #Check if it's online or not. If it's not online, it is required to register a place

     speakers = fields.Many2many(comodel_name='devmeet.developer', relation='developers_event', column1='event_id', column2='developer_id')
     assistants = fields.Many2many(comodel_name='devmeet.developer', relation='developers_event_assistant', column1='event_id', column2='developer_id')

     technologies = fields.Many2many(comodel_name='devmeet.technology', relation='technologies_event',column1='event_id',column2='technology_id')

     classroom = fields.Many2one('devmeet.classroom', ondelete='set null', help='Class where the event will be held')

     _sql_constraints = [('check_dates','check(end_date >= start_date)','End date must be at least the same day than start date')]

class classroom(models.Model):
     _name = 'devmeet.classroom'
     _description = 'devmeet.classroom'

     name = fields.Char()
     desc = fields.Char()

     events = fields.One2many(comodel_name='devmeet.event', inverse_name='classroom')

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
