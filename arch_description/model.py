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
from sqlalchemy.orm import relationship
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
        verbose_name = 'Arkivbildare'
        verbose_name_plural = 'Arkivbildare'
        list_display = ['crname']
        field_attributes = {'crname': {'name': 'Namn'}}

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
        list_display = ['creator', 'description', 'period']
        field_attributes = {'creator': {'name': 'Arkivbildare'},
                'description': {'name': 'Beskrivning (fil)'}}
        form_actions = [DescriptionReport(), LabelReport()]

class Series( Entity ):
    __tablename__ = 'series'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String, info = {'label': 'Serierubrik'})
    archive_id = Column(Integer,  ForeignKey('archives.id'))
    note = Column(String, info = {'label': u'Anmärkning'})
    archive = relationship('Archive', backref = 'series')

    def __unicode__(self):
        if self.archive is None:
            return self.signum or 'Odefinierad serie'
        else:
            return str(self.archive.creator.crname) + ':' + self.signum

    class Admin( EntityAdmin ):
        verbose_name = 'Serie'
        verbose_name_plural = 'Serier'
        list_display = ['signum', 'header', 'archive', 'note']
        field_attributes = {'header': {'name': 'Rubrik'},
                'archive': {'name': 'Arkiv'}, 'note': {'name': u'Anmärkning'}}

class Subseries( Entity ):
    __tablename__ = 'subseries'
    id = Column(Integer, primary_key = True)
    signum = Column(String)
    header = Column(String, info = {'label': 'Serierubrik'})
    series_id = Column(Integer,  ForeignKey('series.id'))
    note = Column(String)
    series = relationship('Series', backref = 'subseries')

    def __unicode__(self):
        if self.series is None:
            return self.signum or 'Odefinierad serie'
        else:
            return str(self.series.archive.creator.crname) + ':' + self.signum

    class Admin( EntityAdmin ):
        verbose_name = 'Underserie'
        verbose_name_plural = 'Underserier'
        list_display = ['signum', 'header', 'series', 'note']
        field_attributes = {'header': {'name': 'Rubrik'},
                'series': {'name': 'Serie'}, 'note': {'name': u'Anmärkning'}}

class Volume( Entity ):
    __tablename__ = 'volumes'
    volno = Column(Integer)
    subseries_id = Column(Integer, ForeignKey('subseries.id'))
    period = Column(String)
    note = Column(String)
    subseries = relationship('Subseries', backref = 'volumes')
    
    def __unicode__(self):
        return str(self.volno) or 'Odefinierad volym'
    
    class Admin( EntityAdmin ):
        verbose_name = 'Volym'
        verbose_name_plural = 'Volymer'
        list_display = ['volno', 'period', 'subseries', 'note']   
        field_attributes = {'volno': {'name': 'Volymnummer'},
                'subseries': {'name': 'Underserie'}, 'note': {'name': u'Anmärkning'}}
