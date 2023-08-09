import pandas as pd
import matplotlib.backends.backend_tkagg
import matplotlib as mlp
mlp.use('tkagg')
import matplotlib.pyplot as plt
import pycountry_convert as pc
import tkinter as tk
import PIL
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import ImageTk, Image
from user_agents import parse
from CWGraph import drawGraph

datasetloaded = False

#function to load the data from JSON file, filename is passed as argument
def loadData(filename):
    global data_df
    global data_df_PR
    global tree
    global datasetloaded
    data_df = pd.read_json(filename, lines=True)
    data_df_PR = data_df.loc[data_df['event_type'].isin({'pagereadtime', 'pageread'})]
    datasetloaded = True

#function to show the country histogram, document id is passed as argument
def showCountryHist(doc_id):
    if datasetloaded:
        country=retrieveCountry(doc_id)
        showHistogram(country)
    else:
        messagebox.showinfo("Information", "Input data file not loaded. Please load dataset and try again.")

#function to retrieve the countries of the documents, document id is passed as argument
def retrieveCountry(doc_id):
    newdf=data_df.loc[data_df['subject_doc_id'] == doc_id]
    country=newdf["visitor_country"]
    return country

#function to show the continent histogram, document id is passed as argument
def showContinentHist(doc_id):
    if datasetloaded:
        continent = []
        country=retrieveCountry(doc_id)
        for record in country:
            continent.append(country_to_continent(record))
        showHistogram(continent)
    else:
        messagebox.showinfo("Information", "Input data file not loaded. Please load dataset and try again.")

#function to retrieve the continents of the documents, document id is passed as argument
def country_to_continent(country_alpha2):
    country_to_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_to_continent_name = pc.convert_continent_code_to_continent_name(country_to_continent_code)
    return country_to_continent_name

#function to show the browser names in the histgram
def showBrowserHist():
    if datasetloaded:
        bdf=[]
        browserdf=data_df['visitor_useragent']
        for record in browserdf:
            # Accessing user agent's browser attributes
            user_agent = parse(record)
            bdf.append(user_agent.device.family)
        showHistogram(bdf)
    else:
        messagebox.showinfo("Information", "Input data file not loaded. Please load dataset and try again.")

#function to show the browser names in the histgram
def showBrowserHistName():
    if datasetloaded:
        bdf=[]
        browserdf=data_df['visitor_useragent']
        for record in browserdf:
            # Accessing user agent's browser attributes
            user_agent = parse(record)
            bdf.append(user_agent.browser.family)
        showHistogram(bdf)
    else:
        messagebox.showinfo("Information", "Input data file not loaded. Please load dataset and try again.")

#function that draws the histogram by plotting the passed data using matplot
def showHistogram(data):
    img_name="temp_img.png"
    plt.figure(figsize=(6.5,6))
    plt.rcParams.update({'font.size': 10})
    plt.hist(data)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(img_name)
    plt.clf()
    plt.cla()
    plt.close()
    #tree.destroy
    open_img(img_name)

#function that loads the temporarily created image to show the histogram on the GUI
def open_img(imagefile):
    img = PIL.ImageTk.PhotoImage(PIL.Image.open(imagefile))
    content_display.config(image=img)
    content_display.image=img

#function to show the top readers list, this function will gather the required data
def showTopReadersList():
    if datasetloaded:
        content_display.config(text="Top Readers")
        #select only visitor uuid and event readtime
        rdf=data_df_PR[['visitor_uuid','event_readtime']].copy()
        #group by visitor uuid and sum on event readtime
        rdf=rdf.groupby(['visitor_uuid']).sum().reset_index()
        # sort on total readtime
        rdf = rdf.sort_values(['event_readtime'],ascending=False)
        selected_rdf = rdf.head(10)
        showList(selected_rdf)
    else:
        messagebox.showinfo("Information", "Input data file not loaded. Please load dataset and try again.")

#function to show the top readers list by receving the data as arguments, build a tree to show the data.
def showList(data):
    content_display.config(image="")
    content_display.image=""
    clear_tree()
    cols = list(data.columns)
    tree["columns"] = cols
    for i in cols:
        tree.column(i, anchor=tk.CENTER)
        tree.heading(i, text=i, anchor=tk.CENTER)
    for index, row in data.iterrows():
        tree.insert('', tk.END,values=list(row))
    tree.place(x=200,y=130)

#function to clear the tree to show next information
def clear_tree():
    for each_item in tree.get_children():
      tree.delete(each_item)

#function to retrieve the visitor ids of the reader for the document id passed as argument
def retrieveVisitorUUID(doc_id):
    visitors=data_df_PR.loc[data_df['subject_doc_id'] == doc_id]
    visitors=visitors[['subject_doc_id','visitor_uuid']].copy()
    visitors=visitors.drop_duplicates()
    return visitors

#function to retrieve the documents ids for the visitor id passed as argument
def retrieveDocumentID(visitor_id):
    documents=data_df_PR.loc[data_df['visitor_uuid'] == visitor_id]
    documents=documents[['visitor_uuid','subject_doc_id']].copy()
    documents=documents.drop_duplicates()
    return documents

#function that identifies the also like documents of the document id passed as argument
def retrieveAlsoLike(doc_id, docSort):
    if datasetloaded:
        alsoRead = []
        for index, visitor in retrieveVisitorUUID(doc_id).iterrows():    
            for index, document in retrieveDocumentID(visitor['visitor_uuid']).iterrows():
                if visitor['subject_doc_id'] != document['subject_doc_id']:
                    alsoRead.append({'subject_doc_id': doc_id, 'visitor_uuid': visitor['visitor_uuid'], 'also_like_doc': document['subject_doc_id']})
    else:
        messagebox.showinfo("Information", "Input data file not loaded. Please load dataset and try again.")
    return(alsoRead)

#function to segregate and sort the data required to show the also like list
def showAlsoLike(doc_id, docSort):
    alsoRead = retrieveAlsoLike(doc_id, docSort)
    if len(alsoRead) != 0:
        content_display.config(text="Also Likes")
        alsoRead_pdf = pd.DataFrame(alsoRead)
        alsoRead_pdf = alsoRead_pdf[['also_like_doc']].copy()
        alsoRead_pdf = alsoRead_pdf.groupby(['also_like_doc']).size().reset_index(name='Counts')
        sorted = docSort(alsoRead_pdf)
        showList(sorted)
    else:
        messagebox.showinfo("Information", "No data available for the request.")

#function that gathers the also like documents list to draw the graph
def showGraph(doc_id, docSort):
    alsoRead = retrieveAlsoLike(doc_id, docSort)
    if len(alsoRead) != 0:
        content_display.config(text="Also Likes")
        alsoRead_pdf = pd.DataFrame(alsoRead)
        forSort = alsoRead_pdf[['also_like_doc']].copy()
        forSort = forSort.groupby(['also_like_doc']).size().reset_index(name='Counts')
        sorted = docSort(forSort)
        alsoRead_pdf = alsoRead_pdf[['visitor_uuid','also_like_doc']].copy()
        showList(sorted)
        drawGraph(doc_id, alsoRead_pdf)
    else:
        messagebox.showinfo("Information", "No data available for the request.")

#function to sort the data using sorting parameter
def sortDocs(docs):
    sortedDocs = docs.sort_values(['Counts'],ascending=False)
    sortedDocs = sortedDocs.head(10)
    return(sortedDocs)
    
#events to follow when the country button is clicked
def countryButtonClicked():
    if doc_ID_Entry.get() == '':
        messagebox.showinfo("Information", "Document Id can't be blank. Enter a Document Id.")
    else:
        showCountryHist(doc_ID_Entry.get())

#events to follow when the continent button is clicked
def continentButtonClicked():
    if doc_ID_Entry.get() == '':
        messagebox.showinfo("Information", "Document Id can't be blank. Enter a Document Id.")
    else:
        showContinentHist(doc_ID_Entry.get())

#events to follow when the browser button is clicked
def browserButtonClicked():
    showBrowserHist()

#events to follow when the browser button is clicked
def browserButtonVClicked():
    showBrowserHistName()

#events to follow when the top reader button is clicked
def readerButtonClicked():
    showTopReadersList()

#events to follow when the also like button is clicked
def alsoLikeButtonClicked():
    if doc_ID_Entry.get() == '':
        messagebox.showinfo("Information", "Document Id can't be blank. Enter a Document Id.")
    else:
        showAlsoLike(doc_ID_Entry.get(), sortDocs)

#events to follow when the draw graph button is clicked    
def drawGraphButtonClicked():
    if doc_ID_Entry.get() == '':
        messagebox.showinfo("Information", "Document Id can't be blank. Enter a Document Id.")
    else:
        showGraph(doc_ID_Entry.get(), sortDocs)

#function to allow user to select a file to load
def selectFileClicked():
    filetypes = (('json files', '*.json'),('All files', '*.*'))
    filename = fd.askopenfilename(title='Open File',initialdir='/',filetypes=filetypes)
    if filename != '':
        loadData(filename)
    else:
        messagebox.showinfo("Information", "Input file not selected properly.")

#function that runs the gui
def showGUI():
    #global root
    root.mainloop()

#function that is called from CW2.py which carries the task id, document id and filename from command line and calls the appropriate function    
def performTask(task_id, filename, doc_uuid):
    doc_ID_Entry.delete(0, END)
    doc_ID_Entry.insert(0, doc_uuid)
    if task_id == '2a':
        loadData(filename)
        showCountryHist(doc_uuid)
        showGUI()
    elif task_id == '2b':
        loadData(filename)
        showContinentHist(doc_uuid)
        showGUI()
    elif task_id == '3a':
        loadData(filename)
        showBrowserHist()
        showGUI()
    elif task_id == '3b':
        loadData(filename)
        showBrowserHistName()
        showGUI()
    elif task_id == '4':
        loadData(filename)
        showTopReadersList()
        showGUI()
    elif task_id == '5d':
        loadData(filename)
        showAlsoLike(doc_uuid, sortDocs)
        showGUI()
    elif task_id == '6':
        loadData(filename)
        showGraph(doc_uuid, sortDocs)
        showGUI()
    elif task_id == '7':
        loadData(filename)
        showGraph(doc_uuid, sortDocs)
        showGUI()
    elif task_id == '8':
        showGUI()
    else:
        print('No valid task id passed.')

#GUI initiation and building
root = Tk()
root.title('Document Tracker')

window_width = 1200
window_height = 700
# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

#GUI DESIGN PART
doc_ID_Label = Label(root, text="Enter Document id:")
doc_ID_Label.pack(side = LEFT, anchor=NW,padx=30,pady=50)

doc_ID_Entry = Entry(root, bd=5)
doc_ID_Entry.pack(side = LEFT,anchor=NW,padx=30,pady=50)

x=0  

#open file button
openFileBtn = Button(root,
                        text='Load Dataset',
                        command=selectFileClicked)
openFileBtn.place(x=10)

# Histogram Of Countries button
countryButton = Button(root,
                        text = "Countries", 
                        command = countryButtonClicked)
#countryButton.pack()
countryButton.place(x=125)

# Histogram Of Continents button
continentButton = Button(root,
                        text = "Continents", 
                        command = continentButtonClicked)
#continentButton.pack()

continentButton.place(x=220)

# Histogram Of Browsers button
browserButton = Button(root,
                        text = "Browsers", 
                        command = browserButtonClicked)
#browserButton.pack()
browserButton.place(x=320)

# Histogram Of Browsers button
browserVButton = Button(root,
                        text = "Browser Names", 
                        command = browserButtonVClicked)
#browserVButton.pack()
browserVButton.place(x=410)

# Top Readers button
readerButton = Button(root,
                        text = "Top Readers", 
                        command = readerButtonClicked)
#readerButton.pack()
readerButton.place(x=540)

alsoLikesBtn = Button(root,
                        text = "Also Likes", 
                        command = alsoLikeButtonClicked)
alsoLikesBtn.place(x=650)

displayGraphBtn = Button(root,
                        text = "Also Likes Graph", 
                        command = drawGraphButtonClicked)
displayGraphBtn.place(x=750)

#treeview to display readers list
tree = ttk.Treeview(root)

content_display = Label(root)
content_display.place(x=200,y=100)

#main function
if __name__ == "__main__":
    showGUI()
