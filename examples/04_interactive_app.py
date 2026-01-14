"""
Example 4: Interactive App
A complete interactive BMI calculator with visualization and recommendations.

To run:
    streamlit run 04_interactive_app.py
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="🏃",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .big-metric {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
    }
    .category-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🏃 BMI Calculator & Health Tracker")
st.markdown("Calculate your Body Mass Index and get personalized health recommendations")

st.divider()

# Sidebar - User Input
st.sidebar.header("📝 Your Information")

# Unit system selection
unit_system = st.sidebar.radio("Select unit system:", ["Metric (kg, cm)", "Imperial (lbs, inches)"])

# Input fields based on unit system
if unit_system == "Metric (kg, cm)":
    weight = st.sidebar.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
    height = st.sidebar.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.1)

    # Convert to standard units for calculation
    weight_kg = weight
    height_m = height / 100

else:  # Imperial
    weight_lbs = st.sidebar.number_input("Weight (lbs)", min_value=1.0, max_value=700.0, value=154.0, step=0.1)
    height_feet = st.sidebar.number_input("Height (feet)", min_value=1, max_value=8, value=5, step=1)
    height_inches = st.sidebar.number_input("Additional inches", min_value=0, max_value=11, value=7, step=1)

    # Convert to metric
    weight_kg = weight_lbs * 0.453592
    height_m = ((height_feet * 12) + height_inches) * 0.0254

# Additional information
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
activity_level = st.sidebar.select_slider(
    "Activity Level",
    options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
)

st.divider()

# Calculate BMI
def calculate_bmi(weight_kg, height_m):
    """Calculate BMI from weight and height."""
    return weight_kg / (height_m ** 2)

def get_bmi_category(bmi):
    """Determine BMI category."""
    if bmi < 18.5:
        return "Underweight", "🔵", "#3498db"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "🟢", "#2ecc71"
    elif 25 <= bmi < 30:
        return "Overweight", "🟡", "#f39c12"
    else:
        return "Obese", "🔴", "#e74c3c"

def get_recommendations(bmi, category):
    """Get health recommendations based on BMI category."""
    recommendations = {
        "Underweight": [
            "Increase caloric intake with nutrient-dense foods",
            "Focus on strength training exercises",
            "Consult with a nutritionist for a meal plan",
            "Eat more frequent, smaller meals throughout the day"
        ],
        "Normal weight": [
            "Maintain current healthy habits",
            "Continue regular physical activity",
            "Eat a balanced diet with variety",
            "Stay hydrated and get adequate sleep"
        ],
        "Overweight": [
            "Gradually reduce caloric intake",
            "Increase physical activity to 150+ minutes per week",
            "Focus on whole foods and reduce processed foods",
            "Consider consulting a healthcare professional"
        ],
        "Obese": [
            "Consult with a healthcare professional",
            "Create a structured weight loss plan",
            "Start with low-impact exercises like walking",
            "Consider working with a registered dietitian",
            "Set realistic, achievable goals"
        ]
    }
    return recommendations.get(category, [])

# Calculate BMI
bmi = calculate_bmi(weight_kg, height_m)
category, emoji, color = get_bmi_category(bmi)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Display BMI result
    st.header("📊 Your Results")

    # BMI value in a styled box
    st.markdown(f"""
        <div class="category-box" style="background-color: {color}; color: white;">
            BMI: {bmi:.1f}
        </div>
    """, unsafe_allow_html=True)

    # Category
    st.markdown(f"""
        <div style="text-align: center; font-size: 2rem; margin: 20px 0;">
            {emoji} {category}
        </div>
    """, unsafe_allow_html=True)

    # BMI Chart with indicator
    st.subheader("BMI Scale")

    fig = go.Figure()

    # Background zones
    fig.add_trace(go.Bar(
        x=['Underweight', 'Normal', 'Overweight', 'Obese'],
        y=[18.5, 6.5, 5, 10],  # Heights for visual representation
        marker_color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'],
        opacity=0.6,
        name='BMI Ranges',
        text=['< 18.5', '18.5-25', '25-30', '> 30'],
        textposition='inside'
    ))

    # User's BMI indicator
    if bmi < 18.5:
        x_pos = 0
    elif bmi < 25:
        x_pos = 1
    elif bmi < 30:
        x_pos = 2
    else:
        x_pos = 3

    fig.add_trace(go.Scatter(
        x=[x_pos],
        y=[bmi if bmi < 35 else 35],
        mode='markers+text',
        marker=dict(size=20, color='red', symbol='star'),
        text=[f'You: {bmi:.1f}'],
        textposition='top center',
        name='Your BMI'
    ))

    fig.update_layout(
        title='Your BMI on the Scale',
        xaxis_title='Category',
        yaxis_title='BMI Value',
        yaxis=dict(range=[0, 40]),
        showlegend=False,
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Health Metrics
    st.header("📈 Health Metrics")

    # Ideal weight range (for normal BMI)
    ideal_bmi_min = 18.5
    ideal_bmi_max = 25
    ideal_weight_min = ideal_bmi_min * (height_m ** 2)
    ideal_weight_max = ideal_bmi_max * (height_m ** 2)

    if unit_system == "Metric (kg, cm)":
        st.metric("Current Weight", f"{weight_kg:.1f} kg")
        st.metric("Ideal Weight Range", f"{ideal_weight_min:.1f} - {ideal_weight_max:.1f} kg")
    else:
        current_lbs = weight_kg / 0.453592
        ideal_min_lbs = ideal_weight_min / 0.453592
        ideal_max_lbs = ideal_weight_max / 0.453592
        st.metric("Current Weight", f"{current_lbs:.1f} lbs")
        st.metric("Ideal Weight Range", f"{ideal_min_lbs:.1f} - {ideal_max_lbs:.1f} lbs")

    # Weight to lose/gain
    if weight_kg < ideal_weight_min:
        weight_diff = ideal_weight_min - weight_kg
        st.metric("To Reach Normal BMI", f"+{weight_diff:.1f} kg" if unit_system.startswith("M") else f"+{weight_diff/0.453592:.1f} lbs")
    elif weight_kg > ideal_weight_max:
        weight_diff = weight_kg - ideal_weight_max
        st.metric("To Reach Normal BMI", f"-{weight_diff:.1f} kg" if unit_system.startswith("M") else f"-{weight_diff/0.453592:.1f} lbs")
    else:
        st.success("✅ You're in the healthy range!")

st.divider()

# Recommendations
st.header("💡 Personalized Recommendations")

recommendations = get_recommendations(bmi, category)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Action Items")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")

with col2:
    st.subheader("General Tips")
    st.markdown("""
    - **Exercise**: Aim for 150 minutes of moderate activity per week
    - **Nutrition**: Eat plenty of fruits, vegetables, and whole grains
    - **Hydration**: Drink 8 glasses of water daily
    - **Sleep**: Get 7-9 hours of quality sleep each night
    - **Stress**: Practice stress management techniques
    """)

st.divider()

# Progress Tracker
st.header("📅 Track Your Progress")

with st.expander("➕ Add Measurement"):
    st.markdown("Use the form below to track your BMI over time")

    col1, col2, col3 = st.columns(3)
    with col1:
        track_date = st.date_input("Date")
    with col2:
        track_weight = st.number_input("Weight", value=weight_kg)
    with col3:
        track_notes = st.text_input("Notes (optional)")

    if st.button("Save Measurement"):
        st.success("✅ Measurement saved! (Demo - not actually saved)")

# Sample progress chart
st.subheader("Weight Progress Chart (Sample)")
dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
sample_weights = np.linspace(weight_kg + 2, weight_kg, 30) + np.random.normal(0, 0.3, 30)
progress_df = pd.DataFrame({
    'Date': dates,
    'Weight': sample_weights
})

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=progress_df['Date'],
    y=progress_df['Weight'],
    mode='lines+markers',
    name='Weight',
    line=dict(color='blue', width=2)
))

# Add target line
fig.add_hline(
    y=ideal_weight_max,
    line_dash="dash",
    line_color="green",
    annotation_text="Target Weight"
)

fig.update_layout(
    title='Weight Progress (Sample Data)',
    xaxis_title='Date',
    yaxis_title='Weight (kg)',
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Educational content
st.header("ℹ️ About BMI")

with st.expander("What is BMI?"):
    st.markdown("""
    **Body Mass Index (BMI)** is a measure of body fat based on height and weight.

    **Formula:**
    ```
    BMI = weight (kg) / [height (m)]²
    ```

    **Categories:**
    - Underweight: BMI < 18.5
    - Normal weight: BMI 18.5-24.9
    - Overweight: BMI 25-29.9
    - Obese: BMI ≥ 30

    **Limitations:**
    BMI doesn't distinguish between muscle and fat, so it may not be accurate for:
    - Athletes with high muscle mass
    - Elderly with reduced muscle mass
    - Pregnant women
    - Growing children
    """)

with st.expander("Disclaimer"):
    st.warning("""
    ⚠️ **Important:** This BMI calculator is for informational purposes only and should
    not replace professional medical advice. Always consult with a healthcare provider
    for personalized health recommendations.
    """)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        Made with ❤️ using Streamlit | BMI Calculator v1.0
    </div>
""", unsafe_allow_html=True)
