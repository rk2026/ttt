import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import geopandas as gpd
from shapely.geometry import Point, box
import math

def main():
    st.title("ट्री भोलुम क्यालकुलेटर (TVC 1.0)")

    # Template data
    tdata = {
        'TID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        'species': ['Row Labels', 'Abies spp', 'Acacia catechu', 'Adino cordifolia', 'Albizia spp',
                    'Alnus nepalensis', 'Anogeissus latifolia', 'Bambax ceiba', 'Cedrela toona',
                    'Dalbergia sissoo', 'Eugenia Jambolana', 'Hill spp', 'Hymenodictyon excelsum',
                    'Lagerstroenia parviflora', 'Michelia champaca', 'Pinus roxburghii',
                    'Pinus wallichiana', 'Quercus spp', 'Schima wallichii', 'Shorea robusta',
                    'Terai spp', 'Terminalia alata', 'Trewia nudiflora', 'Tsuga spp'],
        # ... rest of the template data
    }

    tdf = pd.DataFrame(tdata)
    st.dataframe(tdf)

    # Download template
    @st.cache_data
    def convert_df_to_csv(tdf):
        return tdf.to_csv(index=False).encode('utf-8')

    csv_data = convert_df_to_csv(tdf)
    st.download_button(
        label="Download Data as template CSV",
        data=csv_data,
        file_name='tree_data_template.csv',
        mime='text/csv'
    )

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Species data
        species_data = {
            'SN': range(1, 26),
            'scientific_name': ['Abies spp', 'Acacia catechu', 'Adino cordifolia', 'Albizia spp', 'Alnus nepalensis',
                                'Anogeissus latifolia', 'Bambax ceiba', 'Cedrela toona', 'Dalbergia sissoo',
                                'Eugenia Jambolana', 'Hymenodictyon excelsum', 'Lagerstroenia parviflora',
                                'Michelia champaca', 'Pinus roxburghii', 'Pinus wallichiana', 'Quercus spp',
                                'Schima wallichii', 'Shorea robusta', 'Terminalia alata', 'Trewia nudiflora',
                                'Tsuga spp', 'Terai spp', 'Hill spp', 'Coniferious', 'Broadleaved'],
            # ... rest of the species data
        }

        sppVal = pd.DataFrame(species_data)
        joined_df = df.merge(sppVal, left_on='species', right_on='scientific_name')

        # Calculate tree volumes
        def add_calculated_columns(df):
            # ... volume calculation formulas
            return df

        result_df = add_calculated_columns(joined_df)
        result_df = result_df.drop(columns=['SN', 'scientific_name', 'a', 'b', 'c', 'a1', 'b1', 's', 'm', 'bg'])
        st.write("Analysis Table:")
        st.dataframe(result_df)

        # Spatial analysis and visualization
        result_df['geometry'] = result_df.apply(lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1)
        result_gdf = gpd.GeoDataFrame(result_df, geometry='geometry', crs='epsg:4326')

        # Get bounding box and create grid
        xmin, ymin, xmax, ymax = result_gdf.total_bounds
        bounding_polygon = box(xmin, ymin, xmax, ymax)
        bounding_gdf = gpd.GeoDataFrame(geometry=[bounding_polygon], crs=result_gdf.crs)
                                        
        # ... rest of the bounding box and grid creation code ...

        # Spatial join and visualization
        intersected_grid_indices = gpd.sjoin(grid_gdf, result_gdf, how='inner', predicate='intersects').index.unique()
        selected_polygons_gdf = grid_gdf[grid_gdf.index.isin(intersected_grid_indices)].reset_index(drop=True)

        st.map(selected_polygons_gdf)
        st.map(result_gdf)

if __name__ == "__main__":
    main()
