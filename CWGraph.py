from graphviz import Digraph
import pandas as pd

#function to draw the also like graph, data is passed from the calling function and the graph is generated and drawn here.
def drawGraph(doc_id, alsoRead_pdf):
    uniqueReaders = alsoRead_pdf[['visitor_uuid']].copy()
    uniqueReaders= pd.DataFrame.drop_duplicates(uniqueReaders, subset=['visitor_uuid'])
 
    algraph = Digraph()

    #Creating the Subgtraph with same rank
    with algraph.subgraph() as i:
        i.attr(rank='same',label="Readers")
        for index, data in uniqueReaders.iterrows():    
            i.node(str(data['visitor_uuid'])[-4:], shape="box") #visitor ids / readers are added to the graph
         
    #Creating SubGraph with same level
    with algraph.subgraph() as i:
        i.attr(rank='same',label='Documents')
        i.node(str(doc_id)[-4:],shape="circle",style='filled',color=".3 .9 .7") #input document id is added to the graph
        for index, data in alsoRead_pdf.iterrows(): 
            i.node(str(data['also_like_doc'])[-4:], shape="circle")
            algraph.edge(str(data['visitor_uuid'])[-4:],str(data['also_like_doc'])[-4:]) #also like documents are added to the graph
        
        for index, data in uniqueReaders.iterrows():     
            algraph.edge(str(data['visitor_uuid'])[-4:],str(doc_id)[-4:]) #edges between readers and documents are added to the graph

    algraph.render('Also Like Graph', view=True)

