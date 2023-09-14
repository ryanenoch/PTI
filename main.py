import streamlit as stm
import os.path
import csv

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
#if 'sidebar_state' not in stm.session_state:
#    stm.session_state.sidebar_state = 'collapsed'

#stm.set_page_config(page_title="This is a Multipage WebApp",initial_sidebar_state=stm.session_state.sidebar_state)
stm.set_page_config(page_title="This is a Multipage WebApp")
stm.title("Pothole Tracking Initiative")
#stm.sidebar.success("Select Any Page from here")

stm.markdown(
  'PTI is an inhouse initiative to help the people of SSM report potholes and be informed of one in their neighborhood, near their workplace, near their favorite grocery store or anywhere in Sault Ste Marie'
)

# /IMGDIR/image_name.jpg
#out = os.path.isabs("/IMGDIR/WhatsApp Image 2023-04-16 at 10.22.27 PM.jpeg")
#print(out)

#if CSV file doesn't exist, one will be created on first time use
if os.path.isfile('potholes.csv')==False:
  with open('potholes.csv', 'w', newline='') as csvfile:
      fieldnames = ['lat','long','street','timestamp','dirpath','image']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
  print('CSV file created')    

 #st.markdown("", unsafe_allow_html=True) 
