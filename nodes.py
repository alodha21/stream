import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowEdge,StreamlitFlowNode
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout
import pandas as pd


def home_page():
    st.title('Home')

    nodes = [
            StreamlitFlowNode(id='1', pos=(0, 0), data={'content': 'Node 1'}, node_type='input', source_position='right', target_position='left'),
            StreamlitFlowNode(id='2', pos=(0, 0), data={'content': 'Node 2'}, node_type='default',target_position= 'left'),
            StreamlitFlowNode(id='3', pos=(0, 0), data={'content': 'Node 3'}, node_type='default', target_position='left'),
            StreamlitFlowNode(id='4', pos=(0, 0), data={'content': 'Node 4'}, node_type='output', target_position='left'),
            StreamlitFlowNode(id='5', pos=(0, 0), data={'content': 'Node 5'}, node_type='output', target_position='left'),
            StreamlitFlowNode(id='6', pos=(0, 0), data={'content': 'Node 6'}, node_type='output', target_position='left'),
            StreamlitFlowNode(id='7', pos=(0, 0), data={'content': 'Node 7'}, node_type='output', target_position='left')
        ]
    edges = [
            StreamlitFlowEdge('1-2', '1', '2', animated=True),
            StreamlitFlowEdge('1-3', '1', '3', animated=True),
            StreamlitFlowEdge('2-4', '2', '4', animated=True),
            StreamlitFlowEdge('2-5', '2', '5', animated=True),
            StreamlitFlowEdge('3-6', '3', '6', animated=True),
            StreamlitFlowEdge('3-7', '3', '7', animated=True)
        ]
    state = StreamlitFlowState(nodes,edges)
    streamlit_flow('tree_layout',state,layout=TreeLayout(direction='right'),fit_view=True, allow_new_edges=True,enable_edge_menu=True,enable_pane_menu=True,enable_node_menu=True)


def flow(df):
    nodes = []
    edges = []
    node_ids = set()
   
    for index,row in df.iterrows():
            source_id = row['Source']
            target_id = row['Target']
            if source_id not in node_ids:
                nodes.append(StreamlitFlowNode(id=source_id, pos=(0, 0), data={'content': source_id}, node_type='default'))
                node_ids.add(source_id)

            if target_id not in node_ids:
                nodes.append(StreamlitFlowNode(id=target_id, pos=(0, 0), data={'content': target_id}, node_type='default'))
                node_ids.add(target_id)
                

            edges.append(StreamlitFlowEdge(id=f'{source_id}-{target_id}', source=f'{source_id}', target=f'{target_id}', animated=True))
            
    return nodes,edges        

def visualize_flow(nodes,edges):
    state = StreamlitFlowState(nodes,edges)
    streamlit_flow('tree_layout',state,layout=TreeLayout(direction='right'),fit_view=True, allow_new_edges=True,enable_edge_menu=True,enable_pane_menu=True,enable_node_menu=True)

def about_page():
    st.title('About')
    file = st.file_uploader(label='Upload CSV', type=['csv'])
    if file is not None:
        data = pd.read_csv(file)
        with st.expander('View'):
           st.dataframe(data)

                    
        with st.expander('Flow'): 
            nodes,edges = flow(data)
            #st.write(nodes)
            #st.write(edges)
            visualize_flow(nodes,edges)

def main():
    home = st.Page(home_page,title='Home')
    about = st.Page(about_page,title='About')

    pg = st.navigation({'Pages':[home,about]})
    pg.run()

if __name__ == '__main__':
    main()