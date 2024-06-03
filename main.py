import streamlit as st
st.set_page_config(layout="wide")
import Preprocessor
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

df = pd.read_excel("OGIC_Lat_Long_Data_by_Comany(Equinor_Repsol_Petronas).xlsx", sheet_name = "Others")
df_eq = pd.read_excel("output_eq.xlsx")

# Main Page Navigation
Analysis = option_menu("Select your Visualization",
                    ["Locate oilwells", "Risk evaluation"],icons=["geo-alt-fill", "graph-up"], menu_icon="graph-up-arrow",default_index=0,
                    orientation="horizontal", styles={"container": {"padding": "5px", "background-color": "#fafafa"},
                            "icon": {"color": "orange", "font-size": "20px"},
                            "nav-link": {
                                "font-size": "13px",
                                "text-align": "left",
                                "margin": "25px",
                                "--hover-color": "#eee"}})

if Analysis == "Locate oilwells":
    company = Preprocessor.multiselect("Select company", df["CompanyName"].unique().tolist())
    df_company = df[df["CompanyName"].isin(company)]
    region = Preprocessor.multiselect("Select region", df_company["Region"].unique().tolist())
    df_region = df_company[df_company["Region"].isin(region)]
    country = Preprocessor.multiselect("Select country", df_region["Country"].unique().tolist())
    df_country = df_region[df_region["Country"].isin(country)]
    fig = px.scatter_geo(
    df_country, 
    lat='Latitude', 
    lon='Longitude', 
    hover_name='AssetName',  # Assuming there's a column with well names
    hover_data=['Latitude', 'Longitude'],  
    height=800)

    # Set the mapbox style
    fig.update_layout(mapbox_style="open-street-map")
    # fig.update_layout(mapbox_style="open-street-map", title=f"Oil Wells of {company} in {country}")
    st.plotly_chart(fig)
    # Checking the grid score
    # Title of the app
    st.title("Enter lat long")
    
    # Creating two columns for side-by-side input fields
    col1, col2 = st.columns(2)
    # Input fields for latitude and longitude in separate columns
    with col1:
        latitude = st.text_input("Enter the latitude:")
    with col2:
        longitude = st.text_input("Enter the longitude:")
    # Displaying the input values
    if st.button("Submit"):
        lat_min = 24.396308 
        lat_max = 49.384358 
        lon_min = -125.0 
        lon_max = -66.93457 
        cell_size = 0.3
        grid = Preprocessor.generate_grid(lat_min, lat_max, lon_min, lon_max, cell_size)
        grid_ends = Preprocessor.find_grid((float(latitude),float(longitude)), grid)
        if grid_ends == None:
            st.write("Data not available")
        else:
            plot_data = df_eq[df_eq["grid_keys"] == str(grid_ends)].groupby("Year").sum().reset_index()[["Year","EAL"]]
            # Create line chart
            fig = px.line(plot_data, x='Year', y='EAL', title='Year wise earthquake trend')
            st.plotly_chart(fig)
# Risk Evaluation
if Analysis == "Risk evaluation":
    flourish_code = """
    <div class="flourish-embed flourish-map" data-src="visualisation/18061267">
        <script src="https://public.flourish.studio/resources/embed.js"></script>
    </div>
    """
    # Embed the Flourish visualization
    components.html(flourish_code, height=600)  # Adjust the height as needed

