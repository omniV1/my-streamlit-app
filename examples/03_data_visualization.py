"""
Example 3: Data Visualization
Demonstrates various chart types and data visualization in Streamlit.

To run:
    streamlit run 03_data_visualization.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Data Visualization Demo",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Data Visualization with Streamlit")
st.markdown("Explore different types of charts and visualizations")

# Generate sample data
@st.cache_data
def generate_data():
    """Generate sample datasets for visualization."""
    np.random.seed(42)

    # Time series data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    time_series = pd.DataFrame({
        'Date': dates,
        'Sales': np.cumsum(np.random.randn(100)) + 100,
        'Revenue': np.cumsum(np.random.randn(100)) + 150,
        'Profit': np.cumsum(np.random.randn(100)) + 80
    })

    # Category data
    categories = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E'],
        'Value': np.random.randint(10, 100, 5),
        'Count': np.random.randint(5, 50, 5)
    })

    # Scatter data
    scatter_data = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'category': np.random.choice(['Group 1', 'Group 2', 'Group 3'], 100)
    })

    return time_series, categories, scatter_data

time_series, categories, scatter_data = generate_data()

# Sidebar options
st.sidebar.header("Visualization Options")
chart_type = st.sidebar.selectbox(
    "Select Chart Type:",
    ["Line Chart", "Bar Chart", "Area Chart", "Scatter Plot",
     "Histogram", "Heatmap", "3D Surface", "All Charts"]
)

st.divider()

# --- LINE CHART ---
if chart_type in ["Line Chart", "All Charts"]:
    st.header("1. Line Chart")
    st.markdown("Great for showing trends over time")

    col1, col2 = st.columns([3, 1])

    with col1:
        # Streamlit native line chart
        st.subheader("Native Streamlit Line Chart")
        st.line_chart(time_series.set_index('Date')[['Sales', 'Revenue', 'Profit']])

    with col2:
        st.subheader("Options")
        show_sales = st.checkbox("Sales", value=True, key="line_sales")
        show_revenue = st.checkbox("Revenue", value=True, key="line_revenue")
        show_profit = st.checkbox("Profit", value=True, key="line_profit")

    # Plotly interactive line chart
    st.subheader("Interactive Plotly Line Chart")
    fig = go.Figure()

    if show_sales:
        fig.add_trace(go.Scatter(x=time_series['Date'], y=time_series['Sales'],
                                 mode='lines', name='Sales'))
    if show_revenue:
        fig.add_trace(go.Scatter(x=time_series['Date'], y=time_series['Revenue'],
                                 mode='lines', name='Revenue'))
    if show_profit:
        fig.add_trace(go.Scatter(x=time_series['Date'], y=time_series['Profit'],
                                 mode='lines', name='Profit'))

    fig.update_layout(title='Time Series Data', xaxis_title='Date', yaxis_title='Value')
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

# --- BAR CHART ---
if chart_type in ["Bar Chart", "All Charts"]:
    st.header("2. Bar Chart")
    st.markdown("Perfect for comparing categories")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Native Streamlit Bar Chart")
        st.bar_chart(categories.set_index('Category')['Value'])

    with col2:
        st.subheader("Plotly Bar Chart")
        fig = px.bar(categories, x='Category', y='Value',
                     title='Category Values',
                     color='Value',
                     color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

# --- AREA CHART ---
if chart_type in ["Area Chart", "All Charts"]:
    st.header("3. Area Chart")
    st.markdown("Shows cumulative totals over time")

    st.subheader("Native Streamlit Area Chart")
    st.area_chart(time_series.set_index('Date')[['Sales', 'Revenue']])

    st.divider()

# --- SCATTER PLOT ---
if chart_type in ["Scatter Plot", "All Charts"]:
    st.header("4. Scatter Plot")
    st.markdown("Reveals relationships between variables")

    col1, col2 = st.columns([3, 1])

    with col1:
        fig = px.scatter(
            scatter_data,
            x='x',
            y='y',
            color='category',
            title='Scatter Plot with Categories',
            labels={'x': 'X Values', 'y': 'Y Values'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Statistics")
        st.metric("Total Points", len(scatter_data))
        st.metric("Groups", scatter_data['category'].nunique())
        st.metric("Correlation", f"{scatter_data['x'].corr(scatter_data['y']):.3f}")

    st.divider()

# --- HISTOGRAM ---
if chart_type in ["Histogram", "All Charts"]:
    st.header("5. Histogram")
    st.markdown("Shows distribution of values")

    col1, col2 = st.columns([3, 1])

    with col1:
        bins = st.slider("Number of bins:", 10, 50, 30, key="hist_bins")

        fig = px.histogram(
            scatter_data,
            x='x',
            nbins=bins,
            title='Distribution of X Values',
            marginal='box'  # Adds a box plot above
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribution Stats")
        st.metric("Mean", f"{scatter_data['x'].mean():.3f}")
        st.metric("Std Dev", f"{scatter_data['x'].std():.3f}")
        st.metric("Min", f"{scatter_data['x'].min():.3f}")
        st.metric("Max", f"{scatter_data['x'].max():.3f}")

    st.divider()

# --- HEATMAP ---
if chart_type in ["Heatmap", "All Charts"]:
    st.header("6. Heatmap")
    st.markdown("Visualizes matrix data with colors")

    # Create correlation matrix
    corr_data = pd.DataFrame(
        np.random.randn(10, 10),
        columns=[f'Feature {i+1}' for i in range(10)]
    )
    corr_matrix = corr_data.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 8}
    ))

    fig.update_layout(title='Correlation Heatmap', width=700, height=700)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

# --- 3D SURFACE ---
if chart_type in ["3D Surface", "All Charts"]:
    st.header("7. 3D Surface Plot")
    st.markdown("Visualizes 3D data surfaces")

    # Generate 3D surface data
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='viridis')])
    fig.update_layout(
        title='3D Surface: sin(√(x² + y²))',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

# Data table
st.header("📋 Raw Data")

tab1, tab2, tab3 = st.tabs(["Time Series", "Categories", "Scatter Data"])

with tab1:
    st.dataframe(time_series, use_container_width=True)

with tab2:
    st.dataframe(categories, use_container_width=True)

with tab3:
    st.dataframe(scatter_data, use_container_width=True)

# Summary
st.divider()
st.success("""
💡 **Key Takeaways:**
- Streamlit has built-in charts (`st.line_chart`, `st.bar_chart`, etc.) for quick visualization
- Plotly provides interactive charts with zoom, pan, and hover capabilities
- Use `@st.cache_data` to cache expensive data generation
- Charts automatically resize with `use_container_width=True`
""")
