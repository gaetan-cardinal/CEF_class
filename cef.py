import re

class CEFevt:
    """
    CEFevt class doc

    This Class allows creating and manipulating CEF events objects. 

    A CEF instance has following attributes:
	CEF Header : obj.header : the mandatory parameters located at the beginning of a CEF event
        CEF Tail   : obj.tail   : the optional key=value pairs defining the CEF extension and located at the end of the CEF event
        CEF Event  : obj.event  : the concatenation of the CEF Header and the CEF Tail representing the full CEF event
    
    The methods are split in 4 main groups:
        Generic  : apply to the whole cef event
        Header   : modification of the header (method name always start with 'h')
        Tail     : modification of the tail (method name always start with 't')
        Internal : not meant to be called by an external program. Should only be used by the class functions
    
    Available functions (Internal function not shown):
        __init__         
        display
        hcreate
        hreplace
        tcreate
        tappendfield
        tappendfields
        tremovefield
        tremovefields
        treplace
        tempty
    
    Documentation:
        From the Python interpreter:
        >>> import cef
        >>> print(cef.CEFevt.function_name.__doc__)
    """   


    #######################
    ### Generic methods ###
    #######################

    def __init__(self,deviceVendor="test",deviceProduct="test",deviceVersion="1.0",deviceEventClassId="100",name="test event",severity="0",dictail={}):
        """
        __init__
        
        Desc: initializing the CEF header. If no data provided for the header, 
              default value will be used in order to have a valid CEF event.
              If no data provided for the tail, tail is kept empty.

        Syntax:
            obj=CEFevt([deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity,dictail])
                deviceVendor:        string
                deviceProduct:       string
                deviceVersion:       string
                deviceEventClassId:  string
                name:                string
                severity:            string
                dictail:             dictionary containing fieldname,value key pairs for the tail 
                                     ie: {'msg': 'test message', 'src': '1.2.3.4'}

        """
        self.header=self._headerbuilder(deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity)
        self.tail=self.tcreate(dictail)
        self.event=self.header+self.tail


    def display(self):  
        """
        display 
        
        Desc: just printing the cef event 

        Syntax: 
            obj.display()
        """
        self.event=self.header+self.tail
        print(self.event)

    def help(self,method=""):
        """
        help

        Desc: printing the doc of a method. If no method is provided, the class doc and the list of methods is printed.

        Syntax:
            obj.help([method])
              method:  string

        Return:
            doc: string
                 The output of the method
        """
        import cef
        if method == "all":
            
            print (cef.CEFevt.__doc__) 
            methods_lst = [method for method in dir(CEFevt) if callable(getattr(CEFevt, method))]
            for metname in methods_lst:
                print "### "+metname+" ###"
                command1="print (cef.CEFevt."+str(metname)+".__doc__)" ; 

        elif method == "":
            #print (cef.CEFevt.__doc__) 
            pass

        else :
            try:
                command1="print (cef.CEFevt."+str(method)+".__doc__)" ; exec command 
            except Exception,e: 
                print str(e) 
            

    #######################
    ### Header methods  ###
    #######################


    def hcreate(self,deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity):
        """  
        hcreate

        Desc: create a new cef header. All the values must be provided in the correct order
 
        Syntax:
            obj.hcreate(deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity)
        """
        deviceVendor=self._hescaping(deviceVendor); deviceProduct=self._hescaping(deviceProduct); deviceVersion=self._hescaping(deviceVersion)
        deviceEventClassId=self._hescaping(deviceEventClassId); name=self._hescaping(name); severity=self._hescaping(severity)
      
        self.header=self._headerbuilder(deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity)
        self.event=self.header+self.tail
    
    
    def hreplace(self,field,value):
        """ 
        hreplace

        Desc: replace the value of one of the fields in the cef header. In order to avoid typo when calling this function
              several values are valid for some field names and the field name is not case sensitive . 
              It is also possible to use a numerical value to design the fieldname which needs to be changed 

        Syntax: 
            obj.hreplace(fieldname,value)
              fieldname: string 
              value:     string

        Allowed fieldnames (not case sensitive):
              deviceVendor 1
              deviceProduct 2 
              deviceVersion 3
              deviceEventClassId SigId SignatureId 4 
              name 5
              severity 6

        Examples:
              obj.hreplace("1","MyVendor")
              obj.hreplace(sIGiD,"101")
        """
        value=self._hescaping(value)
        field=str(field)
        field=field.lower()
        if field=="1" or field=="devicevendor" :
            self.deviceVendor=value
        elif field=="2" or field=="deviceproduct" :
            self.deviceProduct=value
        elif field=="3" or field=="deviceversion" :
            self.deviceVersion=value
        elif field=="4" or field=="deviceeventclassid" or field=="sigid" or field=="signatureid" :
            self.deviceEventClassId=value
        elif field=="5" or field=="name" :
            self.name=value
        elif field=="6" or field=="severity" :
            self.severity=value
        else :
            print("\nIncorrect field name (%s) provided to hreplace. No change implemented to the header\n" % (field))
        self.header=self._headerbuilder(self.deviceVendor,self.deviceProduct,self.deviceVersion,self.deviceEventClassId,self.name,self.severity)
        self.event=self.header+self.tail



    ####################    
    ### Tail methods ###
    ####################

    def tcreate(self,dict):
        """
        tcreate

        Desc: replace the existing tail with the key/value pairs provided in a dictionary format
        
        Syntax:
            obj.tcreate(dict)
              dict: dictionary containing fieldname/value key pairs.
                    ie: {'msg': 'test message', 'src': '1.2.3.4'} 
        Return:
            tail: string
        """
        newtail=''
        try:
            for key,value in dict.iteritems():
                newtail=newtail+" "+key+"="+value
                #self.tail=self.tail+" "+key+"="+value
            self.tail=newtail.lstrip()
        except Exception,e: print("\nThe variable provided to tcreate should be a dictionary\n"+str(e)+"\n")
        self.event=self.header+self.tail    
        return(self.tail)
        
    def tappendfield(self,field,value):
        """
        tappendfield

        Desc: add a new fieldname and its value at the end of the existing tail. 
        
        Syntax: 
            obj.tappendfield(fieldname,value)
              fieldname:  string
              value:      string
        """
        self.tail=self.tail+' '+field+'='+value
        self.tail=self.tail.lstrip()
        self.event=self.header+self.tail

    def tappendfields(self,dict):
        """
        tappendfields

        Desc: add one or several fieldname(s) and their value(s) at the end of the existing tail.

        Syntax:
            obj.tappendfield(dict)
              dict:  dictionary
                     ie: {'msg': 'test message', 'src': '1.2.3.4'}
        """
        newtail=''
        try:
            for key,value in dict.iteritems():
                newtail=newtail+" "+key+"="+value
            self.tail=self.tail+newtail
            self.tail=self.tail.lstrip()
        except Exception,e: print("\nThe variable provided to tappendfields should be a dictionary\n"+str(e)+"\n")
        self.event=self.header+self.tail
        
    def tremovefield(self,field):
        """
        tremovefield

        Desc: remove the fieldname and its value from the tail. If the fieldname can't be found, no action is taken

        Syntax: 
            obj.tremovefield(fieldname)
              fieldname:  string

        Return:
            fieldfound:  boolean --> indicates if the fieldname has been found in the tail
        """
        fieldfound=False
        regex=re.search(r"(.*)" + re.escape(field) + r"=(.*)", self.tail, re.IGNORECASE)
        if regex: # the fieldname provided has been found
            fieldfound=True
            tailstart=regex.group(1)
            tailend=regex.group(2)
            regex=re.search(r" ([^\\ ]+=[^ ]+.*)", tailend)
            if regex: # the fieldname is not the last one in the tail
                self.tail=tailstart+regex.group(1)
            else: # the fieldname is the last in the queue
                self.tail=tailstart.rstrip()
            self.event=self.header+self.tail
        else:
            pass
            #The fieldname couldn't be found in the tail. No change made to the tail 
        return(fieldfound)

    def tremovefields(self,list):
        """
        tremovefields

        Desc: remove one or several fieldname(s) and their value(s) from the tail

        Syntax:
            obj.tremovefields(dict)
              dict: dictionary containing fieldname/value key pairs.
                    ie: {'msg': 'test message', 'src': '1.2.3.4'}
        """
        for fieldname in list:
            self.tremovefield(fieldname)

    def treplace(self,fieldname,newvalue,append=True):
        """
        treplace

        Desc: replace the value of an existing field in the tail by another one. 

        Syntax:
            obj.treplace(fieldname, value[,append]) 
                fieldname: str: field to replace
                newvalue: str: the new value of the fieldname in the tail
                append: bool: by default, if the fieldname is not found, the fieldname/value pair is added to the string (similar to tappendfield).
                              if set to False, no action is taken if the field is not found
        """
        fieldfound=self.tremovefield(fieldname) 
        if fieldfound:
            self.tappendfield(fieldname,newvalue)
        else:
            if append:
                self.tappendfield(fieldname,newvalue)
               
    def tempty(self):
        """
        tempty
        
        Desc: simply empty the tail
        
        Syntax:
            obj.tempty()
        """
        self.tail=""
        self.event=self.header+self.tail


    ########################
    ### Internal methods ###
    ########################

    def _headerbuilder(self,deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity):
        """
        _headerbuilder

        Desc: build the cef header based on variables received
        For internal use only. To build a header from your program, call hcreate method

        Syntax:
            self._headerbuilder(deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity)
              deviceVendor:        string
              deviceProduct:       string
              deviceVersion:       string
              deviceEventClassId:  string
              name:                string
              severity:            string

        Return:
            header:  string 
                    
        """
        header="CEF:0|%s|%s|%s|%s|%s|%s|" % (deviceVendor,deviceProduct,deviceVersion,deviceEventClassId,name,severity)
        self.deviceVendor=deviceVendor ; self.deviceProduct=deviceProduct ; self.deviceVersion=deviceVersion
        self.deviceEventClassId=deviceEventClassId ; self.name=name ; self.severity=severity
        return(header)    

    def _hescaping(self,value):
        """
        _hescaping

        Desc: escape special characters as explained in the 'Implementing Arcsight CEF' official document

              | char will be replaced by \|  -- \| char will be kept like that, assuming the escaping aleady happened
              \ char will be replaced by \\  -- \\ char will be kept like that, assuming the escaping already happened 

              The idea is to escape special characters when they probably haven't been in the value provided but to keep the escaping
              in the values which seem to have been escaped already. This should be accurate most of the time but will not properly
              escape sequences of several continuguous backspaces 

              For internal use only, should not be called from the main program

        Syntax:
            obj._hescaping(value)
              value:  string

        Return:
            value:  string
                    The input value after escaping
        """
        value=value.replace("\|","|")             
        value=value.replace("\\","\\\\")
        value=value.replace("|","\|")
        return(value)


############################
### Examples and testing ###
############################

cef=CEFevt()
'''
# __init__
print("\n__init__ CEFevt object at init time:\n\n\t"+cef.event+"\n")
command='cef=CEFevt()' ; exec command
print('\tex1: '+command+'\n\t\t'+cef.event)
dict={'src': '1.2.3.4', 'dhost': 'www.foo.com'}
command='cef=CEFevt("myvendor","myproduct","","","","1",dict)' ; exec command 
print('\tex2: '+command+'\n\t\t'+cef.event+"\n\t\tdict="+str(dict))


# hcreate
command='cef.hcreate("vendor","product","2.0","1000","event name","0")' ; exec command
print('\nhcreate: creating a new header: '+command+'\n\n\t'+cef.event+"\n") 

# hreplace
print('hreplace: replacing some cef header elements:\n')
command='cef.hreplace("deviceVendor","WorldCompany")' ; exec command
print('\tex1: '+command+'\n\t\t'+cef.event)
command='cef.hreplace("dEvicevendor","anotherCompany")' ; exec command
print('\tex2: '+command+'\n\t\t'+cef.event)
command='cef.hreplace("5","name is the fifth element in the header")' ; exec command
print('\tex3: '+command+'\n\t\t'+cef.event)

# tcreate
dict={'src': '1.2.3.4', 'dhost': 'www.foo.com'}
command='cef.tcreate(dict)' ; exec command
print('\ntcreate: creating a new tail: '+command+'\n\n\t'+cef.event+"\n")
print("\tdict:"+str(dict))

# tappendfield
command='cef.tappendfield("cs1","this is my custom string 1")' ; exec command
print('\ntappendfield: adding a new element to the tail: '+command+'\n\n\t'+cef.event+"\n")

# tappendfields
dict={'dst': '2.3.4.5', 'shost': 'www.bar.org'}
command='cef.tappendfields(dict)' ; exec command
print('\ntappendfields: adding new element(s) to the tail from dict: '+command+'\n\n\t'+cef.event+"\n")
print("\tdict:"+str(dict))

# tremovefield
command='cef.tremovefield("cs1")' ; exec command
print('\ntremovefield: removing an element from the tail: '+command+'\n\n\t'+cef.event+"\n")

# tremovefields
list=["src","dhost"]
command='cef.tremovefields(list)' ; exec command
print('\ntremovefields: removing element(s) from the tail: '+command+'\n\n\t'+cef.event+"\n")
print("\tlist:"+str(list))

# treplace
print('\ntreplace: replacing a value in the tail: \n')
command='cef.treplace("shost","www.newbar.org")' ; exec command
print('\tex1: '+command+'\n\t\t'+cef.event)
command='cef.treplace("cs3","my cs3",False)' ; exec command
print('\tex2: '+command+'\n\t\t'+cef.event)
command='cef.treplace("cs3","my cs3")' ; exec command
print('\tex3: '+command+'\n\t\t'+cef.event+"\n")

# tempty
command='cef.tempty()' ; exec command
print('\ntempty: emptying the tail: '+command+'\n\n\t'+cef.event+"\n")

# hescaping 
print("\n_hescaping\nThis is an example of how the internal function _hescaping escapes values in the header")
print("Note that \| and \\"+"\ won't be escaped a second time as we assume they have already been escaped")
print("This is an internal function not meant to be called by the program")
value="f\o\\"+"\\o|ba\|r"
print ("Value to escape in the header: "+value)
value=cef._hescaping("f\o\\o|ba\|r")
print('Value escaped in the header: '+value)

print("\n")

#print(cef.CEFevt.hcreate.__doc__)

######################
## Printing the doc ##
######################

methods_lst = [method for method in dir(CEFevt) if callable(getattr(CEFevt, method))]
import cef
for metname in methods_lst:
    print "### "+metname+" ###"
    command="print (cef.CEFevt."+str(metname)+".__doc__)" ; exec command
'''

# help 
print('\nhelp: display help: \n')
command='cef.help()' ; print('\tex1: '+command+'\n') ; exec command
#command='cef.help("all")' ; print('\tex2: '+command+'\n') ; exec command
#command='cef.help("treplace")' ; print('\tex3: '+command+'\n') ; exec command
