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

from camelot.admin.action import Action
from camelot.view.art import Icon
from camelot.admin.object_admin import ObjectAdmin
from camelot.core.utils import ugettext_lazy as _
from camelot.core.conf import settings
from camelot.view.action_steps import ( SelectFile, ChangeObject )
from jinja2 import Environment, FileSystemLoader
from arch_description.paths import maindir, templdir
import os
import sys
import natsort
from operator import attrgetter

def outformat_options(outformat, templname):
    u"""Inställningar för filformat för rapporter"""
    if outformat == 'docx':
        pdoc_writer = 'docx'
        templsetting = 'reference-docx'
        templfullname = os.path.join(templdir, templname + '.docx')
        filefilter = 'Word-dokument (*.docx);;Alla (*.*)'
    elif outformat == 'pdf':
        pdoc_writer = 'latex'
        templsetting = 'template'
        templfullname = os.path.join(templdir, templname + '.tex')
        filefilter = 'PDF-dokument (*.pdf);;Alla (*.*)'
    elif outformat == 'latex':
        pdoc_writer = 'latex'
        templsetting = 'template'
        templfullname = os.path.join(templdir, templname + '.tex')
        filefilter = 'LaTeX (*.tex);;Alla (*.*)'
    return {'pdoc_writer': pdoc_writer, 'templsetting': templsetting,
            'templfullname': templfullname, 'filefilter': filefilter}

def convert_report(templsetting, templfullname, reportsrc,
        report_fullfilename, pdoc_writer, pdoc_extra_args = []):
    u"""Inställningar för generering av rapporter via Pandoc"""
    import pypandoc
    pdoc_args = (['--smart', '--standalone', '--latex-engine=xelatex', 
            '--columns=60', '--' + templsetting + '=' + templfullname,
            '--latex-engine-opt=-include-directory=' + templdir] + 
            pdoc_extra_args)
    pypandoc.convert(reportsrc, pdoc_writer, format = 'md', 
    outputfile = report_fullfilename, extra_args = pdoc_args)
    if (sys.platform == 'win32' and pdoc_writer == 'docx' and '--toc' in pdoc_args):
        import subprocess
        tocscript = os.path.join(maindir, 'toc16.vbs')
        subprocess.Popen(['wscript', tocscript, report_fullfilename])

class DescriptionReport( Action ):
    u"""Förteckning (inklusive arkivbeskrivning) för arkiv med allmänna arkivschemat"""
    verbose_name = _(u'Spara förteckning')
    icon = Icon('tango/22x22/mimetypes/x-office-document.png')
    
    def model_run( self, model_context ):
        objclass = model_context.get_object().__class__.__name__
        if objclass == 'Archive':
            templname = 'description'
        elif objclass == 'Creator':
            templname = 'procreport'
        outoptions = OutputOptions()
        yield ChangeObject( outoptions )
        outformat = outoptions.outformat
        of_opt = outformat_options(outformat, templname)
        select_report_file = SelectFile( of_opt['filefilter'] )
        select_report_file.existing = False
        report_filename = (yield select_report_file)[0]

        report_fullfilename = addext(report_filename, outformat)
        fileloader = FileSystemLoader(templdir)
        env = Environment(loader=fileloader)
        reporttempl = env.get_template(templname + '.md')
        logo = os.path.join(templdir, "logo")
        if objclass == 'Archive':
            archive = model_context.get_object()
            serlist = natsort.natsorted(archive.series, key=lambda ser: ser.signum)
            descpath = os.path.join(settings.CAMELOT_MEDIA_ROOT(), archive.description.name)
            with open(descpath) as descfile:
                description = unicode(descfile.read(), 'utf-8')
            reportsrc = reporttempl.render(archive = archive, serlist = serlist,
                    description = description, logo = logo)
        elif objclass == 'Creator':
            creator = model_context.get_object()
            objlist = natsort.natsorted(creator.arch_objects, key=lambda obj: obj.signum)
            divlist = natsort.natsorted(creator.divisions, key=lambda div: div.signum)
            reportsrc = reporttempl.render(creator = creator, 
                    objlist = objlist, divlist = divlist, logo = logo)

        convert_report(of_opt['templsetting'], of_opt['templfullname'], reportsrc,
                report_fullfilename, of_opt['pdoc_writer'], ['--toc'])

class ShippingReport( Action ):
    u"""Leveransreversal"""
    verbose_name = _(u'Spara leveransreversal')
    icon = Icon('tango/22x22/mimetypes/x-office-document.png')
    
    def model_run( self, model_context ):
        templname = 'shipreport'
        outoptions = OutputOptions()
        yield ChangeObject( outoptions )
        outformat = outoptions.outformat
        of_opt = outformat_options(outformat, templname)
        select_report_file = SelectFile( of_opt['filefilter'] )
        select_report_file.existing = False
        report_filename = (yield select_report_file)[0]

        report_fullfilename = addext(report_filename, outformat)
        fileloader = FileSystemLoader(templdir)
        env = Environment(loader=fileloader)
        reporttempl = env.get_template(templname + '.md')
        archive = model_context.get_object()
        archive.voltot = 0
        serlist = natsort.natsorted(archive.series, key=lambda ser: ser.signum)
        for series in serlist:
            if series.volumes:
                series.voltot = max(vol.volno for vol in series.volumes)
                archive.voltot = archive.voltot + series.voltot
        reportsrc = reporttempl.render(archive = archive, serlist = serlist)

        convert_report(of_opt['templsetting'], of_opt['templfullname'], reportsrc,
                report_fullfilename, of_opt['pdoc_writer'])

class ProcdescReport( Action ):
    u"""Bevarandeförteckning för arkiv med processorienterad redovisning"""
    verbose_name = _(u'Spara arkivbeskrivning')
    icon = Icon('tango/22x22/mimetypes/x-office-document.png')
    
    def model_run( self, model_context ):
        templname = 'procdesc'
        outoptions = OutputOptions()
        yield ChangeObject( outoptions )
        outformat = outoptions.outformat
        of_opt = outformat_options(outformat, templname)
        select_report_file = SelectFile( of_opt['filefilter'] )
        select_report_file.existing = False
        report_filename = (yield select_report_file)[0]

        report_fullfilename = addext(report_filename, outformat)
        fileloader = FileSystemLoader(templdir)
        env = Environment(loader=fileloader)
        reporttempl = env.get_template(templname + '.md')
        logo = os.path.join(templdir, "logo")
        creator = model_context.get_object()
        descpath = os.path.join(settings.CAMELOT_MEDIA_ROOT(), creator.description.name)
        with open(descpath) as descfile:
            description = unicode(descfile.read(), 'utf-8')
        reportsrc = reporttempl.render(creator = creator, 
                description = description, logo = logo)

        convert_report(of_opt['templsetting'], of_opt['templfullname'], reportsrc,
                report_fullfilename, of_opt['pdoc_writer'])

class LabelReport( Action ):
    u"""Etiketter för arkivkartonger (genereras som PDF via ReportLab)"""
    verbose_name = _('Spara etiketter')
    icon = Icon('tango/22x22/mimetypes/x-office-document.png')
    
    def model_run( self, model_context ):
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm
        #import textwrap
        objclass = model_context.get_object().__class__.__name__
        
        lo = LabelOptions()
        yield ChangeObject( lo )
        filefilter = 'PDF-dokument (*.pdf);;Alla (*.*)'
        select_report_file = SelectFile( filefilter )
        select_report_file.existing = False
        report_filename = (yield select_report_file)[0]
        report_fullfilename = addext(report_filename, 'pdf')
        labelstrings_all = []
        fileloader = FileSystemLoader(templdir)
        env = Environment(loader=fileloader)
        if objclass == 'Archive':
            labeltempl = env.get_template('label.txt')
            archive = model_context.get_object()
            serlist = natsort.natsorted(archive.series, key=lambda ser: ser.signum)
            for series in serlist:
                vollist = natsort.natsorted(series.volumes, key=lambda vol: vol.volno)
                for volume in vollist:
                    curlabel = labeltempl.render(archive = archive, series = series,
                        volume = volume).replace('--', u'\u2013')
                    labelstrings_all.append(curlabel)
        elif objclass == 'Creator':
            objtempl = env.get_template('objlabel.txt')
            proctempl = env.get_template('proclabel.txt')
            typetempl = env.get_template('typelabel.txt')
            creator = model_context.get_object()
            objlist = natsort.natsorted(creator.arch_objects, key=lambda obj: obj.signum)
            for obj in objlist:
                unitlist = natsort.natsorted(obj.storage_units,
                        key=lambda unit: unit.signum)
                for unit in unitlist:
                    curlabel = objtempl.render(obj = obj, unit = unit).replace('--', u'\u2013')
                    labelstrings_all.append(curlabel)
            divlist = natsort.natsorted(creator.divisions, key=lambda div: div.signum)
            for div in divlist:
                proclist =  natsort.natsorted(div.processes, key=lambda proc: proc.signum)
                for proc in proclist:
                    unitlist = natsort.natsorted(proc.storage_units,
                        key=lambda unit: unit.signum)
                    for unit in unitlist:
                        curlabel = proctempl.render(div = div, proc = proc,
                            unit = unit).replace('--', u'\u2013')
                        labelstrings_all.append(curlabel)
                    acttypelist = natsort.natsorted(proc.acttypes, 
                            key=lambda atype: atype.signum)
                    for acttype in acttypelist:
                        unitlist = natsort.natsorted(acttype.storage_units,
                            key=lambda unit: unit.signum)
                        for unit in unitlist:
                            curlabel = typetempl.render(div = div, proc = proc,
                                    acttype = acttype, unit = unit).replace('--', u'\u2013')
                            labelstrings_all.append(curlabel)

        
        # Inspired by http://two.pairlist.net/pipermail/reportlab-users/2006-October/005401.html
        labelsize_x = lo.labelsize_x * mm
        labelsize_y = lo.labelsize_y * mm
        labelsep_x = lo.labelsep_x * mm
        labelsep_y = lo.labelsep_y * mm
        labels_xy = lo.labels_x * lo.labels_y
        papersize_x = lo.papersize_x * mm
        papersize_y = lo.papersize_y * mm
        margin_x = lo.margin_x * mm 
        margin_y = lo.margin_y * mm 
        labeltot_x = labelsize_x + labelsep_x
        labeltot_y = labelsize_y + labelsep_y
        fontsize = 10

        def chunks(l, n):
            n = max(1, n)
            return [l[i:i + n] for i in range(0, len(l), n)]
        
        labelstrings_bysheet = chunks(labelstrings_all, labels_xy)
        c = canvas.Canvas(report_fullfilename)
        c.setPageSize((papersize_x, papersize_y))

        def LabelPosition(labelord):
            y, x = divmod(labelord, lo.labels_x)
            x = margin_x + x * labeltot_x
            y = (papersize_y - margin_y) - y * labeltot_y
            return x, y
        
        for sheet in labelstrings_bysheet:
            for labelord in range(0, len(sheet)):
                x, y = LabelPosition(labelord)
                #c.rect(x, y, labelsize_x, -labelsize_y)
                labeltext = c.beginText(x+fontsize, y-2*fontsize)
                labeltext.setFont('Helvetica', fontsize, fontsize)
                labeltext.textLines(sheet[labelord])
                #labeltext.textLines(textwrap.fill(sheet[labelord], 25, 
                #    drop_whitespace = True, replace_whitespace = False))
                c.drawText(labeltext)
                    
            c.showPage()

        c.save()

class EadReport( Action ):
    u"""EAD XML för arkiv med allmänna arkivschemat"""
    verbose_name = _(u'Spara EAD XML')
    icon = Icon('tango/22x22/mimetypes/x-office-document.png')

    def model_run( self, model_context ):
        templname = 'ead'
        filefilter = 'XML-dokument (*.xml);;Alla (*.*)'
        select_report_file = SelectFile( filefilter )
        select_report_file.existing = False
        report_filename = (yield select_report_file)[0]
        report_fullfilename = addext(report_filename, 'xml')
        fileloader = FileSystemLoader(templdir)
        env = Environment(loader=fileloader)
        reporttempl = env.get_template(templname + '.xml')
        archive = model_context.get_object()
        serlist = natsort.natsorted(archive.series, key=lambda ser: ser.signum)
        reporttempl.stream(archive = archive, serlist = serlist).dump(report_fullfilename, encoding='utf-8')

def addext(filename, ext):
        if os.path.splitext(filename)[1] == '':
            return filename + '.' + ext
        else:
            return filename

class OutputOptions( object ):
    u"""Dialog med inställningar för rapporter"""
    def __init__(self):
        self.outformat = 'docx'
        self.converter = 'pandoc'
        #self.pandocpath = os.getenv('PYPANDOC_PANDOC')
    
    class Admin( ObjectAdmin ):
        from camelot.view.controls import delegates
        # Option for docverter conversion currently disabled because of bad results.
        verbose_name = _('Rapportalternativ')
        form_display = [ 'outformat' ]
        field_attributes = {'outformat': {'delegate': delegates.ComboBoxDelegate,
            'name': 'Utdataformat', 'choices': lambda o:[('docx', 'Word-dokument (OOXML)'), 
            ('latex', 'LaTeX'), ('pdf', 'PDF-dokument')], 'editable': True},
            'converter': {'delegate': delegates.ComboBoxDelegate, 'name': 'Konverterare',
            'choices': lambda o:[('pandoc', 'Pandoc (installerad i systemet)'),
            ('docverter', 'Docverter (online)')], 'editable': True}}

class LabelOptions( object ):
    u"""Dialog med inställningar för kartongetiketter som hämtas från JSON-fil"""
    def __init__(self):
        import json
        lo = json.load(open(os.path.join(templdir, 'labeloptions.json')))
        for key, value in lo.items():
            setattr(self, key, value)
    
    class Admin( ObjectAdmin ):
        from camelot.view.controls import delegates
        verbose_name = _('Etikettalternativ')
        form_display = [ 'papersize_x', 'papersize_y', 'labels_x', 'labels_y',
                'labelsize_x', 'labelsize_y',  'labelsep_x', 'labelsep_y',
                'margin_x', 'margin_y' ]
        field_attributes = {'papersize_x': {'delegate': delegates.IntegerDelegate,
            'name': 'Pappersstorlek (X-led)', 'editable': True},
            'papersize_y': {'delegate': delegates.IntegerDelegate,
            'name': 'Pappersstorlek (Y-led)', 'editable': True},
            'labels_x': {'delegate': delegates.IntegerDelegate,
            'name': 'Antal etiketter (X-led)', 'editable': True},
            'labels_y': {'delegate': delegates.IntegerDelegate,
            'name': 'Antal etiketter (Y-led)', 'editable': True},
            'labelsize_x': {'delegate': delegates.IntegerDelegate,
            'name': 'Etikettstorlek (X-led)', 'editable': True},
            'labelsize_y': {'delegate': delegates.IntegerDelegate,
            'name': 'Etikettstorlek (Y-led)', 'editable': True},
            'labelsep_x': {'delegate': delegates.IntegerDelegate,
            'name': u'Avstånd mellan etiketter (X-led)', 'editable': True},
            'labelsep_y': {'delegate': delegates.IntegerDelegate,
            'name': u'Avstånd mellan etiketter (Y-led)', 'editable': True},
            'margin_x': {'delegate': delegates.IntegerDelegate,
            'name': 'Marginal (X-led)', 'editable': True},
            'margin_y': {'delegate': delegates.IntegerDelegate,
            'name': 'Marginal (Y-led)', 'editable': True}}
