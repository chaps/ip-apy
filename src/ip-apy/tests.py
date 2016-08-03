#! -*- coding: utf-8 -*-

from ip_api import IpApiResponse, IpApi, InvalidField
from random import randint


def test_instance_class( ipapi ):
    """ Tests the type if the instanced class.\
    """
    assert type(ipapi.__class__) == type(IpApi)
    pass


def test_json( ipapi ):
    """Tests that the json response is valid.\
    """
    ipapi.request( request_format="json" )
    assert type( ipapi.apiresponse.__class__ ) == type( IpApiResponse ) 
    pass


def test_xml( ipapi ):
    """ Tests that the xml response is valid.\
    """
    ipapi.request( request_format="xml")
    assert type( ipapi.apiresponse.__class__ ) == type( IpApiResponse ) 


def test_csv( ipapi ):
    """ Tests that the csv response is valid.\
    """
    ipapi.request( request_format="csv" )
    assert type( ipapi.apiresponse.__class__ ) == type( IpApiResponse ) 


def test_lines( ipapi ):
    """ Tests that the lines response is valid.\
    """
    ipapi.request( request_format="lines")
    pass


def test_add_invalid_field( ipapi ):
    """ Tries to add an invalid field to the requests fields list.
    """
    try:
        ipapi.add_field( "Yeo" )
	raise(BaseException("Error not called..."))
    except InvalidField, e:
        print "Exception:"
        print e
        assert type( e.__class__) == type( InvalidField  )


def test_set_fields( ipapi ):
    """Test adding and retriving a random number of fields.\
    """
    fields = []
    nfields = randint( 1, len(ipapi.FIELDS)-1 )
    tmpfields = list( ipapi.FIELDS )

    for i in range(nfields):
        fields.append( tmpfields[ randint( 1, len(tmpfields)-1 ) ] )
	tmpfields.remove( fields[-1] )
    ipapi.set_fields( fields )
    assert len( ipapi.fields ) > 0
    pass


def test_json_fields( ipapi ):
    """After setting random fields.
    """
    test_set_fields( ipapi )
    test_json( ipapi )    
    pass


def test_xml_fields( ipapi ):
    test_set_fields( ipapi )
    test_xml( ipapi )
    assert type( ipapi.apiresponse.__class__ ) == type( IpApiResponse ) 


def test_csv_fields( ipapi ):
    test_set_fields( ipapi )
    test_csv( ipapi )
    pass


def test_lines_fields( ipapi ):
    test_set_fields( ipapi )
    test_lines( ipapi )


if __name__ == "__main__":

    ipapi = IpApi()
    test_instance_class( ipapi )
    test_json( ipapi )
    test_xml( ipapi )
    test_csv( ipapi )
    test_lines( ipapi )
    test_add_invalid_field( ipapi )
    
    test_set_fields( ipapi )
    test_json_fields( ipapi )
    test_xml_fields( ipapi )
    test_csv_fields( ipapi )
    test_lines_fields( ipapi )
    pass
