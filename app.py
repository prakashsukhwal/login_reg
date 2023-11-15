import streamlit as st
import sqlite3
from importlib.metadata import version
print(sqlite3.version)
# Initialize session state
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Connect to SQLite database
conn = sqlite3.connect('user.db')
c = conn.cursor()

# Create users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, gender TEXT, age INTEGER, health_conditions TEXT)''')

# Registration page
def registration():
    st.header('User Registration')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    gender = st.selectbox('Gender', ['Male', 'Female'])
    age = st.selectbox('Age', range(20, 101))
    health_conditions = st.multiselect('Existing Health Conditions', ['Diabetes', 'Hypertension', 'Asthma'])
    if st.button('Register'):
        # Check if user already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone() is not None:
            st.error('User already exists. Please proceed to login.')
        else:
            # Add user to database
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (username, password, gender, age, ', '.join(health_conditions)))
            conn.commit()
            st.success('Registration successful. Please proceed to login.')

# Login page
def login():
    st.header('User Login')
    username = st.text_input('Username', key='11')
    password = st.text_input('Password', type='password', key='22')
    if st.button('Login'):
        # Check if user exists
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone() is not None:
            st.success('Login successful.')
            st.session_state['username'] = username
        else:
            st.error('Invalid username or password. Please try again.')

# User details page
def user_details():
    st.header('User Details')
    c.execute("SELECT * FROM users WHERE username=?", (st.session_state['username'],))
    user = c.fetchone()
    st.write('Username:', user[0])
    st.write('Gender:', user[2])
    st.write('Age:', user[3])
    st.write('Existing Health Conditions:', user[4])

# Logout functionality
def logout():
    st.session_state['username'] = None
    st.success('Logout successful.')

# Multipage streamlit application
def app():
    st.set_page_config(page_title='User Registration and Login', page_icon=':guardsman:', layout='wide')
    st.title('User Registration and Login')
    menu = ['Home', 'Registration', 'Login', 'User Details']
    choice = st.sidebar.selectbox('Select an option', menu)
    if choice == 'Home':
        st.write('Welcome to User Registration and Login')
    elif choice == 'Registration':
        registration()
    elif choice == 'Login':
        login()
    elif choice == 'User Details':
        if st.session_state['username'] is not None:
            user_details()
            st.button('Logout', on_click=logout)
        else:
            st.warning('Please login to view user details.')

if __name__ == '__main__':
    app()
