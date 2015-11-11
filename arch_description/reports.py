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



class DescriptionReport( Action ):
    verbose_name = _(u'Spara förteckning')
    icon = Icon('tango/22x22/mimetypes/x-office-document.png')
    
    def model_run( self, model_context ):
        outoptions = OutputOptions()
        yield ChangeObject( outoptions )
        outformat = outoptions.outformat
        converter = outoptions.converter
        if outformat == 'docx':
            pdoc_writer = 'docx'
            templsetting = 'reference-docx'
            templname = os.path.join(templdir, 'description.docx')
            filefilter = 'Word-dokument (*.docx);;Alla (*.*)'
        elif outformat == 'pdf':
            pdoc_writer = 'latex'
            templsetting = 'template'
            templname = os.path.join(templdir, 'description.tex')
            filefilter = 'PDF-dokument (*.pdf);;Alla (*.*)'
        elif outformat == 'latex':
            pdoc_writer = 'latex'
            templsetting = 'template'
            templname = os.path.join(templdir, 'description.tex')
            filefilter = 'LaTeX (*.tex);;Alla (*.*)'
        select_report_file = SelectFile( filefilter )
        select_report_file.existing = False
        report_filename = (yield select_report_file)[0]

        report_fullfilename = addext(report_filename, outformat)
        archive = model_context.get_object()
        serlist = natsort.natsorted(archive.series, key=lambda ser: ser.signum)
        descpath = os.path.join(settings.CAMELOT_MEDIA_ROOT(), archive.description.name)
        with open(descpath) as descfile:
            description = descfile.read()
        fileloader = FileSystemLoader(templdir)
        env = Environment(loader=fileloader)
        reporttempl = env.get_template('description.md')
        reportsrc = reporttempl.render(archive = archive, serlist = serlist,
                description = description)

        if converter == 'pandoc':
            import pypandoc
            pdoc_args = ['--smart', '--standalone', '--toc', 
                    '--' + templsetting + '=' + templname]
            pypandoc.convert(reportsrc, pdoc_writer, format = 'md', 
                outputfile = report_fullfilename, extra_args = pdoc_args)
            if (sys.platform == 'win32' and outformat == 'docx'):
                import subprocess
                tocscript = os.path.join(maindir, 'toc16.vbs')
                subprocess.Popen(['wscript', tocscript, report_fullfilename])

        elif converter == 'docverter':
            import requests
            base_templ = os.path.basename(templname)
            docv_data = {'smart': 'true', 'from': 'markdown', 'to': outformat}
            docv_files = {'input_files[]': ('reportsrc.md', reportsrc)} 
            
            if outformat != 'pdf':
                docv_data[templsetting.replace('-', '_')] = base_templ
                docv_files['other_files[]'] = (base_templ, open(templname))

            docv_req = requests.post('http://c.docverter.com/convert',
                    data = docv_data, files = docv_files)
            with open(report_fullfilename, 'wb') as outfile:
                outfile.write(docv_req.content)

class LabelReport( Action ):
    verbose_name = _('Spara etiketter')
    icon = Icon('tango/22x22/mimetypes/x-office-document.png')
    
    def model_run( self, model_context ):
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm
        import textwrap
        
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
        labeltempl = env.get_template('label.txt')
        archive = model_context.get_object()
        serlist = natsort.natsorted(archive.series, key=lambda ser: ser.signum)
        for series in serlist:
            vollist = natsort.natsorted(series.volumes, key=lambda vol: vol.volno)
            for volume in vollist:
                curlabel = labeltempl.render(archive = archive, series = series,
                        volume = volume).replace('--', u'\u2013')
                labelstrings_all.append(curlabel)
        
        # Inspired by http://two.pairlist.net/pipermail/reportlab-users/2006-October/005401.html
        labelsize_x = lo.labelsize_x * mm
        labelsize_y = lo.labelsize_y * mm
        labels_xy = lo.labels_x * lo.labels_y
        papersize_x = lo.papersize_x * mm
        papersize_y = lo.papersize_y * mm
        labelsep = labelsize_x
        margin_x = 14
        margin_y = 36
        fontsize = 12

        def chunks(l, n):
            n = max(1, n)
            return [l[i:i + n] for i in range(0, len(l), n)]
        
        labelstrings_bysheet = chunks(labelstrings_all, labels_xy)
        c = canvas.Canvas(report_fullfilename)
        c.setPageSize((papersize_x, papersize_y))

        def LabelPosition(labelord):
            y, x = divmod(labelord, lo.labels_x)
            x = margin_x + x * labelsep 
            y = (papersize_y - margin_y) - y * labelsize_y
            return x, y
        
        for sheet in labelstrings_bysheet:
            for labelord in range(0, len(sheet)):
                x, y = LabelPosition(labelord)
                c.rect(x, y, labelsize_x, -labelsize_y)
                labeltext = c.beginText(x, y-fontsize)
                labeltext.setFont('Times-Roman', fontsize, fontsize)
                labeltext.textLines(textwrap.fill(sheet[labelord], 20, 
                    replace_whitespace = False))
                c.drawText(labeltext)
                    
            c.showPage()

        c.save()

def addext(filename, ext):
        if os.path.splitext(filename)[1] == '':
            return filename + '.' + ext
        else:
            return filename

class OutputOptions( object ):
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
    def __init__(self):
        import json
        lo = json.load(open(os.path.join(templdir, 'labeloptions.json')))
        for key, value in lo.items():
            setattr(self, key, value)
    
    class Admin( ObjectAdmin ):
        from camelot.view.controls import delegates
        verbose_name = _('Etikettalternativ')
        form_display = [ 'papersize_x', 'papersize_y', 'labels_x', 'labels_y',
                'labelsize_x', 'labelsize_y' ]
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
            'name': 'Etikettstorlek (Y-led)', 'editable': True}}
