###################################################################
# Author    :   Sivaprakash.B                                     #
# Email     :   ssivpr@amazon.com                                 #
# Purpose   :   Python Tool for Amazon Fire TV Log Analysis         #
###################################################################


# Validating the import as python versions < 3 supports Tkinter ( T - Upper Case )
# And python versions >3 supports tkinter ( T - Lower Case )

try:
    import Tkinter as tkin         # This is for python2
    import tkFileDialog            # For providing dialog box option for selecting files
    import tkMessageBox            # For displaying message box alerts
    import webbrowser              # For converting text into clickable links
except:
    import tkinter as tkin         # This is for python3
    tkFileDialog=tkin.filedialog   # For providing dialog box option for selecting files
    tkMessageBox=tkin.messagebox   # For displaying message box alerts
    import webbrowser              # For converting text into clickable links

import subprocess                  # For validating the output on the search query


# Declaring variables required for the code 

m=tkin.Tk()                        # Creating root object ( m )  of the Tkinter ot tkinter 
m.title('FireLogPad')                  # Adding title to the root object or the GUI Window.
m.resizable(0,0)                   # Setting the window not to be resized due to python limitations

filename = ""                       # Variable to hold the file path of the file to be analysied 
bgcolor = '#ff9900'                    # Variable to hold Background color for the theme
fgcolor = 'black'                    # Variable to hold foreground or text color for the theme
logareabgcolor = 'black'


# Variable to hold the color code for the logs based on the type log filter. 

logscolorcode = {'E':'red', 'W':'yellow','D':'green', 'I':'white','V':'blue','all':'white'} 

# Top frame holds the file selection and file path display section 

topframe = tkin.Frame(m)
topframe.configure(bg=bgcolor)
topframe.pack( side = tkin.TOP, expand=tkin.TRUE)

# Search frame is used to have search box enter the text for search

searchframe = tkin.Frame(m)
searchframe.configure(bg=bgcolor)
searchframe.pack( side = tkin.TOP)

# filter frame is used to set the search filters

filterframe = tkin.Frame(m)
filterframe.configure(bg=bgcolor)
filterframe.pack( side = tkin.TOP)

# Bottom frame holds the Log Area to display the logs.

bottomframe = tkin.Frame(m)
bottomframe.configure(bg=bgcolor)
bottomframe.pack( side = tkin.TOP)


# Function to select the file to parse the logs.

def SelectFile():
     global filename
     filename = tkFileDialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        
     # Validation to check if a file is selected or not 
    
     if len(filename) == 0 :
         return
    
     filepatharea.delete('1.0', tkin.END)
     filepatharea.insert(tkin.INSERT,filename)
     searchquery = "awk '{ print;}' "+ filename
     logarea.config(fg=logscolorcode[logtype.get()]) 
     logarea.insert(tkin.INSERT,subprocess.check_output(searchquery,shell=True))

# Search function to filter the logs based on selection 

def SearchFunction():
     global filename,logtype,cataegory,casecheck,negationcheck,afterbox,beforebox

     # Validation to check if a file is selected or not 
     if len(filename) == 0 :
         tkMessageBox.showerror("Error", "Please select the log file to perform search")
         return
    
     # Clearing Log Area for new search results
        
     logarea.delete('1.0', tkin.END)

     # Validation to if search should be performed only on classname or not.

     if cataegory.get() :
         if logtype.get() == "all" :
            searchquery = "awk '{ print $6;}' "+ filename +" | sort -u "
         else :
             searchquery = "awk '{ if( $5 == \""+logtype.get()+"\" ) print $6;}' " + filename + " | sort -u "
     else :
         if logtype.get() == "all" :
            searchquery = "awk '{ print;}' "+ filename
         else :
             searchquery = "awk '{ if( $5 == \""+logtype.get()+"\" ) print;}' "+ filename 
     options=""

     if searchbox.get("1.0",'end-1c') :
         options+= " -i " if casecheck.get() else ""
         options+= " -v " if negationcheck.get() else ""
         options+= " -A "+afterbox.get("1.0",'end-1c')+" " if afterbox.get("1.0",'end-1c') else ""
         options+= " -B "+beforebox.get("1.0",'end-1c')+" " if beforebox.get("1.0",'end-1c') else ""
         searchquery = searchquery+" | grep "+options+" \""+ searchbox.get("1.0",'end-1c') + "\" "
     print ( "\n" + searchquery )  
    
     logarea.config(fg=logscolorcode[logtype.get()]) 
     logarea.insert(tkin.INSERT,subprocess.check_output(searchquery,shell=True))

# Event Call Back for Key Down Events

def HandleKeyRelease (e) :
    print ( "Keypressed" , e.char )
    SearchFunction()


# Event Call Back for AFTER OR BEFORE INT BOX Key Down Events

def HandleKeyAFTERINTRelease (e) :
    if afterbox.get("1.0",'end-1c') :
        try : 
            i=int(afterbox.get("1.0",'end-1c'))
            print ( i )
            print ( "Keypressed", e.char )
            SearchFunction()
        except :
            tkMessageBox.showerror("Error", "Please enter a interger value")
            afterbox.delete('1.0', tkin.END)
    else :
        SearchFunction()


def HandleKeyBEFOREINTRelease (e) :
    if beforebox.get("1.0",'end-1c') :
        try : 
           i=int(beforebox.get("1.0",'end-1c'))
           print ( i )
           print( "Keypressed" , e.char )
           SearchFunction()
        except :
           tkMessageBox.showerror("Error", "Please enter a interger value")
           beforebox.delete('1.0', tkin.END)
    else :
        SearchFunction()
    

# Callback function to call a web URL

def callback(url):
    webbrowser.open_new(url)

# File Path label creation and packing to the view area

filepathlabel = tkin.Label(topframe,justify = tkin.LEFT)
filepathlabel.config(text = "FILE PATH :",bg=bgcolor,fg=fgcolor)
filepathlabel.pack(anchor=tkin.W)

# File Path creation and packing to the view area

filepatharea = tkin.Text(topframe,wrap=tkin.WORD,width=200, height= 2)
filepatharea.configure(bg=bgcolor,fg=fgcolor,highlightbackground=bgcolor)
filepatharea.pack(fill="none", expand=tkin.TRUE)

# Select File action button creation and packing to the view area

selectfilebutton = tkin.Button(topframe, text='SELECT FILE',command=SelectFile)
selectfilebutton.pack(side=tkin.BOTTOM)

# ( Deprecated ) Get Logs action button creation and packing to the view area

#searchbutton = tkin.Button(topframe, text='Search', bg='green',fg='white', command=SearchFunction)
#searchbutton.pack(fill="none",side=tkin.RIGHT)

# Search box label creation and packing to the view area

searchboxlabel = tkin.Label(searchframe,justify = tkin.LEFT)
searchboxlabel.config(text = "SEARCH AREA",bg=bgcolor,fg=fgcolor)
searchboxlabel.pack(side=tkin.LEFT)
 
# Search box text area creation and packing to the view area

searchbox=tkin.Text(searchframe, height=2, width=50, borderwidth=2, relief=tkin.GROOVE)
searchbox.configure(highlightbackground=bgcolor)
searchbox.bind('<KeyRelease>',HandleKeyRelease)
searchbox.pack(side=tkin.LEFT)

# Before box label creation and packing to the view area

beforeboxlabel = tkin.Label(searchframe,justify = tkin.LEFT)
beforeboxlabel.config(text = "BEFORE ",bg=bgcolor,fg=fgcolor)
beforeboxlabel.pack(side=tkin.LEFT)
 
# Before box text area creation and packing to the view area

beforebox=tkin.Text(searchframe, height=1, width=3, borderwidth=2, relief=tkin.GROOVE)
beforebox.configure(highlightbackground=bgcolor)
beforebox.bind('<KeyRelease>',HandleKeyBEFOREINTRelease)
beforebox.pack(side=tkin.LEFT)

# After box label creation and packing to the view area

afterboxlabel = tkin.Label(searchframe,justify = tkin.LEFT)
afterboxlabel.config(text = "AFTER ",bg=bgcolor,fg=fgcolor)
afterboxlabel.pack(side=tkin.LEFT)
 
# After box text area creation and packing to the view area

afterbox=tkin.Text(searchframe, height=1, width=3, borderwidth=2, relief=tkin.GROOVE)
afterbox.configure(highlightbackground=bgcolor)
afterbox.bind('<KeyRelease>',HandleKeyAFTERINTRelease)
afterbox.pack(side=tkin.LEFT)




# Class name category selection Check Box creation

cataegory = tkin.IntVar()
classnamecheckbox = tkin.Checkbutton(searchframe,variable=cataegory,command=SearchFunction)
classnamecheckbox.config(bg=bgcolor)
classnamecheckbox.pack(side=tkin.LEFT)

# Category selection check box label creation and packing to the view area

classnamecheckboxlabel = tkin.Label(searchframe,justify = tkin.LEFT)
classnamecheckboxlabel.config(text = "SEARCH CLASS NAME ALONE",bg=bgcolor,fg=fgcolor)
classnamecheckboxlabel.pack(side=tkin.LEFT)


# Ingnore Case Check Box creation

casecheck = tkin.IntVar()
ignorecasecheckbox = tkin.Checkbutton(searchframe,variable=casecheck,command=SearchFunction)
ignorecasecheckbox.config(bg=bgcolor)
ignorecasecheckbox.pack(side=tkin.LEFT)

# Ingnore case check box label creation and packing to the view area

ignorecasecheckboxlabel = tkin.Label(searchframe,justify = tkin.LEFT)
ignorecasecheckboxlabel.config(text = "IGNORE CASE",bg=bgcolor,fg=fgcolor)
ignorecasecheckboxlabel.pack(side=tkin.LEFT)

# Ingnore Case Check Box creation

negationcheck = tkin.IntVar()
negatecasecheckbox = tkin.Checkbutton(searchframe,variable=negationcheck,command=SearchFunction)
negatecasecheckbox.config(bg=bgcolor)
negatecasecheckbox.pack(side=tkin.LEFT)

# Negate Keyword case check box label creation and packing to the view area

negatecasecheckboxlabel = tkin.Label(searchframe,justify = tkin.LEFT)
negatecasecheckboxlabel.config(text = "NEGATE KEYWORD",bg=bgcolor,fg=fgcolor)
negatecasecheckboxlabel.pack(side=tkin.LEFT)

# Logs Type ( E - Error, W - Warning, D - Debug, I - Information, V - Verbose , ALL ) Category selection 
# Radio box creation, packing and default option selection.

logtype= tkin.StringVar()
tkin.Radiobutton(filterframe, 
              value='E',     # E - Error Category Radio Button  
              variable=logtype, 
              command=SearchFunction,
              bg=bgcolor,fg=fgcolor).pack(side=tkin.LEFT)
tkin.Label(filterframe,justify = tkin.LEFT, text = "E",bg=bgcolor,fg=logscolorcode['E'], padx = 20).pack(side=tkin.LEFT)

tkin.Radiobutton(filterframe, 
              value='W',     # W - Warning Category Radio Button  
              variable=logtype, 
              command=SearchFunction,
              bg=bgcolor,fg=fgcolor).pack(side=tkin.LEFT)
tkin.Label(filterframe,justify = tkin.LEFT, text = "W",bg=bgcolor,fg=logscolorcode['W'], padx = 20).pack(side=tkin.LEFT)

tkin.Radiobutton(filterframe, 
              value='D',     # D - Debug Category Radio Button  
              variable=logtype, 
              command=SearchFunction,
              bg=bgcolor,fg=fgcolor).pack(side=tkin.LEFT)
tkin.Label(filterframe,justify = tkin.LEFT, text = "D",bg=bgcolor,fg=logscolorcode['D'], padx = 20).pack(side=tkin.LEFT)

tkin.Radiobutton(filterframe, 
              value='I',     # I - Info Category Radio Button  
              variable=logtype,
              command=SearchFunction, 
              bg=bgcolor,fg=fgcolor).pack(side=tkin.LEFT)
tkin.Label(filterframe,justify = tkin.LEFT, text = "I",bg=bgcolor,fg=logscolorcode['I'], padx = 20).pack(side=tkin.LEFT)

tkin.Radiobutton(filterframe, 
              value='V',     # V - Verbose Category Radio Button  
              variable=logtype, 
              command=SearchFunction,
              bg=bgcolor,fg=fgcolor).pack(side=tkin.LEFT)
tkin.Label(filterframe,justify = tkin.LEFT, text = "V",bg=bgcolor,fg=logscolorcode['V'], padx = 20).pack(side=tkin.LEFT)

R1=tkin.Radiobutton(filterframe, 
              value='all',    # ALL Category Radio Button 
              variable=logtype, 
              command=SearchFunction,
              bg=bgcolor,fg=fgcolor)
R1.pack(side=tkin.LEFT)
R1.select()
tkin.Label(filterframe,justify = tkin.LEFT, text = "ALL",bg=bgcolor,fg=logscolorcode['all'], padx = 20).pack(side=tkin.LEFT)


# Log Area Label creation and packing to the view area

logarealabel = tkin.Label(bottomframe,justify = tkin.LEFT)
logarealabel.config(text = "LOG AREA", bg=bgcolor,fg=fgcolor)
logarealabel.pack(anchor=tkin.W)

# Log Area creation and packing to the view area

logarea = tkin.Text(bottomframe,wrap=tkin.WORD,width=200, height= 30, borderwidth=2, relief=tkin.GROOVE, bg=logareabgcolor, fg=fgcolor)
logarea.pack(fill="none", expand=tkin.TRUE)

# Adding config to the Root Element ( m )

m.config(bg=bgcolor)
m.mainloop()
