# -*- coding: utf-8 -*-

import requests

from bs4 import BeautifulSoup


class InvalidArgument( Exception ):
    def __init__(self, message, errors):
        super( Exception, self).__init__(message)
        # Now for your custom code...
        self.errors = errors
	pass

class InvalidLang( Exception ):
    def __init__(self, message, errors):
        super( Exception, self).__init__(message)
        # Now for your custom code...
        self.errors = errors


class InvalidFormat( Exception ):
    def __init__(self, message, errors):
        super( Exception, self).__init__(message)
        # Now for your custom code...
        self.errors = errors
	pass


class InvalidField( Exception ):
    def __init__(self, message, errors):
        super( Exception, self).__init__(message)
        # Now for your custom code...
        self.errors = errors
	pass


class InvalidFieldsReturned( Exception):
    def __init__(self, message, errors):
        super( Exception, self).__init__(message)
        # Now for your custom code...
        self.errors = errors
	

class IpApiResponse():
    """ Class for returning and requesting its parameters.
    in case of a jason batch it will return an array of instances of this class.
    """
    def __init__(
        self, status=None, country=None, countryCode=None, region=None, regionName=None, city=None, zip_code=None,
        lat=None, lon=None, timezone=None, isp=None, org=None, AS=None, reverse=None, mobile=None, proxy=None, query=None, message=None
    ):

        self.status = None
        if status: self.status = status
        
	self.query = None
	if query: self.query = query

        self.message = None

	if self.status:
	    if self.status == "fail":
	        self.message = message        
	        return
	
	self.country = None
	if country: self.country = country

	self.countryCode = None
	if countryCode: self.countryCode = countryCode

	self.region = None
	if region: self.region = region

	self.regionName = None
	if regionName: self.regionName = regionName

	self.city = None
	if city: self.city = city

        self.zip_code = None
	if zip_code: self.zip_code = zip_code

	self.lat = None
	if lat: self.lat = lat

	self.lon = None
	if lon: self.lon = lon

	self.timezone = None
	if timezone: self.timezone = timezone

        self.isp = None
	if isp: self.isp = isp

        self.org = None
	if org: self.org = org

        self.AS = None
	if AS: self.AS = AS

        self.proxy = None
	if proxy: self.proxy = proxy
        
	self.reverse = None
	if reverse: self.reverse = reverse

        self.mobile = None
	if mobile: self.mobile = mobile

        pass

    pass



class IpApi():
    

    ERROR_MESSAGES = {
        "private range": "the IP address is part of a private range",
	"reserved range": "the IP address is part of a reserved range",
        "invalid query": "invalid IP address or domain name",
	"quota": "over quota"
    }

    FIELDS = [
        "country",
	"countryCode",
	"region",
	"regionName",
	"city",
	"zip",
        "lat",
	"lon",
	"timezone",
	"isp",
	"org",
	"as",
	"reverse",
	"mobile",
	"proxy",
	"query",
	"status",
	"message"
    ]

    FORMATS = [
        #csv, comma separated..
        "csv",
        "json",
	#JSON batch requests
        "batch",
	#New Line separated.
        "line",
	#xml
	"xml"
    ]

    LANGS = [
       "en",
       "de",
       "es",
       "pt-BR",
       "fr",
       "ja",
       "zh-CN",
       "ru"
    ]

    ENDPOINT = "http://ip-api.com/"


    def __init__(self, use_proxy=None):
        """ Inits with default non set values.
	"""
        self.proxy = None

        #If not set it will request the current public ip.
        self.lookup = None
	# If any , this will be the fields accepted by the api.
        self.fields = []
	#The response format
	self.request_format = None
        #In case there is a query for an ip.
	self.ip = None
	#In case there is a query for a domain
	self.domain = None
        #Requests the response in an specific lang.
        self.lang = None
        pass


    def set_proxy(self, proxy):
        """Sets a proxy for the requests made.
	"""
        self.proxy = proxy
        pass


    def set_format(self, useformat):
        """
	"""
	if not userformat in self.FORMATS:
	    raise( InvalidFormat( "%s is not a valid Field" % ( field, ), {} ) )
	    pass
        self.format = useformat
        pass


    def set_lan(self, lan):
	if not lan in self.LANGS:
	    raise( InvalidLang( "%s is not a valid LANG option" % ( lan, ), {} ) )
	    pass
        self.lan = lan
        pass


    def set_fields(self, fields):
        """ Receives a list of fields and sets it as
	the new fields argument.
	"""
	self.fields = []
	for field in fields:
	    self.add_field( field )
	#self.fields = fields
        pass


    def add_field(self, field):
        """Receives a field as a string to add it to the fields list argument.
	"""
        if not field in self.FIELDS:
	    raise( InvalidField( "%s is not a valid Field" % ( field, ), {} ) )
	self.fields.append( field )
        pass



    def request( self, proxy=None, request_format = None, ip = None, domain=None, lang=None ):
        """ Makes the request to the api endpoint.
	Stores the response on response argument.
	"""
	#Sets the local var proxy if any
        if not proxy: proxy = self.proxy
	#Builds the proxy dir for the request get method.
	if proxy: proxy = {"http": proxy, "https": proxy }
        #Sets the request format if any
	if not request_format: request_format = self.request_format
	#Sets the local lang var if any
	if not lang: lang = self.lang
        host = self.ENDPOINT + request_format + "/"
        # Adds ip to request endpoint
	if self.ip: host += self.ip
	# Adds domain to request endpoint.
        if self.domain: host += self.domain

        #Builds the params based on local vars.
        params = {}
	if self.fields and not "status" in self.fields: self.fields.append( "status" ) 
	if self.fields: params["fields"] = ",".join( self.fields )
        if lang: params["lang"] = lang
        
	
	self.response = requests.get(
	    host,
	    params = params,
	    proxies = proxy
	)

	if request_format == "csv":
	    self.parse_csv()
	    pass
	
        if request_format == "json":
	    self.parse_json()
	    pass
	
        if request_format == "batch":
	    self.parse_batch()
	    pass
	
        if request_format == "line":
	    self.parse_line()
	    pass
	
	if request_format == "xml":
	    self.parse_xml()
	    pass
	
        pass


    def parse_csv( self ):
        """ Parses an csv response,
	returns an IpApiResponse
	"""
	self.csv_response = self.response.text.split(",")
	if self.fields:
	    ###
	    # Checks valid number of arguments.
	    ###
	    check_n_fields = len( self.fields )
	    if self.csv_response[0] == "success" and "message" in self.fields:
	        check_n_fields = check_n_fields -1
            if not check_n_fields == len( self.csv_response):
	        raise( InvalidFieldsReturned(
		    "Requested Fields: %d Returned Fields: %d" % (
		        check_n_fields, len( self.csv_response)
		    ), {} 
		))
		pass
	    ###
	    # Build Params based on strings....
	    ###
	    params = {}
	    params["status"] = self.csv_response[0]
	    for r in self.csv_response[1:]:
	        for f in self.FIELDS:
		    if f in params:
		        continue
	            if f in self.fields:
		        if f == "zip":
			    if "zip_code" in params:
			        continue
		            params["zip_code"] = r
			    break
			if f == "as":
			    if "AS" in params:
			        continue
			    params["AS"] = r
			    break
			params[f] = r
			break
	            pass
	        pass
            self.apiresponse = IpApiResponse( **params)
	        
	    pass
        else:
	    if self.csv_response[0] == "success":
	        self.apiresponse = IpApiResponse( *self.csv_response)
		return
	        pass
	    else:
	        self.apiresponse = IpApiResponse(
		    status = self.csv_response[0],
		    message = self.csv_response[1],
		    query = self.csv_response[2]
		)
		return
	        pass
	        


    def parse_batch( self ):
        """ Parses a json batch response,
	returns an array of 
	"""
        json_response = self.response.json() 
	for batchresponse in json_response:

	    pass
        pass


    def parse_json( self ):
        """ Parses a json response.
	Returns an ApiResponse.
	"""
        self.json_response = self.response.json()
        if self.fields:
	    check_n_fields = len( self.fields )
	    #Not counting message from response if it was successful.
	    if "status" in self.json_response and self.json_response["status"] == "success" and "message" in self.fields:
	        check_n_fields = check_n_fields - 1

            if not check_n_fields == len( self.json_response.keys() ) :

	        raise( InvalidFieldsReturned(
		    "Requested Fields: %d Returned Fields: %d" % ( check_n_fields, self.json_response.keys() ), {} )
		)
	        pass
        if "zip" in self.json_response:
	    self.json_response["zip_code"] = self.json_response["zip"]
	    self.json_response.pop("zip")
	if "as" in self.json_response:
	    self.json_response["AS"] = self.json_response["as"]
	    self.json_response.pop("as")
	self.apiresponse = IpApiResponse( **self.json_response )
        pass 



    def parse_lines( self ):
        """ Parses a separated by lines response.
	"""

        self.lines_response = "\n".split( self.response.text )
	for i, line in enumerate( self.lines_response ):
	    self.lines_response[i] = line.strip()
	apiresponse_kwargs = {}
	#Check for correct fields returned
	if self.fields:
	    check_n_fields = len( self.fields )
	    if self.lines_response[0] == "success" and  "message" in self.fields:
	        check_n_fields = check_n_fields -1
	    if not check_n_fields == len( self.json_response.keys() ) :

	        raise( InvalidFieldsReturned(
		    "Requested Fields: %d Returned Fields: %d" % ( check_n_fields, self.json_response.keys() ), {} 
		))
	    #Custom fields:
            params = {}
	    params["status"] = self.lines_response[0] 
	    for r in self.lines_response[1:]:
	        for f in self.FIELDS:
		    if f in params:
		        continue
	            if f in self.fields:
		        if f == "zip":
			    if "zip_code" in params:
			        continue
		            params["zip_code"] = r
			    break
			if f == "as":
			    if "AS" in params:
			        continue
			    params["AS"] = r
			    break
			params[f] = r
			break
	            pass
	        pass
            self.apiresponse = IpApiResponse( **params)
	    return
        
	 
	#Default response (No fields )
	if self.lines_response[0] == "success":
            self.apiresponse = IpApiResponse( *self.lines_response )
	else:
	    self.apiresponse = IpApiResponse(
	        status = self.lines_response[0],
		message= self.lines_response[1],
		query= self.lines_response[2]
	    )
	    pass
	return

        pass


    def parse_xml( self ):
        """ Parses a xml response.
	Returns an ApiResponse.
	"""
        self.xml_response = BeautifulSoup( self.response.text[39:], "xml")
	apiresponse_kwargs = {}
	query = self.xml_response.find("query")
	children = []
	for c in query.children:
	    if c != "\n":
	        children.append( c )

	if self.fields:
	    check_n_fields = len( self.fields )
	    if query.find("status").text == "success" and  "message" in self.fields:
	        check_n_fields -= 1
	    if not check_n_fields == len( children ):
	        raise( InvalidFieldsReturned(
		    "Requested Fields: %d Returned Fields: %d" % ( check_n_fields, len(children) ), {} )
		) 
	        pass
	for c in children:
	    if c.name == "zip":
		apiresponse_kwargs[ "zip_code" ] = c.string
                continue
	    if c.name == "as":
		apiresponse_kwargs["AS"] = c.string
		continue
	    apiresponse_kwargs[ c.name ] = self.xml_response.find(c.name).string
        self.apiresponse = IpApiResponse( **apiresponse_kwargs )
	


	pass


    pass



