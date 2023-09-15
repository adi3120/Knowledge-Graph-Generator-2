from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import streamlit as st

class GraphRenderer:
	def __init__(self,width=500,height=1000):
		self.width=width
		self.height=height

	def draw_graph(self,triplets):
		with st.spinner("Rendering Graph...."):
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
					G.add_edge(edge_key[0], target_entity, label=edge_key[1],arrow='to',length=200)
			net = Network(notebook=True,directed=True)
			net.from_nx(G)
			net.show("file.html")
			HtmlFile = open("file.html", 'r', encoding='utf-8')
			source_code = HtmlFile.read() 
			components.html(source_code,height=self.height)
