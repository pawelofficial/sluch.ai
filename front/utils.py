

import streamlit as st 



# sets session state variables, no overwrite 
def init_session_state():
    map={
        'logged_in':False,
        'username':None,
        'password':None
    }
    for key,value in map.items():
        if key not in st.session_state:
            st.session_state[key]=value



# checks if user is logged in
def is_logged():
    if  st.session_state.get('logged_in'):
        return True
    return False 

# gets session value
def get_session_value(key):
    value=st.session_state.get(key,None)
    return value
def get_username():
    return get_session_value('username')


def set_session_value(key,value):
    st.session_state[key]=value
        
# shows bottom stuff on sidebar 
def bottom_placeholder():
    bottom_placeholder = st.sidebar.empty()

    if get_session_value('logged_in'):
        bottom_placeholder.markdown("---") 
        bottom_placeholder.write(f"logged in as {get_session_value('username')} ")
    

def authenticate(username,password,df):
    if df is None:
        set_session_value('logged_in',True)
        set_session_value('username',username)
        set_session_value('password',password)

    return get_session_value('logged_in')
    
    
#@st.fragment not sure if leave as fragment or not 
def login(dummy=True):

        
    """Handles user login."""
    if is_logged(): # return if logged in already 
        return
    if dummy:
        authenticate('admin','password',None)
        st.rerun()
    
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        authenticate(username,password,None)
        
    if is_logged():
        st.rerun()
        #st.rerun(scope='fragment')
    
    
def read_file(fp):
    with open(fp,encoding="utf-8" ) as f :
        text=f.read()
    return text