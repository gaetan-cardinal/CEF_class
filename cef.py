#!/usr/bin/env python

##############################################################################
# CEF library
#
# Author:  gaetan cardinal  ( cardinal_gaetan /at/ yahoo.fr )
# Version: 1.1 (02 nov 2016)
# Created: 17 oct 2016

#______________________________________________________________________________
# The MIT License
#
#Copyright 2016 Gaetan Cardinal
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#________________________________________________________________________________

import re

class CEFevt:
    """
    CEFevt class doc

    This Class allows creating and manipulating CEF events objects. 

    A CEF instance has following attributes:
	CEF Header : obj.header : the mandatory parameters located at the beginning of a CEF event
        CEF Tail   : obj.tail   : the optional key=value pairs defining the CEF extension and located at the end of the CEF event
    
    The methods are split in 4 main groups:
        Generic  : apply to the whole cef event
        Header   : modification of the header (method name always start with 'h')
        Tail     : modification of the tail (method name always start with 't')
        Internal : not meant to be called by an external program. Should only be used by the class functions
    
    Available functions (Internal function not shown):
        __init__         
        display
        help
        stringest
        hupdate
        hcleandisplay
        tupdate
        tremove
        tempty
        tcleandisplay
    
    Documentation:
        From the Python interpreter:
        >>> import cef
        >>> print(cef.CEFevt.function_name.__doc__)
    """   


    #######################
    ### Generic methods ###
    #######################

    def __init__(self,inputdict={},dictail={}):
        """
        __init__
        
        Desc: initializing the CEF header. If no data provided for the header, 
              default value will be used in order to have a valid CEF event.
              If no data provided for the tail, tail is kept empty.

        Syntax:
            obj=CEFevt([dicthead],[dictail])

                dicthead:	     dictionary containing {fieldname:value} key pairs for the tail. 
                                     ie: {"deviceVendor": "VendorX", "deviceProduct": "ProductY"}

                                     Accepted keys:

                                     deviceVendor:        string
                                     deviceProduct:       string
                                     deviceVersion:       string
                                     deviceEventClassId:  string
                                     name:                string
                                     severity:            string

                                     other keys won't generate any errors but will be discarded. If keys are missing, default values will be used

                dictail:             dictionary containing {fieldname:value} key pairs for the tail 
                                     ie: {'msg': 'test message', 'src': '1.2.3.4'}

        """
        dichead={"deviceVendor": "test", "deviceProduct": "test", "deviceVersion": "1.0", "deviceEventClassId": "100", "name": "test event","severity": "0"}
        for key in dichead:
            if key in inputdict:
                dichead[key]=inputdict[key]
        self.header=dichead
        self.tail=dictail


    def display(self):  
        """
        display 
        
        Desc: just printing the cef event 

        Syntax: 
            obj.display()

        Return:
            
            cefstr:     a string containing the cef event
        """

        cefstr=self._headerbuilder(self.header)+self._tailbuilder(self.tail) 
        print(cefstr)
        return(cefstr)

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


    def stringest(self,strcef):

        """
        stringest

        Desc: Ingest a CEF event in string format. It can then be used with all the other functions 

        Syntax:
            obj.stringest(cefevent)
              cefevent:  string

        """

        strcef=strcef.replace("\|","*()*") 
        if strcef.count('|') < 7:
            print("Couldn't parse the CEF event provided")
            quit()
        groups=strcef.split('|')
        header='|'.join(groups[:7])
        tail='|'.join(groups[7:])
        extracted_fields_lst=header.split("|")

        ## header
        self.header['deviceVendor']=extracted_fields_lst[1].replace("*()*","\|")
        self.header['deviceProduct']=extracted_fields_lst[2].replace("*()*","\|")
        self.header['deviceVersion']=extracted_fields_lst[3].replace("*()*","\|")
        self.header['deviceEventClassId']=extracted_fields_lst[4].replace("*()*","\|")
        self.header['name']=extracted_fields_lst[5].replace("*()*","\|")
        self.header['severity']=extracted_fields_lst[6].replace("*()*","\|")
       
        ## tail
        self.tail={} 
        tail=tail.replace("*()*","\|") # remove escaping to make split easier
        tail=tail.replace("\=","*()*")
        tail_lst=tail.split("=")
        i=0
        while i<len(tail_lst): # set back the escaping
            tail_lst[i]=tail_lst[i].replace("*()*","\=")
            i=i+1
        i=0;listlen=len(tail_lst)-1
        while i<listlen:
                
            regex=re.search('\s?([^\s]+)$',tail_lst[i])
            if regex :
                field=regex.group(1)
            else:
                quit()
            if i==(listlen-1): #if we are in the last part of the tail
                value=tail_lst[i+1].strip()
            else:
                regex=re.search('(.*)\s+[^\s]+$',tail_lst[i+1])
                if regex :
                    value=regex.group(1).strip()
                else:
                    quit()
            self.tail[field]=value
            i=i+1 
            

    #######################
    ### Header methods  ###
    #######################


    def hupdate(self,dicinput):
        """ 
        hupdate

        Desc: replace the value of one or several fields in the cef header. In order to avoid typo when calling this function
              several values are valid for some field names and the field name is not case sensitive . 
              It is also possible to use a numerical value to design the fieldname which needs to be changed 

        Syntax: 
            obj.hupdate(dicinput)
              dicinput:   dictionary  

        Allowed fieldnames (not case sensitive):
              deviceVendor 1
              deviceProduct 2 
              deviceVersion 3
              deviceEventClassId SigId SignatureId 4 
              name 5
              severity 6

        Example:
              obj.hupdate({"deviceVendor": "foo", "2": "bar", "siGiD": "400"})

        Return:
              head: dictionary containing the header fieldname/value pairs
        """

        dichead=self.header
        for key in dicinput:
            value=self._hescaping(dicinput[key])
            keylower=str(key).lower()
            if keylower=="1" or keylower=="devicevendor" :
                dichead["deviceVendor"]=value
            elif keylower=="2" or keylower=="deviceproduct" :
                dichead["deviceProduct"]=value
            elif keylower=="3" or keylower=="deviceversion" :
                dichead["deviceVersion"]=value
            elif keylower=="4" or keylower=="deviceeventclassid" or keylower=="sigid" or keylower=="signatureid" :
                dichead["deviceEventClassId"]=value
            elif keylower=="5" or keylower=="name" :
                dichead["name"]=value
            elif keylower=="6" or keylower=="severity" :
                dichead["severity"]=value
        self.header=dichead 
        return(self.header)

    def hcleandisplay(self):
        """
        hcleandisplay

        Desc: printing the cef event header with nice and readable output (1 fieldname/fieldvalue pair per line)

        Syntax:
            obj.hcleandisplay()
        """
        print ("CEF event header:\n=================")
        maxlen=1
        for k,v in self.header.iteritems():
            if len(k)>maxlen:
                maxlen=len(k)
        for k,v in sorted(self.header.iteritems()):
            spacenum=maxlen-len(k)+4
            print(k+spacenum*" "+v)

    ####################    
    ### Tail methods ###
    ####################


    def tupdate(self,dict):
        """
        tupdate

        Desc: add new fieldname(s)/value(s) or change value(s) of existing fieldname(s)

        Syntax:
            obj.tupdate(dict)
              dict:  dictionary
                     ie: {'msg': 'test message', 'src': '1.2.3.4'}

        Return:
            tail:    dictionary containing the tail values 
            
        """
        try:
            for key,value in dict.iteritems():
                self.tail[key]=value
        except Exception,e: print("\nThe variable provided to tappend should be a dictionary\n"+str(e)+"\n")
        return(self.tail)
        

    def tremove(self,fieldslist):
        """
        tremove

        Desc: remove one or several fieldname(s) and their value(s) from the tail

        Syntax:
            obj.tremove(fieldslist)
              fieldslist: list containing fieldnames to remove from the tail
                    ie:('msg', 'src') 

        Return:
            tail: dictionary containing new tail fieldnames/values key pairs
        """
        for fieldname in fieldslist:
            try:
                del self.tail[fieldname]
            except: 
                pass
        return(self.tail)

               
    def tempty(self):
        """
        tempty
        
        Desc: simply empty the tail
        
        Syntax:
            obj.tempty()
        """
        self.tail={}

    def tcleandisplay(self,mapdict={}):
        """
        tcleandisplay

        Desc: printing the cef event tail with nice and readable output (1 fieldname/fieldvalue pair per line)
              optionally, a dictionary mapping cef fieldname with more meaningful name can be provided

        Syntax:
            obj.tcleandisplay()
        """

        print ("\nCEF event tail:\n================")
        maxlen1=maxlen2=1
        for k,v in self.tail.iteritems(): # find the longest key in self.string
            if len(k)>maxlen1:
                maxlen1=len(k)
        if mapdict=={}: # if no mapping file
                for k,v in sorted(self.tail.iteritems()): # print
                    spacenum1=maxlen1-len(k)+4
                    print(k+spacenum1*" "+v)
        else:

           for k,v in self.tail.iteritems(): # find longest key in mapping dict
               if len(k)>maxlen2:
                   maxlen2=len(k)
           for k,v in sorted(self.tail.iteritems()): # print
                spacenum1=maxlen1-len(k)+4
                if k in mapdict:
                    spacenum2=maxlen2-len(mapdict[k])+4
                    print(k+spacenum1*" "+mapdict[k]+spacenum2*" "+v)
                else:
                    spacenum2=maxlen2+4
                    print(k+spacenum1*" "+spacenum2*" "+v)
		


    ########################
    ### Internal methods ###
    ########################

    def _headerbuilder(self,dichead):
        """
        _headerbuilder

        Desc: build the cef header based on dictionary received
        For internal use only. To build a header from your program, call hcreate method

        Syntax:
            self._headerbuilder(dichead)
              deviceVendor:        string
              deviceProduct:       string
              deviceVersion:       string
              deviceEventClassId:  string
              name:                string
              severity:            string

        Return:
            header:  string 
                    
        """
        header="CEF:0|%s|%s|%s|%s|%s|%s|" % (dichead['deviceVendor'],dichead['deviceProduct'],dichead['deviceVersion'],
                                             dichead['deviceEventClassId'],dichead['name'],dichead['severity'])
        return(header)    

    def _tailbuilder(self,dictail):
        """
        _tailbuilder

        Desc: build the cef tail based on received dictionary
        
        Syntax:
            self._tailbuilder(dictail)
                dictail:  dictionary

        Return:
            tail:  string
        """

        tail=''
        for key in dictail:
            tail=tail+' '+key+'='+dictail[key]
        tail=tail.strip()
        return(tail)


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
            self._hescaping(value)
              value:  string

        Return:
            value:  string
                    The input value after escaping
        """
        value=value.replace("\|","|")             
        value=value.replace("\\","\\\\")
        value=value.replace("|","\|")
        return(value)


