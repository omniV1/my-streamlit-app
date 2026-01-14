"""
Example 5: Advanced Features
Demonstrates caching, session state, layouts, and performance optimization.

To run:
    streamlit run 05_advanced_features.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Advanced Streamlit Features",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🚀 Advanced Streamlit Features")
st.markdown("Learn about caching, session state, and performance optimization")

st.divider()

# Create tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗄️ Caching",
    "💾 Session State",
    "📐 Layouts",
    "⚡ Performance",
    "🎨 Advanced UI"
])

# ===== TAB 1: CACHING =====
with tab1:
    st.header("🗄️ Data Caching")
    st.markdown("""
    Caching prevents expensive computations from running on every interaction.
    Streamlit provides two main caching decorators:
    - `@st.cache_data` - For data (DataFrames, arrays, etc.)
    - `@st.cache_resource` - For resources (ML models, database connections)
    """)

    st.subheader("Demo: With vs Without Caching")

    col1, col2 = st.columns(2)

    # WITHOUT CACHING
    with col1:
        st.markdown("**❌ Without Caching**")

        def load_data_no_cache(n_rows):
            """Simulate expensive data loading (no cache)."""
            time.sleep(2)  # Simulate delay
            return pd.DataFrame({
                'A': np.random.randn(n_rows),
                'B': np.random.randn(n_rows),
                'C': np.random.randn(n_rows)
            })

        if st.button("Load Data (No Cache)", key="no_cache"):
            with st.spinner("Loading... this takes 2 seconds every time"):
                start = time.time()
                df_no_cache = load_data_no_cache(1000)
                elapsed = time.time() - start
                st.success(f"Loaded in {elapsed:.2f} seconds")
                st.dataframe(df_no_cache.head())
                st.warning("⚠️ Click again - it will take 2 seconds every time!")

    # WITH CACHING
    with col2:
        st.markdown("**✅ With Caching**")

        @st.cache_data
        def load_data_cached(n_rows):
            """Simulate expensive data loading (with cache)."""
            time.sleep(2)  # Simulate delay
            return pd.DataFrame({
                'A': np.random.randn(n_rows),
                'B': np.random.randn(n_rows),
                'C': np.random.randn(n_rows)
            })

        if st.button("Load Data (Cached)", key="cached"):
            with st.spinner("Loading... (only slow the first time)"):
                start = time.time()
                df_cached = load_data_cached(1000)
                elapsed = time.time() - start
                st.success(f"Loaded in {elapsed:.2f} seconds")
                st.dataframe(df_cached.head())
                st.info("✨ Click again - it's instant now!")

    st.divider()

    # Cache examples
    st.subheader("📚 Caching Examples")

    with st.expander("Example 1: Cache Data"):
        st.code("""
@st.cache_data
def load_csv_data(filename):
    \"\"\"Cache CSV data loading.\"\"\"
    return pd.read_csv(filename)

# First call: reads from disk (slow)
# Subsequent calls: returns cached data (fast)
df = load_csv_data('data.csv')
        """, language='python')

    with st.expander("Example 2: Cache with Parameters"):
        st.code("""
@st.cache_data
def filter_data(df, category, min_value):
    \"\"\"Cache is separate for each combination of parameters.\"\"\"
    return df[(df['category'] == category) & (df['value'] > min_value)]

# Different parameters = different cache
df1 = filter_data(data, 'A', 10)  # Cached separately
df2 = filter_data(data, 'B', 20)  # Different cache
        """, language='python')

    with st.expander("Example 3: Cache Resources (ML Models)"):
        st.code("""
@st.cache_resource
def load_model():
    \"\"\"Cache expensive resources like ML models.\"\"\"
    # This only loads once, even across sessions
    model = load_my_ml_model()
    return model

# Model is loaded once and reused
model = load_model()
predictions = model.predict(input_data)
        """, language='python')

# ===== TAB 2: SESSION STATE =====
with tab2:
    st.header("💾 Session State")
    st.markdown("""
    Session state allows you to store variables that persist across reruns.
    Perfect for maintaining state in interactive apps.
    """)

    st.subheader("Demo: Counter Example")

    # Initialize session state
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    if 'history' not in st.session_state:
        st.session_state.history = []

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Increment"):
            st.session_state.counter += 1
            st.session_state.history.append(('increment', datetime.now()))

    with col2:
        if st.button("➖ Decrement"):
            st.session_state.counter -= 1
            st.session_state.history.append(('decrement', datetime.now()))

    with col3:
        if st.button("🔄 Reset"):
            st.session_state.counter = 0
            st.session_state.history = []

    st.markdown(f"### Current Count: `{st.session_state.counter}`")

    # Show history
    if st.session_state.history:
        with st.expander("View History"):
            for action, timestamp in st.session_state.history[-10:]:
                st.text(f"{timestamp.strftime('%H:%M:%S')} - {action}")

    st.divider()

    # Shopping cart example
    st.subheader("Demo: Shopping Cart")

    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # Product selection
    products = {
        'Apple': 1.50,
        'Banana': 0.75,
        'Orange': 1.25,
        'Milk': 3.50,
        'Bread': 2.00
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_product = st.selectbox("Select product:", list(products.keys()))
        quantity = st.number_input("Quantity:", min_value=1, max_value=10, value=1)

        if st.button("🛒 Add to Cart"):
            st.session_state.cart.append({
                'product': selected_product,
                'quantity': quantity,
                'price': products[selected_product]
            })
            st.success(f"Added {quantity}x {selected_product} to cart!")

    with col2:
        st.markdown("**🛒 Your Cart**")
        if st.session_state.cart:
            total = 0
            for item in st.session_state.cart:
                subtotal = item['quantity'] * item['price']
                total += subtotal
                st.text(f"{item['quantity']}x {item['product']}: ${subtotal:.2f}")

            st.markdown(f"**Total: ${total:.2f}**")

            if st.button("🗑️ Clear Cart"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.info("Cart is empty")

    st.divider()

    # Code examples
    st.subheader("📚 Session State Examples")

    with st.expander("Example: Form with Persistence"):
        st.code("""
# Initialize
if 'form_data' not in st.session_state:
    st.session_state.form_data = {'name': '', 'email': ''}

# Store form data
st.session_state.form_data['name'] = st.text_input(
    "Name",
    value=st.session_state.form_data['name']
)

# Data persists even if user navigates away and comes back
        """, language='python')

# ===== TAB 3: LAYOUTS =====
with tab3:
    st.header("📐 Advanced Layouts")

    st.subheader("1. Columns")
    st.markdown("Create side-by-side content")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.info("Column 1\n(ratio: 1)")
    with col2:
        st.success("Column 2\n(ratio: 2)")
    with col3:
        st.warning("Column 3\n(ratio: 1)")

    st.divider()

    st.subheader("2. Expanders")
    st.markdown("Collapsible content sections")

    with st.expander("Click to expand"):
        st.write("This content is hidden by default")
        st.line_chart(np.random.randn(20, 3))

    st.divider()

    st.subheader("3. Containers")
    st.markdown("Group elements together")

    container = st.container()
    st.write("This is outside the container")

    container.write("This is inside the container")
    container.line_chart(np.random.randn(10, 2))

    st.divider()

    st.subheader("4. Sidebar")
    st.markdown("Persistent side panel (see left sidebar)")

    # Add content to sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Sidebar Demo")
    st.sidebar.write("This stays visible on all pages")
    sidebar_value = st.sidebar.slider("Sidebar slider", 0, 100, 50)
    st.write(f"Sidebar slider value: {sidebar_value}")

    st.divider()

    st.subheader("5. Empty Placeholders")
    st.markdown("Update content dynamically")

    placeholder = st.empty()

    if st.button("Start Animation"):
        for i in range(10):
            placeholder.metric("Progress", f"{i+1}/10")
            time.sleep(0.3)
        placeholder.success("✅ Complete!")

# ===== TAB 4: PERFORMANCE =====
with tab4:
    st.header("⚡ Performance Optimization")

    st.subheader("1. Use st.cache_data for Expensive Operations")
    st.code("""
@st.cache_data
def expensive_computation(data):
    # Cached - only runs once per unique input
    return process_data(data)
    """, language='python')

    st.subheader("2. Avoid Recomputing in Loops")
    st.markdown("**❌ Bad:**")
    st.code("""
# This recalculates sum on every loop iteration
for item in items:
    if item > sum(all_items):  # Expensive!
        process(item)
    """, language='python')

    st.markdown("**✅ Good:**")
    st.code("""
# Calculate once, reuse
total = sum(all_items)
for item in items:
    if item > total:  # Fast!
        process(item)
    """, language='python')

    st.subheader("3. Use Session State to Avoid Re-initialization")
    st.code("""
# Only initialize once
if 'model' not in st.session_state:
    st.session_state.model = load_expensive_model()

# Reuse across reruns
predictions = st.session_state.model.predict(data)
    """, language='python')

    st.subheader("4. Limit DataFrame Size for Display")
    st.code("""
# Show only first N rows
st.dataframe(df.head(100))  # Instead of entire df

# Or use pagination
page_size = 50
page = st.number_input('Page', 1, len(df)//page_size)
st.dataframe(df.iloc[(page-1)*page_size:page*page_size])
    """, language='python')

    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Cache Hit Rate", "98%", "+2%")
    col2.metric("Avg Response Time", "120ms", "-30ms")
    col3.metric("Memory Usage", "45MB", "-5MB")

# ===== TAB 5: ADVANCED UI =====
with tab5:
    st.header("🎨 Advanced UI Elements")

    st.subheader("1. Status Elements")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("Success message")
        st.info("Info message")
    with col2:
        st.warning("Warning message")
        st.error("Error message")
    with col3:
        st.exception(ValueError("Example exception"))

    st.divider()

    st.subheader("2. Progress Indicators")

    if st.button("Show Progress"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Processing: {i+1}%")
            time.sleep(0.01)

        status_text.text("Complete!")

    st.divider()

    st.subheader("3. Spinners")

    if st.button("Show Spinner"):
        with st.spinner("Processing..."):
            time.sleep(2)
        st.success("Done!")

    st.divider()

    st.subheader("4. Balloons and Snow")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎈 Balloons"):
            st.balloons()
    with col2:
        if st.button("❄️ Snow"):
            st.snow()

    st.divider()

    st.subheader("5. Custom HTML/CSS")

    st.markdown("""
        <style>
        .custom-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        </style>
        <div class="custom-box">
            Custom Styled Box with Gradient!
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("6. Download Buttons")

    # Text download
    text_data = "This is sample text data"
    st.download_button(
        label="📥 Download Text",
        data=text_data,
        file_name="sample.txt",
        mime="text/plain"
    )

    # CSV download
    df_download = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    csv = df_download.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv"
    )

# Sidebar content
st.sidebar.header("🎯 Learning Goals")
st.sidebar.markdown("""
After this tutorial, you should understand:

✅ How to cache expensive operations
✅ Using session state for persistence
✅ Creating advanced layouts
✅ Optimizing app performance
✅ Building professional UIs
""")

st.sidebar.divider()
st.sidebar.info("💡 Tip: Inspect the source code to see how these features are implemented!")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666;">
        🚀 Advanced Streamlit Features Demo | Made with ❤️
    </div>
""", unsafe_allow_html=True)
