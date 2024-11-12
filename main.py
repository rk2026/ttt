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
    'SN': range(1, 26),
    'scientific_name': ['Abies spp', 'Acacia catechu', 'Adina cardifolia', 'Albizia spp', 'Alnus nepalensis',
                       'Anogeissus latifolia', 'Bombax ceiba', 'Cedrela toona', 'Dalbergia sissoo',
                       'Eugenia Jambolana', 'Hymenodictyon excelsum', 'Lagerstroemia parviflora',
                       'Michelia champaca', 'Pinus roxburghii', 'Pinus wallichiana', 'Quercus spp',
                       'Schima wallichii', 'Shorea robusta', 'Terminalia alata', 'Trewia nudiflora',
                       'Tsuga spp', 'Terai spp', 'Hill spp', 'Coniferious', 'Broadleaved'],
    'a': [-2.4453, -2.3256, -2.5626, -2.4284, -2.7761, -2.272, -2.3856, -2.1832, -2.1959, -2.5693,
          -2.585, -2.3411, -2.0152, -2.977, -2.8195, -2.36, -2.7385, -2.4554, -2.4616, -2.4585,
          -2.5293, -2.3993, -2.3204, None, None],
    'b': [1.722, 1.6476, 1.8598, 1.7609, 1.9006, 1.7499, 1.7414, 1.8679, 1.6567, 1.8816,
          1.9437, 1.7246, 1.8555, 1.9235, 1.725, 1.968, 1.8155, 1.9026, 1.8497, 1.8043,
          1.7815, 1.7836, 1.8507, None, None],
    'c': [1.0757, 1.0552, 0.8783, 0.9662, 0.9428, 0.9174, 1.0063, 0.7569, 0.9899, 0.8498,
          0.7902, 0.9702, 0.763, 1.0019, 1.1623, 0.7496, 1.0072, 0.8352, 0.88, 0.922,
          1.0369, 0.9546, 0.8223, None, None],
    'a1': [5.4433, 5.4401, 5.4681, 4.4031, 6.019, 4.9502, 4.5554, 4.9705, 4.358, 5.1749,
           5.5572, 5.3349, 3.3499, 6.2696, 5.7216, 4.8511, 7.4617, 5.2026, 4.5968, 5.3475,
           5.2774, 4.8991, 5.5323, None, None],
    'b1': [-2.6902, -2.491, -2.491, -2.2094, -2.7271, -2.3353, -2.3009, -2.3436, -2.1559, -2.3636,
           -2.496, -2.4428, -2.0161, -2.8252, -2.6788, -2.4494, -3.0676, -2.4788, -2.2305, -2.4774,
           -2.6483, -2.3406, -2.4815, None, None],
    's': [0.436, 0.443, 0.443, 0.443, 0.803, 0.443, 0.443, 0.443, 0.684, 0.443,
          0.443, 0.443, 0.443, 0.189, 0.683, 0.747, 0.52, 0.055, 0.443, 0.443,
          0.443, 0.443, 0.443, 0.436, 0.443],
    'm': [0.372, 0.511, 0.511, 0.511, 1.226, 0.511, 0.511, 0.511, 0.684, 0.511,
          0.511, 0.511, 0.511, 0.256, 0.488, 0.96, 0.186, 0.341, 0.511, 0.511,
          0.511, 0.511, 0.511, 0.372, 0.511],
    'bg': [0.355, 0.71, 0.71, 0.71, 1.51, 0.71, 0.71, 0.71, 0.684, 0.71,
           0.71, 0.71, 0.71, 0.3, 0.41, 1.06, 0.168, 0.357, 0.71, 0.71,
           0.71, 0.71, 0.71, 0.355, 0.71],
    'Local_Name': ['Thingre Salla', 'Khayar', 'Karma', 'Siris', 'Uttis', 'Banjhi', 'Simal', 'Tooni',
                   'Sissoo', 'Jamun', 'Bhudkul', 'Botdhayero', 'Chanp', 'Khote Salla', 'Gobre Salla',
                   'Kharsu', 'Chilaune', 'Sal', 'Saj', 'Gamhari', 'Dhupi Salla', 'Terai Spp',
                   'Hill spp', None, None]
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
    'scientific_name': ['Abies spp', 'Acacia catechu', 'Adina cardifolia', 'Albizia spp', 'Alnus nepalensis',
                       'Anogeissus latifolia', 'Bombax ceiba', 'Cedrela toona', 'Dalbergia sissoo',
                       'Eugenia Jambolana', 'Hymenodictyon excelsum', 'Lagerstroemia parviflora',
                       'Michelia champaca', 'Pinus roxburghii', 'Pinus wallichiana', 'Quercus spp',
                       'Schima wallichii', 'Shorea robusta', 'Terminalia alata', 'Trewia nudiflora',
                       'Tsuga spp', 'Terai spp', 'Hill spp', 'Coniferious', 'Broadleaved'],
    'a': [-2.4453, -2.3256, -2.5626, -2.4284, -2.7761, -2.272, -2.3856, -2.1832, -2.1959, -2.5693,
          -2.585, -2.3411, -2.0152, -2.977, -2.8195, -2.36, -2.7385, -2.4554, -2.4616, -2.4585,
          -2.5293, -2.3993, -2.3204, None, None],
    'b': [1.722, 1.6476, 1.8598, 1.7609, 1.9006, 1.7499, 1.7414, 1.8679, 1.6567, 1.8816,
          1.9437, 1.7246, 1.8555, 1.9235, 1.725, 1.968, 1.8155, 1.9026, 1.8497, 1.8043,
          1.7815, 1.7836, 1.8507, None, None],
    'c': [1.0757, 1.0552, 0.8783, 0.9662, 0.9428, 0.9174, 1.0063, 0.7569, 0.9899, 0.8498,
          0.7902, 0.9702, 0.763, 1.0019, 1.1623, 0.7496, 1.0072, 0.8352, 0.88, 0.922,
          1.0369, 0.9546, 0.8223, None, None],
    'a1': [5.4433, 5.4401, 5.4681, 4.4031, 6.019, 4.9502, 4.5554, 4.9705, 4.358, 5.1749,
           5.5572, 5.3349, 3.3499, 6.2696, 5.7216, 4.8511, 7.4617, 5.2026, 4.5968, 5.3475,
           5.2774, 4.8991, 5.5323, None, None],
    'b1': [-2.6902, -2.491, -2.491, -2.2094, -2.7271, -2.3353, -2.3009, -2.3436, -2.1559, -2.3636,
           -2.496, -2.4428, -2.0161, -2.8252, -2.6788, -2.4494, -3.0676, -2.4788, -2.2305, -2.4774,
           -2.6483, -2.3406, -2.4815, None, None],
    's': [0.436, 0.443, 0.443, 0.443, 0.803, 0.443, 0.443, 0.443, 0.684, 0.443,
          0.443, 0.443, 0.443, 0.189, 0.683, 0.747, 0.52, 0.055, 0.443, 0.443,
          0.443, 0.443, 0.443, 0.436, 0.443],
    'm': [0.372, 0.511, 0.511, 0.511, 1.226, 0.511, 0.511, 0.511, 0.684, 0.511,
          0.511, 0.511, 0.511, 0.256, 0.488, 0.96, 0.186, 0.341, 0.511, 0.511,
          0.511, 0.511, 0.511, 0.372, 0.511],
    'bg': [0.355, 0.71, 0.71, 0.71, 1.51, 0.71, 0.71, 0.71, 0.684, 0.71,
           0.71, 0.71, 0.71, 0.3, 0.41, 1.06, 0.168, 0.357, 0.71, 0.71,
           0.71, 0.71, 0.71, 0.355, 0.71],
    'Local_Name': ['Thingre Salla', 'Khayar', 'Karma', 'Siris', 'Uttis', 'Banjhi', 'Simal', 'Tooni',
                   'Sissoo', 'Jamun', 'Bhudkul', 'Botdhayero', 'Chanp', 'Khote Salla', 'Gobre Salla',
                   'Kharsu', 'Chilaune', 'Sal', 'Saj', 'Gamhari', 'Dhupi Salla', 'Terai Spp',
                   'Hill spp', None, None]
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
