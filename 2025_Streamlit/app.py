import streamlit as st
import pandas as pd
import plotly.express as px

# Basic app title
st.title("My First Streamlit App")

# Simple text
st.write("Hello! This is a basic Streamlit app.")

# File uploader
st.subheader("Upload your CSV file")
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

# Display the data if file is uploaded
if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file)
    
    st.success(f"File uploaded successfully! Found {len(df)} rows.")
    
    # Display the table
    st.subheader("Data Preview")
    st.dataframe(df)
    
    # Show some basic info
    st.subheader("Data Information")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Rows", len(df))
    with col2:
        st.metric("Number of Columns", len(df.columns))
    
    # Display column names
    st.subheader("Column Names")
    st.write(df.columns.tolist())
    
    # Filter section
    st.subheader("Filter Data")
    
    # Select column to filter on
    filter_column = st.selectbox("Select column to filter", df.columns)
    
    # Get unique values from the selected column
    unique_values = df[filter_column].unique()
    
    # Multi-select for filtering
    selected_values = st.multiselect(
        f"Select values from '{filter_column}'",
        options=unique_values,
        default=unique_values.tolist()
    )
    
    # Filter the dataframe
    if selected_values:
        filtered_df = df[df[filter_column].isin(selected_values)]
        st.success(f"Showing {len(filtered_df)} rows after filtering")
        st.dataframe(filtered_df)
        
        # Plotting section
        st.subheader("Visualize Data")
        
        # Chart type selection
        chart_type = st.selectbox(
            "Select chart type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("Select X-axis", filtered_df.columns)
        
        with col2:
            # For some charts we need Y-axis
            if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
                y_axis = st.selectbox("Select Y-axis", filtered_df.columns)
        
        # Generate plot button
        if st.button("Generate Plot", type="primary"):
            try:
                if chart_type == "Bar Chart":
                    fig = px.bar(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                elif chart_type == "Line Chart":
                    fig = px.line(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                elif chart_type == "Histogram":
                    fig = px.histogram(filtered_df, x=x_axis, title=f"Distribution of {x_axis}")
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating plot: {str(e)}")
                st.info("Try selecting different columns or check if the data types are compatible.")
    else:
        st.warning("No values selected. Please select at least one value.")
else:
    st.info("Please upload a CSV file to get started.")