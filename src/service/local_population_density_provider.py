import h3
import tifffile as tf
from geopandas import GeoDataFrame, read_file, GeoSeries
from pandas import Series
from shapely.geometry import Point, box

from src.domain.spi.population_density_provider import PopulationDensityProvider

context = {"TOULOUSE":
               {'submap_id': 'R4_C19',
                'bbox': (3580662.888602, 2289403.270429, 3681769.211934, 2351279.165762)},
           "PRAGUE":
               {'submap_id': 'R4_C20',
                'bbox': (4595071.764692, 2977001.128320, 4710012.448128, 3057471.439286)},
           "A_CORUNA":
               {'submap_id': 'R4_C18',
                'bbox': (2809305.829661, 2414692.761667, 2872810.453848, 2464548.756925)}}


def get_xy_from_coordinates(latitude, longitude, top, bottom, left, right, nx_tot, ny_tot):
    # get x,y position in subgrid given EPSG:54009 coordinates
    delta_x = (right - left) / nx_tot
    delta_y = (top - bottom) / ny_tot
    ny = ny_tot - int((latitude - bottom) / delta_y - 0.5)
    nx = int((longitude - left) / delta_x - 0.5)
    return nx, ny


class LocalPopulationDensityProvider(PopulationDensityProvider):

    def __init__(self, city: str = 'PRAGUE', h3_resolution: int = 11):
        info_map = context[city]
        self.submap_id = info_map['submap_id']
        self.submap_url = f'data/geographic_data/GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0_{self.submap_id}.tif'
        self.file_url_grid = 'data/geographic_data/GHSL_data_54009_shapefile.zip'
        self.h3_res_pop_density = h3_resolution
        self.population_density = self._load_population_density(self.h3_res_pop_density, info_map['bbox'],
                                                                bbox_crs="EPSG:3035")

    def _load_population_density(self, h3_resolution_pop_density, bbox, bbox_crs):
        crs_population_density_data = 'ESRI:54009'
        crs_h3_json = 'EPSG:4326'

        bbox_shapefile = self._change_bbox_crs(bbox, crs_before=bbox_crs, crs_after=crs_population_density_data)
        shapefile = read_file(self.file_url_grid, bbox=bbox_shapefile)
        grid_info = shapefile[shapefile['tile_id'] == self.submap_id].iloc[0]

        bbox_h3 = self._change_bbox_crs(bbox_shapefile, crs_before=crs_population_density_data, crs_after=crs_h3_json)
        polygon = box(*bbox_h3, ccw=True)
        geojson = GeoSeries([polygon]).iloc[0].__geo_interface__
        hexagons = h3.polyfill_geojson(geojson, h3_resolution_pop_density)

        population_density_grid = tf.imread(self.submap_url, key=0)

        h3_df = GeoDataFrame()
        h3_df['h3_hex'] = Series(list(hexagons))
        h3_df['geometry'] = h3_df['h3_hex'].apply(lambda h3_hex: Point(h3.h3_to_geo(h3_hex)[::-1]))
        h3_df.set_crs(crs=crs_h3_json, inplace=True)
        h3_df.to_crs(crs=crs_population_density_data, inplace=True)
        h3_df['TOT_P_2018'] = h3_df['geometry'].apply(
            lambda geom, pop_dens=population_density_grid, info=grid_info: self._get_pop_density_data(geom, pop_dens,
                                                                                                      info))
        h3_df.index = h3_df['h3_hex']

        return h3_df['TOT_P_2018']

    def _get_pop_density_data(self, location, pop_grid, info):
        x, y = get_xy_from_coordinates(location.y, location.x, info['top'], info['bottom'], info['left'],
                                       info['right'], *pop_grid.shape)
        population_density = pop_grid[y][x] * 100
        if population_density < 0.0:
            population_density = 0.0
        return population_density

    def _change_bbox_crs(self, bbox, crs_before, crs_after):
        (lon_min, lat_min, lon_max, lat_max) = bbox
        p_min = Point(lon_min, lat_min)
        p_max = Point(lon_max, lat_max)
        data = [{'geometry': p_min}, {'geometry': p_max}]
        gdf_bbox = GeoDataFrame(data, crs=crs_before)
        gdf_bbox = gdf_bbox.to_crs(crs=crs_after)
        lon_min = gdf_bbox.loc[0, 'geometry'].x
        lat_min = gdf_bbox.loc[0, 'geometry'].y
        lon_max = gdf_bbox.loc[1, 'geometry'].x
        lat_max = gdf_bbox.loc[1, 'geometry'].y
        bbox = (lon_min, lat_min, lon_max, lat_max)
        return bbox

    def get_population_density(self, h3_hex: str) -> float:
        try:
            population_density = self.population_density[h3_hex]
        except KeyError:
            return -1
        return population_density
