# add potholes

import streamlit as stm
import folium
from streamlit_folium import st_folium
from folium import plugins
import csv
import os
from datetime import datetime
import pytz
from serve_image import serve_image

stm.title("Pothole Tracking Initiative")
stm.header('Add potholes')
stm.sidebar.success("You can add a pothole here")

# center on SSM
center = [46.5277912, -84.3306842]

m = folium.Map(location=center,zoom_start=14,dragging=False,scrollWheelZoom=False)

plugins.LocateControl(
  auto_start=False,
  flyTo=True,
  enableHighAccuracy=True,
  drawCircle=True,
  drawMarker=True,
  strings={
    "title": "See your current location",
    "popup": "You're within {distance} {unit} from this point"
  }).add_to(m)

#m.click_for_marker(popup='Waypoint')

# call to render Folium map in Streamlit
st_data = st_folium(m, width='90%', height=500)

if 'center' in st_data:
  lat, lng = (st_data['center']['lat'], st_data['center']['lng'])
  stm.text("Coordinates \n{}, {}".format(lat, lng))
  
  
  stm.text_input('Lat', lat, disabled=True)
  stm.text_input('Long', lng, disabled=True)
  street = stm.text_input('Street Name',placeholder='Enter Street name')
  timestamp = datetime.now(pytz.timezone('America/Toronto')).strftime("%c")

  image_file = stm.file_uploader('Upload an image (png,jpg,jpeg)',type=['png','jpeg','jpg'])

  
  #If the button is pressed
  if stm.button('Confirm details'):
    stm.success('Confirmed')

    #If image is uploaded
    if image_file is not None:
      file_details = {"FileName":image_file.name,"FileType":image_file.type}

      #create directory if it doesn't exists
      dir = './IMG/'
      if os.path.isdir(dir)==False:
        os.mkdir(dir)
      
      img = Image.open(image_file)

      #fixes image rotation as per exif tag
      img = ImageOps.exif_transpose(img)

      width, height = img.size 

      #compress by thumbnail method
      if width > height: #horizontal
        img.thumbnail([sys.maxsize, 720], Resampling.LANCZOS)
      elif width < height: #vertical
        img.thumbnail([720, sys.maxsize], Resampling.LANCZOS)
      
      #saves image file to directory
      img.save(os.path.join("IMG", image_file.name), optimize=True,quality=80)

        
    #add lat, lng, street, timestamp to CSV
    with open('potholes.csv', 'a', newline='') as csvfile:
      #fieldnames = ['lat','long','street','timestamp']
      fieldnames = ['lat','long','street','timestamp','dirpath']

      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writerow({'lat':lat, 'long':lng, 'street':street, 'timestamp':timestamp, 'dirpath':f'./IMG/{image_file.name}'})
     

    

      
