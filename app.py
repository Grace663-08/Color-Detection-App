import cv2
import pandas as pd
import streamlit as st
import numpy as np

# Load the color dataset
@st.cache_data
def load_data():
    return pd.read_csv("colors.csv")

color_data = load_data()

# Function to find the closest color
def get_color_name(R, G, B):
    min_distance = float('inf')
    color_name = "Unknown"
    
    for index, row in color_data.iterrows():
        distance = np.sqrt((R - row["R"])**2 + (G - row["G"])**2 + (B - row["B"])**2)
        if distance < min_distance:
            min_distance = distance
            color_name = row["Color Name"]
    
    return color_name

# Streamlit UI
st.title("🎨 Color Detection from Images")
st.write("Upload an image and click anywhere to detect the color")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Read the image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Display the image
    st.image(image_rgb, caption="Uploaded Image", use_column_width=True)
    
    # Get click coordinates
    click = st.empty()
    click.info("Click below to select a point on the image")
    
    # Create a placeholder for the image with click detection
    img_placeholder = st.empty()
    img_placeholder.image(image_rgb, use_column_width=True)
    
    # Get click position
    if img_placeholder.image is not None:
        # Using streamlit's experimental click detector
        click_data = st.session_state.get("click_data", None)
        
        if click_data:
            x, y = click_data["x"], click_data["y"]
            
            # Get the color at the clicked position
            pixel_color = image_rgb[y, x]
            color_name = get_color_name(pixel_color[0], pixel_color[1], pixel_color[2])
            
            # Display results
            st.success(f"Detected Color: {color_name}")
            st.write(f"RGB Values: ({pixel_color[0]}, {pixel_color[1]}, {pixel_color[2]})")
            
            # Show color swatch
            st.markdown(
                f'<div style="width:100px;height:100px;border-radius:8px;'
                f'background-color:rgb({pixel_color[0]},{pixel_color[1]},{pixel_color[2]});'
                f'border:2px solid #eee;margin:10px 0;"></div>',
                unsafe_allow_html=True
            )
            
            # Reset click data
            st.session_state.click_data = None
