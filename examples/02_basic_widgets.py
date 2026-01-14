"""
Example 2: Basic Widgets
Demonstrates common Streamlit widgets and user inputs.

To run:
    streamlit run 02_basic_widgets.py
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Streamlit Widgets Demo",
    page_icon="🎛️",
    layout="wide"
)

# Title and description
st.title("🎛️ Streamlit Widgets Demo")
st.markdown("Explore the most commonly used Streamlit widgets")

# Divider
st.divider()

# --- TEXT INPUT WIDGETS ---
st.header("1. Text Input Widgets")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Text Input")
    name = st.text_input("Enter your name:", placeholder="John Doe")
    if name:
        st.success(f"Hello, {name}!")

    st.subheader("Text Area")
    message = st.text_area("Enter a message:", placeholder="Type here...")
    if message:
        st.info(f"You wrote: {message}")

with col2:
    st.subheader("Number Input")
    age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
    st.write(f"You are {age} years old")

    st.subheader("Date Input")
    date = st.date_input("Select a date:")
    st.write(f"Selected date: {date}")

st.divider()

# --- SELECTION WIDGETS ---
st.header("2. Selection Widgets")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Select Box")
    option = st.selectbox(
        "Choose your favorite color:",
        ["Red", "Blue", "Green", "Yellow"]
    )
    st.write(f"You selected: {option}")

with col2:
    st.subheader("Multi-Select")
    options = st.multiselect(
        "Choose multiple options:",
        ["Option A", "Option B", "Option C", "Option D"]
    )
    st.write(f"You selected: {', '.join(options)}")

with col3:
    st.subheader("Radio Buttons")
    radio_choice = st.radio(
        "Pick one:",
        ["Choice 1", "Choice 2", "Choice 3"]
    )
    st.write(f"You picked: {radio_choice}")

st.divider()

# --- SLIDER WIDGETS ---
st.header("3. Slider Widgets")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Slider")
    value = st.slider("Select a value:", 0, 100, 50)
    st.write(f"Value: {value}")

    st.subheader("Range Slider")
    range_values = st.slider("Select a range:", 0.0, 100.0, (25.0, 75.0))
    st.write(f"Range: {range_values[0]} to {range_values[1]}")

with col2:
    st.subheader("Select Slider")
    size = st.select_slider(
        "Choose shirt size:",
        options=["XS", "S", "M", "L", "XL"]
    )
    st.write(f"Size: {size}")

st.divider()

# --- BUTTON WIDGETS ---
st.header("4. Button Widgets")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Button")
    if st.button("Click me!"):
        st.balloons()
        st.success("Button clicked!")

with col2:
    st.subheader("Checkbox")
    agree = st.checkbox("I agree to terms")
    if agree:
        st.success("Thank you for agreeing!")

with col3:
    st.subheader("Toggle")
    enabled = st.toggle("Enable feature")
    if enabled:
        st.info("Feature is enabled!")

st.divider()

# --- FILE UPLOAD ---
st.header("5. File Upload")

uploaded_file = st.file_uploader(
    "Choose a file:",
    type=["txt", "csv", "pdf", "png", "jpg"]
)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size} bytes")
    st.write(f"File type: {uploaded_file.type}")

st.divider()

# --- COLOR PICKER ---
st.header("6. Color Picker")

color = st.color_picker("Pick a color:", "#00f900")
st.write(f"Selected color: {color}")

# Display the color
st.markdown(
    f'<div style="background-color: {color}; padding: 20px; border-radius: 5px;">'
    f'<p style="color: white; text-align: center;">This box uses your selected color!</p>'
    f'</div>',
    unsafe_allow_html=True
)

st.divider()

# Summary
st.header("Summary")
st.info("""
These are the most commonly used Streamlit widgets. Each widget automatically
triggers a rerun of your app when its value changes, making your app interactive!

Try changing values above and watch how the app responds instantly.
""")
