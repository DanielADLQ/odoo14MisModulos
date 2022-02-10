# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'

    name = fields.Char(string="Nombre",readonly=False,required=True,help="Este es el nombre")
    birth_year = fields.Integer()
    description = fields.Text()
    inscription_date = fields.Date()
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200,max_height=200)

    classroom = fields.Many2one('school.classroom', ondelete='set null', help='Clase a la que pertenece') #Muchos studiantes en una clase
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)

class classroom(models.Model):
    _name = 'school.classroom'
    _descripcion = "Las clases"

    name = fields.Char()
    students = fields.One2many(string="Alumnos", comodel_name='school.student', inverse_name='classroom') #1 clase, muchos estudiantes. Classroom es la clave ajena de la relacion

    teachers = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom', column1='classroom_id', column2='teacher_id')
    teachers_last_year = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom_ly', column1='classroom_id', column2='teacher_id') #Ejemplo para ver que se pueden establecer mas relaciones entre las mismas tablas

#profesor puede ir a muchas clases y clase puede tener muchos profesores

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
