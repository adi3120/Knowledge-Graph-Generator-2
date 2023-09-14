import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
from langchain.schema import SystemMessage,HumanMessage
from graphimage import draw_graph_from_image,draw_graph_from_image_link
from graphvideo import draw_graph_from_video
from graphvidlink import draw_graph_from_link

openai_api_key=None
schema = {
	"properties": {
		"subject_entity": {"type": "string"},
		"relation_type": {"type": "string"},
		"target_entity": {"type": "string"},
	},
	"required": ["subject_entity", "relation_type", "target_entity"],
}

def draw_graph(triplets):
    edge_dict = {}

    G = nx.DiGraph()
    for triplet in triplets:
        subject_entity = triplet["subject_entity"]
        relation_type = triplet["relation_type"]
        target_entity = triplet["target_entity"]

        edge_key = (subject_entity, relation_type)
        if edge_key in edge_dict:
            edge_dict[edge_key].append(target_entity)
        else:
            edge_dict[edge_key] = [target_entity]

        G.add_node(subject_entity)
        G.add_nodes_from(edge_dict[edge_key]) 

    for edge_key, target_entities in edge_dict.items():
        for target_entity in target_entities:
            G.add_edge(edge_key[0], target_entity, label=edge_key[1],arrow='to')

    net = Network(notebook=True,directed=True)
    net.from_nx(G)
    net.show("file.html")
    HtmlFile = open("file.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=1000)
    

def draw_graph_from_text(desc):
    global openai_api_key
    llm = ChatOpenAI(
					temperature=0, 
					model="gpt-3.5-turbo",
					openai_api_key=openai_api_key
				)
    message = [SystemMessage(content=("Your task is to process the text and retain only the relevant information in the form of entity-relation-entity triples."))]
    llm(message)
    chain = create_extraction_chain(schema, llm)
    data=chain.run(desc)
    draw_graph(data)
    
    
	
    
def draw_graph_from_keywords(keywords):
    global openai_api_key
    llm = ChatOpenAI(
					temperature=0, 
					model="gpt-3.5-turbo",
					openai_api_key=openai_api_key
				)
    message=[
		SystemMessage(content=("Provide short summary for each of the following topic(s) and try to relate similar topic")),
		HumanMessage(content=(keywords))
	]
    data=str(llm(message))
    message = [SystemMessage(content=("Your task is to process the text and retain only the relevant information in the form of entity-relation-entity triples."))]
    llm(message)
    chain = create_extraction_chain(schema, llm)
    data=chain.run(data)
    print(data)
    draw_graph(data)	
    

with st.sidebar:    
    st.title("Knowledge Graph Generator")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    selected_option = st.radio("Create Knowledge Graph from:", ("Long Textual Data","Keywords", "Video from Device", "Video from YouTube", "Image from Device","Image from URL"))
    selected={
        "desc":False,
        "keywords":False,
        "video":False,
        "link":False,
        "image":False,
        "imagelink":False
	}
    if(selected_option=="Long Textual Data"):
        desc=st.text_area("Enter Text Description")
        for i in selected.keys():
            selected[i]=False
            if i=="desc":
                selected[i]=True
    elif(selected_option=="Keywords"):
        keywords=st.text_area("Enter Comma separated Keywords")
        for i in selected.keys():
            selected[i]=False
            if i=="keywords":
                selected[i]=True
    elif(selected_option=="Video from Device"):
        uploaded_file_video = st.file_uploader("Choose a video...", type=["mp4", "mpeg"])
        for i in selected.keys():
            selected[i]=False
            if i=="video":
                selected[i]=True
    elif(selected_option=="Video from YouTube"):
        linkid=st.text_input("Enter youtube video id")
        for i in selected.keys():
            selected[i]=False
            if i=="link":
                selected[i]=True
    elif(selected_option=="Image from Device"):
        uploaded_file_image = st.file_uploader("Choose an image...", type=["jpeg", "jpg","png"])
        for i in selected.keys():
            selected[i]=False
            if i=="image":
                selected[i]=True
    elif(selected_option=="Image from URL"):
        linkimg=st.text_input("Enter image link")
        for i in selected.keys():
            selected[i]=False
            if i=="imagelink":
                selected[i]=True
    submit=st.button("Create Mind Map")
    
if submit and openai_api_key:
    st.title("Knowledge Graph Generator")
    with st.spinner('Making your graph...'):
        if selected["desc"]:
            draw_graph_from_text(desc)
        elif selected["keywords"]:
            draw_graph_from_keywords(keywords)
        elif selected["video"]:
            data=draw_graph_from_video(uploaded_file_video)
            draw_graph_from_text(data)
        elif selected["link"]:
            with st.spinner("Downloading the video"):
                 draw_graph_from_link(linkid)
            with open("video.mp4","rb") as f:
                 data=draw_graph_from_video(f)
                 draw_graph_from_text(data)
        elif selected["image"]:
            data=draw_graph_from_image(uploaded_file_image)
            draw_graph_from_text(data)
        elif selected["imagelink"]:
            data=draw_graph_from_image_link(linkimg)
            draw_graph_from_text(data)
            
    
	

    