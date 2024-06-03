import streamlit as st

def multiselect(title,list):
    selected = st.sidebar.multiselect(title, list)
    all = st.sidebar.checkbox("Select all",value=True,key = title)
    if all:
        value = list
    else:
        value = selected
    return value


# Define the function to generate grid cells
def generate_grid(lat_min, lat_max, lon_min, lon_max, cell_size):
    grid = []
    cell_size = cell_size * 10
    lat_step = max(int(cell_size), 1)  # Multiply by 10 to handle decimal steps
    lon_step = max(int(cell_size), 1)
    
    lat_range = range(int(lat_min * 10), int(lat_max * 10) + 1, lat_step)
    lon_range = range(int(lon_min * 10), int(lon_max * 10) + 1, lon_step)
    
    for lat in lat_range:
        for lon in lon_range:
            grid.append((lat/10, (lat + cell_size)/10, lon/10, (lon + cell_size)/10))
    
    return grid

# Finding grid end points
def find_grid(coordinate, grid_endpoints):
    lat, lon = coordinate
    for grid in grid_endpoints:
        lat_min, lat_max, lon_min, lon_max = grid
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return grid
    return None