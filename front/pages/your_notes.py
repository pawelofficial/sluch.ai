
import streamlit as st 
import os 
import sys 
sys.path.append(os.path.abspath('.'))
import utils as stu

# redirect to home if not logged in 
if not stu.is_logged():
    st.markdown('<meta http-equiv="refresh" content="0;URL=/" />', unsafe_allow_html=True)


stu.bottom_placeholder()

import streamlit as st
import os

def read_notes():
    fp = f"./permanent_data/{stu.get_username()}"
    
    if not os.path.exists(fp):
        st.error("No notes found!")
        return

    files = os.listdir(fp)
    
    
    if not files:
        st.warning("No files available.")
        return

    # Create three tabs for switching between different note sets
    tab1, tab2, tab3 = st.tabs(["Note 1", "Note 2", "Note 3","Recap"])

    with tab1:
        selected_file1 = st.selectbox("Select file in Tab 1", files, key="file1",index=None)
        if selected_file1:
            text1 = stu.read_file(os.path.join(fp, selected_file1))
            st.write(text1)

    with tab2:
        selected_file2 = st.selectbox("Select file in Tab 2", files, key="file2",index=None)
        if selected_file2:
            text2 = stu.read_file(os.path.join(fp, selected_file2))
            st.write(text2)

    with tab3:
        selected_file3 = st.selectbox("Select file in Tab 3", files, key="file3",index=None)
        if selected_file3:
            text3 = stu.read_file(os.path.join(fp, selected_file3))
            st.write(text3)



        
read_notes()