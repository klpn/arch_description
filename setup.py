import datetime
import logging
import os
import sys

from cx_Freeze import setup, Executable

#from setuptools import setup, find_packages

logging.basicConfig( level=logging.INFO )

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

def include_files():
	path_bases = {'camelot/art': 'C:\\Python27\\Lib\\site-packages\\camelot\\art\\', 'packaging':'C:\\Python27\\Lib\\site-packages\\packaging' }
        
	zip_includes = []
	for key, val in path_bases.items():
		skip_count = len(val)
		zip_includes.append((val, key))
		for root, sub_folders, files in os.walk(val):
			for file_in_root in files:
				zip_includes.append(
					('{}'.format(os.path.join(root, file_in_root)),
					 '{}'.format(os.path.join(key, root[skip_count:], 
						 file_in_root))) 
				)      
        return zip_includes

build_exe_options = {'include_files': ['arch_description/toc16.vbs',
    'arch_description/data/', 
    'arch_description/templates/labeloptions.json', 
    'arch_description/templates/label.txt', 
    'arch_description/templates/objlabel.txt', 
    'arch_description/templates/proclabel.txt', 
    'arch_description/templates/typelabel.txt', 
    'arch_description/templates/logo.eps', 
    'arch_description/templates/description.docx', 
    'arch_description/templates/description.md', 
    'arch_description/templates/description.sty', 
    'arch_description/templates/description.tex',
    'arch_description/templates/procdesc.docx', 
    'arch_description/templates/procdesc.md', 
    'arch_description/templates/procdesc.tex',
    'arch_description/templates/procreport.docx', 
    'arch_description/templates/procreport.md', 
    'arch_description/templates/procreport.tex',
    'arch_description/templates/shipreport.docx', 
    'arch_description/templates/shipreport.md', 
    'arch_description/templates/shipreport.tex',
    'arch_description/templates/ead.xml',
    'C:\\Python27\\Lib\\site-packages\\pypandoc\\files\\pandoc.exe'],
    'zip_includes': include_files()}

setup(
    name = 'Arkivbeskrivning',
    version = '0.1',
    author = 'Karl Pettersson',
    url = 'http://www.python-camelot.com',
    include_package_data = True,
    #packages = find_packages(),
    py_modules = ['settings', 'main'],
    entry_points = {'gui_scripts':[
                     'main = main:start_application',
                    ],},
    options = {
        'bdist_cloud':{'revision':'0',
                       'branch':'master',
                       'uuid':'ba9086dd-b535-4e27-a316-1db3dc9e4504',
                       'update_before_launch':False,
                       'default_entry_point':('gui_scripts','main'),
                       'changes':[],
                       'timestamp':datetime.datetime.now(),
                       },
        'wininst_cloud':{ 'excludes':'excludes.txt',
                          'uuid':'ba9086dd-b535-4e27-a316-1db3dc9e4504', },
        'build_exe': build_exe_options
    },
    executables = [Executable('main.py', base=base)]

  )

    
