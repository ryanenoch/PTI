# Copied from Streamlit's implementation of st.image
def serve_image(image, image_id):
  import mimetypes
  from streamlit import runtime
  from streamlit.runtime import caching
  
  mimetype, _ = mimetypes.guess_type(image)
  if mimetype is None:
    mimetype = "application/octet-stream"
  url = runtime.get_instance().media_file_mgr.add(image, mimetype, image_id)
  caching.save_media_data(image, mimetype, image_id)
  return (url)