#view potholes

import streamlit as stm
import folium
from streamlit_folium import st_folium
from folium import plugins
import pandas as pd
from df_to_geojson import df_to_geojson
import json
from serve_image import serve_image

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
#if 'sidebar_state' not in stm.session_state:
#    stm.session_state.sidebar_state = 'collapsed'

#stm.set_page_config(page_title="This is a Multipage WebApp",initial_sidebar_state=stm.session_state.sidebar_state)
stm.set_page_config(page_title="This is a Multipage WebApp")
stm.title("Pothole Tracking Initiative")
stm.header('View potholes')
stm.sidebar.success("You can view various potholes here")

df = pd.read_csv('potholes.csv')

for i in range(0,len(df)):
  url = serve_image(df['dirpath'][i], i)   #calling fn to get url
  url = f"<a href={url} target='_blank'>Image</a>"
  #print(url)
  #df['image'][i] = url #loc???
  df.loc[i,'image'] = url
df.to_csv('potholes.csv',index=False)  

#print('Using iloc')
#x = df.loc[0,'image']
#print(x)

cols = ['street', 'timestamp','image']  #select columns other than lat and long
geojson = df_to_geojson(df, cols)  #passing df & columns to function

#

#dumping GeoJSONs into separate files(optional)
output_filename = 'potholes.json'
with open(output_filename, 'w') as output_file:
  output_file.write('var dataset = ')
  json.dump(geojson, output_file, indent=2)

# center on SSM
center = [46.5277912, -84.3306842]

#setting up different icons & color for stores & malls
#Link for icons - https://fontawesome.com/v4/
p_marker = folium.Marker(
  icon=folium.Icon(icon='fa-exclamation', prefix='fa', color='red'))

#create GeoJSON objects from each GeoJSON file
p_obj = folium.GeoJson(
  geojson,
  name="Potholes",
  marker=p_marker,
  #tooltip=folium.GeoJsonTooltip(fields=["street", "timestamp"],
  #                              aliases=["Street", "Timestamp"],
  #                              offset=(1,0),
  #                              localize=True),
  popup=folium.GeoJsonPopup(fields=['street','timestamp','image'],
                            aliases=["Street", "Timestamp","Image"],
                            offset=(1,0),
                            localize=True),
)



mode=stm.radio('Mode',('View','Locate'),horizontal=True)

if mode=='View':
  m = folium.Map(location=center, zoom_start=14)
  p_obj.add_to(m)
  
  #This enables user to hide/unhide each category
  folium.LayerControl().add_to(m)
  
  # call to render Folium map in Streamlit
  st_data = st_folium(m, width='90%', height=500)

if mode=='Locate':
  m = folium.Map(location=center, zoom_start=14,dragging=False,scrollWheelZoom=False)
  p_obj.add_to(m)
  
  #This enables user to hide/unhide each category
  folium.LayerControl().add_to(m)
  
  #Adds option to show user location on map
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
  
  # call to render Folium map in Streamlit
  st_data = st_folium(m, width='90%', height=500)

