# -*- coding: utf-8 -*-
#Copyright (C) 2015 Karl Pettersson <karl_pettersson_1998@yahoo.com>
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License version 2
#as published by the Free Software Foundation (and included in the file
#LICENSE along with this program).
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
import sqlalchemy.types
from sqlalchemy.types import *
    
from camelot.admin.entity_admin import EntityAdmin
from camelot.core.orm import Entity
from camelot.types import File

class Creator( Entity ):
    __tablename__ = 'creators'
    id = Column(Integer, primary_key = True)
    crname = Column(String, info = {'label': 'Namn'})

    def __unicode__(self):
        return self.crname or 'Ej namngiven arkivbildare'

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = 'Arkivbildare'
        verbose_name_plural = 'Arkivbildare'
        list_display = ['crname']
        field_attributes = {'crname': {'name': 'Namn'}}
        form_actions = [DescriptionReport(), LabelReport()]

class Archive( Entity ):
    __tablename__ = 'archives'
    id = Column(Integer, primary_key = True)
    creator_id = Column(Integer, ForeignKey('creators.id'))
    description = Column(File)
    period = Column(String)
    creator = relationship('Creator', backref = 'archives')

    def __unicode__(self):
        if self.creator is None:
            return str(self.id) or 'Odefinierat arkiv'
        else:
            return self.creator.crname

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = 'Arkiv'
        verbose_name_plural = 'Arkiv'
        list_display = ['creator', 'description', 'period', 'series']
        field_attributes = {'creator': {'name': 'Arkivbildare'},
                'description': {'name': 'Beskrivning (fil)'},
                'series': {'name': 'Serier'}}
        form_actions = [DescriptionReport(), LabelReport()]

class ArchObject( Entity ):
    __tablename__ = 'arch_objects'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String)
    processes = Column(String)
    preserve = Column(String)
    classified = Column(String)
    note = Column(String)
    creator_id = Column(Integer, ForeignKey('creators.id'))
    creator = relationship('Creator', backref = 'arch_objects')

    def __unicode__(self):
        if self.signum is None:
            return str(self.id) or u'Odefinierat objekt'
        else:
            return self.signum

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = u'Objekt'
        verbose_name_plural = u'Objekt'
        list_display = ['creator', 'signum', 'header', 'processes', 'preserve', 
                'classified', 'note', 'storage_units']
        field_attributes = {
                'creator': {'name': 'Arkivbildare'},
                'processes': {'name': 'Tillkomstprocesser'},
                'preserve': {'name': 'Bevarande'},
                'signum': {'name': 'Objektsbeteckning'},
                'header': {'name': 'Handlingsgrupp'},
                'classified': {'name': 'Sekretess'},
                'note': {'name': 'Kommentar'},
                'storage_units': {'name': u'Förvaringsenheter'}}
 
class Division( Entity ):
    __tablename__ = 'divisions'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String)
    creator_id = Column(Integer, ForeignKey('creators.id'))
    creator = relationship('Creator', backref = 'divisions')

    def __unicode__(self):
        if self.header is None:
            return str(self.id) or u'Odefinierat område'
        else:
            return self.header

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = u'Verksamhetsområde'
        verbose_name_plural = u'Verksamhetsområden'
        list_display = ['creator', 'signum', 'header', 'processes']
        field_attributes = {'creator': {'name': 'Arkivbildare'},
                'signum': {'name': 'Signum'},
                'header': {'name': 'Namn'},
                'processes': {'name': 'Processer'}}

class Procgroup( Entity ):
    __tablename__ = 'procgroups'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String)
    creator_id = Column(Integer, ForeignKey('creators.id'))
    creator = relationship('Creator', backref = 'procgroups')

    def __unicode__(self):
        if self.creator is None:
            return str(self.id) or u'Odefinierad grupp'
        else:
            return self.creator.crname

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = u'Processgrupp'
        verbose_name_plural = u'Processgrupper'
        list_display = ['creator', 'signum', 'header', 'processes']
        field_attributes = {'creator': {'name': 'Arkivbildare'},
                'signum': {'name': 'Signum'},
                'header': {'name': 'Namn'},
                'processes': {'name': 'Processer'}}

class Process( Entity ):
    __tablename__ = 'processes'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String)
    acts = Column(String)
    acts_separate = Column(String)
    classified = Column(String)
    note = Column(String)
    division_id = Column(Integer, ForeignKey('divisions.id'))
    procgroup_id = Column(Integer, ForeignKey('procgroups.id'))
    division = relationship('Division', backref = 'processes')
    procgroup = relationship('Procgroup', backref = 'processes')

    def __unicode__(self):
        if self.header is None:
            return str(self.id) or u'Odefinierad process'
        else:
            return self.header

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = u'Process'
        verbose_name_plural = u'Processer'
        list_display = ['division', 'procgroup', 'signum', 'header', 
                'acts', 'acts_separate', 'classified', 'note',
                'acttypes', 'storage_units']
        field_attributes = {
                'division': {'name': u'Verksamhetsområde'},
                'procgroup': {'name': u'Processgroup'},
                'signum': {'name': 'Processbeteckning'},
                'header': {'name': 'Processnamn'},
                'acts': {'name': 'Handlingar'},
                'acts_separate': {'name': 'Handlingar (redovisas separat)'},
                'classified': {'name': 'Sekretess'},
                'note': {'name': 'Kommentar'},
                'acttypes': {'name': 'Handlingstyper'},
                'storage_units': {'name': u'Förvaringsenheter'}}
 
class Acttype( Entity ):
    __tablename__ = 'acttypes'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String)
    classified = Column(String)
    note = Column(String)
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship('Process', backref = 'acttypes')

    def __unicode__(self):
        if self.header is None:
            return str(self.id) or u'Odefinierad handlingstyp'
        else:
            return self.header

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = u'Handlingstyp'
        verbose_name_plural = u'Handlingstyper'
        list_display = ['process', 'signum', 'header', 'classified', 'note',
                'storage_units']
        field_attributes = {'process': {'name': u'Process'},
                'signum': {'name': 'Typbeteckning'},
                'header': {'name': 'Typer'},
                'note': {'name': 'Kommentar'},
                'storage_units': {'name': u'Förvaringsenheter'}}   
 
class StorageUnit( Entity ):
    __tablename__ = 'storage_units'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    extent = Column(String)
    medium = Column(String)
    unittype = Column(String)
    place = Column(String)
    note = Column(String)
    process_id = Column(Integer, ForeignKey('processes.id'))
    process = relationship('Process', backref = 'storage_units')
    acttype_id = Column(Integer, ForeignKey('acttypes.id'))
    acttype = relationship('Acttype', backref = 'storage_units')
    arch_object_id = Column(Integer, ForeignKey('arch_objects.id'))
    arch_object = relationship('ArchObject', backref = 'storage_units')

    def __unicode__(self):
        if self.creator is None:
            return str(self.id) or u'Odefinierad förvaringsenhet'
        else:
            return self.signum

    class Admin( EntityAdmin ):
        from arch_description.reports import DescriptionReport, LabelReport
        verbose_name = u'Förvaringsenhet'
        verbose_name_plural = u'Förvaringsenheter'
        list_display = ['signum', 'extent', 'medium', 'unittype',
                'place', 'note']
        field_attributes = {
                'signum': {'name': u'Förvarings-id'},
                'extent': {'name': 'Omfattning'},
                'medium': {'name': 'Media'},
                'unittype': {'name': u'Förvaringsenhet'},
                'place': {'name': 'Placering'},
                'note': {'name': 'Kommentar'},
                }   


class Series( Entity ):
    __tablename__ = 'series'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String, info = {'label': 'Serierubrik'})
    archive_id = Column(Integer,  ForeignKey('archives.id'))
    parent_series_id = Column(Integer, ForeignKey('series.id'))
    note = Column(String, info = {'label': u'Anmärkning'})
    archive = relationship('Archive', backref = 'series')
    child_series = relationship('Series', 
            backref = backref('parent_series', remote_side = [id]))

    def __unicode__(self):
        if self.archive is None:
            return self.signum or 'Odefinierad serie'
        else:
            return str(self.archive.creator.crname) + ':' + self.signum

    class Admin( EntityAdmin ):
        verbose_name = 'Serie'
        verbose_name_plural = 'Serier'
        list_display = ['signum', 'header', 'archive', 'note', 
                'child_series', 'volumes', 'parent_series']
        field_attributes = {'header': {'name': 'Rubrik'},
                'archive': {'name': 'Arkiv'}, 'note': {'name': u'Anmärkning'},
                'child_series': {'name': 'Underserier'},
                'parent_series': {'name': u'Överserie'},
                'volumes': {'name': 'Volymer'}}

class Volume( Entity ):
    __tablename__ = 'volumes'
    volno = Column(Integer)
    series_id = Column(Integer, ForeignKey('series.id'))
    period = Column(String)
    note = Column(String)
    series = relationship('Series', backref = 'volumes')
    
    def __unicode__(self):
        return str(self.volno) or 'Odefinierad volym'
    
    class Admin( EntityAdmin ):
        verbose_name = 'Volym'
        verbose_name_plural = 'Volymer'
        list_display = ['volno', 'period', 'series', 'note']   
        field_attributes = {'volno': {'name': 'Volymnummer'},
                'series': {'name': 'Serie'}, 'note': {'name': u'Anmärkning'}}
