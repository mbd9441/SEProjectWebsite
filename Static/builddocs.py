import os, json, shutil

curdir = os.path.dirname(__file__)
headers=[]

def openfile(filename):
    filepath = os.path.join(curdir, filename)
    openfile = open(filepath,'r')
    return(openfile.read())

def createdoclist(filename):
    global headers
    doclist=json.loads(openfile(filename))
    for key,value in doclist.items():
        for items in value:
            for key, value in  items.items():
                curheader=key
                #print(curheader)
                headers=headers+[curheader]
                #print(headers)
                makedir(curheader)
                makeheader(curheader)
                for items in value:
                    makefiles(curheader, items)
    makedoclisthtml()

def makedir(curheader):
    folder=os.path.join(curdir, 'HTML/' + curheader)
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    try:  
        os.mkdir(folder)
    except OSError:  
        print ("Creation of the directory %s failed" % folder)
    else:  
        print ("Successfully created the directory %s " % folder)

def makeheader(curheader):
    folder=os.path.join(curdir, 'HTML/' + curheader)
    headertemplate=openfile(os.path.join(curdir, "HTML/TableHeader.html"))
    headertemplate=headertemplate.replace("{{curheader}}", curheader)
    #print(headertemplate)
    newheaderhtml=open(os.path.join(folder, curheader+".html"),'w')
    newheaderhtml.write(headertemplate)

def makefiles(curheader, items):
    folder=os.path.join(curdir, 'HTML/' + curheader)
    curname=items.get("name")
    headerhtml=open(os.path.join(folder, curheader+".html"),'a')
    documenttemplate=openfile(os.path.join(curdir, "HTML/Document.html"))
    addtoheader='<div class="listitems" w3-include-html="Static/HTML/{{curheader}}/{{name}}.html"></div>'
    addtoheader=addtoheader.replace("{{curheader}}",curheader)
    addtoheader=addtoheader.replace("{{name}}", curname)
    #print(addtoheader)
    headerhtml.write("\n"+addtoheader)
    for key, value in items.items():
        if key=="name":
            documenttemplate=documenttemplate.replace("{{" + key + "}}", value)
        else:
            documenttemplate=documenttemplate.replace("{{" + key + "}}", '"' + value + '"')
    #print(documenttemplate)
    newdocument=open(os.path.join(folder, curname+".html"),'w')
    newdocument.write(documenttemplate)

def makedoclisthtml():
    global headers
    addtodoclist='				<div class="listitems" w3-include-html="Static/HTML/{{header}}/{{header}}.html"></div>'
    doclisttemplate=openfile("HTML/Documents.html")
    doclisttemplate=doclisttemplate.split("~")
    newdoclist=doclisttemplate[0]
    for header in headers:
        currentaddtodoclist=addtodoclist.replace("{{header}}", header)
        newdoclist+="\n"+currentaddtodoclist
        #print(newdoclist)
    newdoclist+=doclisttemplate[1]
    #print(newdoclist)
    newdoclisthtml=open(os.path.join(curdir, "../Documents.html"),'w')
    newdoclisthtml.write(newdoclist)    

createdoclist('doclist.txt')
