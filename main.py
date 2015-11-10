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


import logging
import os
from camelot.core.conf import settings, SimpleSettings
from arch_description.paths import datadir 

logging.basicConfig( level = logging.ERROR )
logger = logging.getLogger( 'main' )

# begin custom settings
class MySettings( SimpleSettings ):

    # add an ENGINE or a CAMELOT_MEDIA_ROOT method here to connect
    # to another database or change the location where files are stored
    #
    # def ENGINE( self ):
    #     from sqlalchemy import create_engine
    #     return create_engine( 'postgresql://user:passwd@127.0.0.1/database' )
    def ENGINE( self ):
        from sqlalchemy import create_engine
        return create_engine( 'sqlite:///' + os.path.join(datadir, 'description.db') )
    
    def CAMELOT_MEDIA_ROOT( self ):
        return datadir
    
    def setup_model( self ):
        """This function will be called at application startup, it is used to 
        setup the model"""
        from camelot.core.sql import metadata
        from camelot.core.orm import setup_all
        metadata.bind = self.ENGINE()
        import camelot.model.authentication
        import camelot.model.i18n
        import camelot.model.memento
        import arch_description.model
        import arch_description.reports
        setup_all()
        metadata.create_all()

my_settings = MySettings( 'Karl Pettersson', 'Arkivbeskrivning' ) 
settings.append( my_settings )
# end custom settings

def start_application():
    from camelot.view.main import main
    from arch_description.application_admin import MyApplicationAdmin
    main(MyApplicationAdmin())

if __name__ == '__main__':
    start_application()
    
