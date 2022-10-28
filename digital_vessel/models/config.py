# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Vessel(models.Model):
    _name = 'vessel.vessel'
    
    name = fields.Char(string="Vessel Name")


class Scope(models.Model):
    _name = 'scope.scope'
    
    name = fields.Char(string="Scope Name")

class WorkingArea(models.Model):
    _name = 'working.area'
    
    name = fields.Char(string="Working Area")

class Technician(models.Model):
    _name = 'technician.technician'
    
    name = fields.Char(string="Technician Name")

class Customer(models.Model):
    _name = 'customer.customer'
    
    name = fields.Char(string="Customer Name")

class Component(models.Model):
    _name = 'component.component'
    
    name = fields.Char(string="Part / Component")
    uom_id = fields.Many2one('uom.uom', string='UOM')
    pm_id = fields.Many2one('preventive.maintenance', string="PM")

class Location(models.Model):
    _name = 'location.location'
    
    name = fields.Char(string="Location Name")

class Captain(models.Model):
    _name = 'captain.captain'
    
    name = fields.Char(string="Captain Name")

class JobCode(models.Model):
    _name = 'job.code'

    name = fields.Char(string ='Job Code')
    code = fields.Char(string ='Uraian')
    uom_id = fields.Many2one('uom.uom', string='Volume')

class Dock(models.Model):
    _name = 'dock.dock'
    
    name = fields.Char(string="Dock Name")

class Kamarmesin(models.Model):
    _name = 'kamar.mesin'
    
    name = fields.Char(string="Kamar Mesin")

class SubSectionLine(models.Model):
    _name = 'sub.section.line'
    
    section_id = fields.Many2one('section.section', string="section_id", required=True)
    name = fields.Char(string="Sub section")

class SectionSection(models.Model):
    _name = 'section.section'
    
    name = fields.Char(string="Section")
    sub_section_ids = fields.One2many('sub.section.line', 'section_id',  string="section line")

class Deck(models.Model):
    _name = 'deck.deck'
    
    name = fields.Char(string="deck")

class Wheelhouse(models.Model):
    _name = 'wheel.house'
    
    name = fields.Char(string="Wheel House")