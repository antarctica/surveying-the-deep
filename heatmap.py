"""
This script generates Figure 7 from Surveying the Deep:
A Review of Computer Vision in the Benthos (Trotter et al. 2025).

Using the literature lat-longs CSV as input, generate a heatmap
showing the geographic origin of image data used to train the reviewed
automated benthic image analysis systems.

Link to CSV: https://ars.els-cdn.com/content/image/1-s2.0-S1574954124005314-mmc1.csv

Usage:
    python3 heatmap.py /path/to/lat_longs.csv output_dir [options]

Author:
    Cameron Trotter (cater@bas.ac.uk)

Date:
    6/01/2025
"""
import argparse
import os
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pandas as pd
from scipy import ndimage
from shapely.geometry import Point

def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        args (argparse.Namespace): An argparse namespace containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Generate a heatmap of the geographic origin\
        of image data used to train the reviewed automated benthic image analysis systems.')
    parser.add_argument('input',
                        type=str,
                        help='Path to the input CSV file containing the latitude and longitude data.')
    parser.add_argument('output',
                        type=str,
                        help='Path for saving the output image file.')
    parser.add_argument('--alpha',
                        type=float,
                        default=1,
                        help='Transparency of the world map. Default is 1.')
    parser.add_argument('--bins',
                        type=int,
                        nargs=2,
                        default=(100,100),
                        help='Number of bins in the heatmap. Default is (100,100).')
    parser.add_argument('--bbox-inches',
                        type=str,
                        default='tight',
                        help='Bounding box of the output image file. Default is "tight".')
    parser.add_argument('--cmap',
                        type=str,
                        default='jet',
                        help='Colormap to use for the heatmap. Default is "jet".')
    parser.add_argument('--colour-bar-label',
                        type=str,
                        default='Log Frequency',
                        help='Label for the colorbar. Default is "Log Frequency".')
    parser.add_argument('--colour-bar-location',
                        type=str,
                        default='right',
                        help='Location of the colorbar. Default is "right".')
    parser.add_argument('--colour-bar-pad',
                        type=float,
                        default=0.05,
                        help='Padding of the colorbar. Default is 0.05.')
    parser.add_argument('--colour-bar-size',
                        type=str,
                        default='2%',
                        help='Size of the colorbar. Default is "2%%".')
    parser.add_argument('--crs',
                        type=str,
                        default='epsg:4326',
                        help='Coordinate reference system to use. Default is "EPSG:4326".')
    parser.add_argument('--dpi',
                        type=int,
                        default=300,
                        help='DPI of the output image file. Default is 300.')
    parser.add_argument('--edgecolor',
                        type=str,
                        default='grey',
                        help='Edge color of the world map. Default is "grey".')
    parser.add_argument('--fig-size',
                        type=int,
                        nargs=2,
                        default=(10,6),
                        help='Size of the output image file in inches. Default is (10,6).')
    parser.add_argument('--filename',
                        type=str,
                        default='heatmap',
                        help='Name of the output image file. Default is "heatmap".')
    parser.add_argument('--format',
                        type=str,
                        default='png',
                        help='Format of the output image file. Default is "png".')
    parser.add_argument('--label-pad',
                        type=int,
                        default=15,
                        help='Padding of the colorbar label. Default is 15.')
    parser.add_argument('--label-rotation',
                        type=int,
                        default=270,
                        help='Rotation of the colorbar label. Default is 270.')
    parser.add_argument('--linewidth',
                        type=float,
                        default=0.75,
                        help='Width of the world map lines. Default is 0.75.')
    parser.add_argument('--map',
                        type=str,
                        default='naturalearth_lowres',
                        help='Name of the map to load. Default is "naturalearth_lowres".')
    parser.add_argument('--mode',
                        type=str,
                        default='nearest',
                        help='Mode of the smoothing filter. Default is "nearest".')
    parser.add_argument('--pad-inches',
                        type=float,
                        default=0.1,
                        help='Padding of the output image file. Default is 0.1.')
    parser.add_argument('--smoothing',
                        type=float,
                        default=1.3,
                        help='Amount of smoothing to apply to the heatmap. Default is 1.3.')
    parser.add_argument('--title',
                        type=str,
                        default=None,
                        help='Title of the output image file. Default is None.')
    parser.add_argument('--x-label',
                        type=str,
                        default='Longitude',
                        help='Label for the x-axis. Default is "Longitude".')
    parser.add_argument('--y-label',
                        type=str,
                        default='Latitude',
                        help='Label for the y-axis. Default is "Latitude".')

    return parser.parse_args()

def get_world_map(map_projection):
    """
    Get a world map from the geopandas library.
    
    Args:
        map (str): The name of the map to load.
        
    Returns:
        world (geopandas.geodataframe.GeoDataFrame): A geopandas dataframe containing the world map.
    """
    world = gpd.read_file(gpd.datasets.get_path(map_projection))
    return world

def pandas_to_geopandas(df, crs):
    """
    Convert a pandas dataframe to a geopandas dataframe.
    
    Args:
        df (pandas.core.frame.DataFrame): A pandas dataframe.
        crs (dict): The coordinate reference system to use.
        
    Returns:
        gdf (geopandas.geodataframe.GeoDataFrame): A geopandas dataframe.
    """
    geometry = [Point(xy) for xy in zip(df.Longitude_rounded, df.Latitude_rounded)]
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
    return gdf

def generate_heatmap(df, args):
    """
    Generate a heatmap from a geopandas dataframe using 2D histogram binning with smoothing.
    Based on https://nbviewer.org/gist/perrygeo/c426355e40037c452434
    
    Args:
        df (geopandas.geodataframe.GeoDataFrame): A geopandas dataframe containing the data.
        args (argparse.Namespace): An argparse namespace containing the arguments.
    """

    coords = df.geometry.apply(lambda pt: pt.coords[0])
    x, y = zip(*coords)
    heatmap, _, _ = np.histogram2d(y, x, bins=args.bins)

    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, args.smoothing, mode=args.mode)

    return logheatmap

def overlay_heat_on_map(world, heat, args):
    """
    Overlay a heatmap on a world map, and save the output image file.
    
    Args:
        world (geopandas.geodataframe.GeoDataFrame): A geopandas dataframe containing the world map.
        heat (numpy.ndarray): A numpy array containing the heatmap data.
        args (argparse.Namespace): An argparse namespace containing the arguments.
    """
    minx, miny, maxx, maxy = world.boundary.total_bounds

    ax = world.boundary.plot(figsize=args.fig_size,
                             edgecolor=args.edgecolor,
                             alpha=args.alpha,
                             linewidth=args.linewidth)
    image = plt.imshow(heat, cmap=args.cmap, extent=[minx, maxx, maxy, miny])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes(args.colour_bar_location,
                              size=args.colour_bar_size,
                              pad=args.colour_bar_pad)
    cbar = plt.colorbar(image, cax=cax)

    ax.invert_yaxis()
    ax.set_xlabel(args.x_label)
    ax.set_ylabel(args.y_label)
    cbar.ax.set_ylabel(args.colour_bar_label,
                       rotation=args.label_rotation,
                       labelpad=args.label_pad)

    if args.title is not None:
        ax.set_title(args.title)

    filename = f"{args.filename}.{args.format}"
    full_path = os.path.join(args.output, filename)
    plt.savefig(full_path,
                dpi=args.dpi,
                format=args.format,
                bbox_inches=args.bbox_inches,
                pad_inches=args.pad_inches)

def main():
    """
    Parse arguments and generate a heatmap of the geographic origin of image data
    used to train the reviewed automated benthic image analysis systems.
    """
    args = parse_args()

    df = pd.read_csv(args.input)
    gdf = pandas_to_geopandas(df, crs=args.crs)

    world = get_world_map(args.map)
    heatmap = generate_heatmap(gdf, args)

    overlay_heat_on_map(world, heatmap, args)

if __name__ == '__main__':
    main()
