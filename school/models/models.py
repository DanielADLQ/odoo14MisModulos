# -*- coding: utf-8 -*-

from email.policy import default
import logging
import string
from odoo import models, fields, api

from odoo import _
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError
import logging
import re

import secrets

_logger = logging.getLogger(__name__)

class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'

    name = fields.Char(string="Nombre",readonly=False,required=True,help="Este es el nombre")
    birth_year = fields.Integer()

    dni = fields.Char(string='DNI')

    #password = fields.Char(compute='_get_password', store=True) #campo calculado
    #store=True para que solo se calcule cuando le diga
    

    #def _get_password(self):
    #    password = secrets.token_urlsafe(12)
    #    #_logger.debug()
    #    return password

    #password = fields.Char(default = _get_password) #Aqui el metodo va sin comillas
    
    #password Con lambda
    password = fields.Char(default=lambda p: secrets.token_urlsafe(12))

    description = fields.Text()
    inscription_date = fields.Date(default=lambda d: fields.Date.today())
    last_login = fields.Datetime(default=lambda d: fields.Datetime.now()) #lambda es necesario para que se cargue CADA VEZ que entra un alumno
        #sin lambda lo haria solo la primera vez en odoo, cuando arrancamos el servicio
    
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200,max_height=200)

    classroom = fields.Many2one('school.classroom', ondelete='set null', help='Clase a la que pertenece') #Muchos studiantes en una clase
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)

    @api.constrains('dni')
    def _check_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z',re.I) #I es IGNORECASE
        for student in self:
            if regex.match(student.dni):
                _logger.info('DNI correcto')
            else:
                raise ValidationError('Formato incorrecto: DNI')

    _sql_constraints = [('dni_uniq','unique(dni)','DNI can\'t be repeated')]


    #@api.one para recibir solo un estudiante, si no pones nada recibe una lista
    @api.depends('name') #Ocurrira al cambiar el nombre
    def _get_password(self):
        print(self)

        for student in self:
            student.password = secrets.token_urlsafe(12) #contraseña aleatoria
            #Aqui print de colores para ayudar a buscar mensajes
            #raise Warning(_("Se ha producido un Warning")) #SACAR WARNINGS
            #print(student)
            _logger.debug("Cambiado")
            #_logger.warning("Cambiado")

class classroom(models.Model):
    _name = 'school.classroom'
    _descripcion = "Las clases"

    name = fields.Char()
    students = fields.One2many(string="Alumnos", comodel_name='school.student', inverse_name='classroom') #1 clase, muchos estudiantes. Classroom es la clave ajena de la relacion

    teachers = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom', column1='classroom_id', column2='teacher_id')
    #profesor puede ir a muchas clases y clase puede tener muchos profesores

    teachers_last_year = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom_ly', column1='classroom_id', column2='teacher_id') #Ejemplo para ver que se pueden establecer mas relaciones entre las mismas tablas

    coordinator = fields.Many2one('school.teacher',compute='_get_coordinator') #Muchas clases pueden tener de coordinador a un mismo profesor
    all_teachers = fields.Many2many('school.teacher', compute='_get_allteachers')

    def _get_coordinator(self): #Pone como coordinator al primer profesor de la lista teachers de la clase
        for classroom in self:
            if len(classroom.teachers) > 0:
                classroom.coordinator = classroom.teachers[0].id
            else:
                classroom.coordinator = None

    def _get_allteachers(self):
        for classroom in self:
            classroom.all_teachers = classroom.teachers + classroom.teachers_last_year


class teacher(models.Model):
    _name = 'school.teacher'
    _descripcion = "Los profesores"

    name = fields.Char()

    classrooms = fields.Many2many(comodel_name='school.classroom', relation='teachers_classroom', column1='teacher_id', column2='classroom_id')
    classrooms_last_year = fields.Many2many(comodel_name='school.classroom', relation='teachers_classroom_ly', column1='teacher_id', column2='classroom_id')

# class school(models.Model):
#     _name = 'school.school'
#     _description = 'school.school'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
