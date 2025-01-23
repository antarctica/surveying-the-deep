"""
This script generates Figure 1 from Surveying the Deep:
A Review of Computer Vision in the Benthos (Trotter et al. 2025).

Using the paper techniques CSV as input, generate a stacked barchart
showing the progression of computer vision-based benthic biodiversity monitoring 
literature over time, subdivided by techniques utilised. If a publication contained
more than a single technique, it is represented multiple times. 

Link to CSV: https://ars.els-cdn.com/content/image/1-s2.0-S1574954124005314-mmc2.csv

Usage:
    python3 techniques.py /path/to/path/to/techniques.csv output_dir [options]

Author:
    Cameron Trotter (cater@bas.ac.uk)

Date:
    6/01/2025
"""
import argparse
import os
import matplotlib.pyplot as plt
import pandas as pd

def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        args (argparse.Namespace): An argparse namespace containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Generate a stacked barchart showing the\
        progression of computer vision-based benthic biodiversity monitoring literature\
        over time, subdivided by techniques utilised.')
    parser.add_argument('input',
                        type=str,
                        help='Path to the input CSV file containing the publication data.')
    parser.add_argument('output',
                        type=str,
                        help='Path for saving the output image file.')
    parser.add_argument('--after-year-only',
                        type=int,
                        default=None,
                        help='Only show statistics after this year. Default is None.')
    parser.add_argument('--bbox-inches',
                        type=str,
                        default='tight',
                        help='Bounding box of the output image file. Default is "tight".')
    parser.add_argument('--dpi',
                        type=int,
                        default=300,
                        help='DPI of the output image file. Default is 300.')
    parser.add_argument('--fig-size',
                        type=int,
                        nargs=2,
                        default=(10, 5),
                        help='Size of the output image file in inches. Default is (10, 5).')
    parser.add_argument('--filename',
                        type=str,
                        default='techniques',
                        help='Name of the output image file. Default is "techniques".')
    parser.add_argument('--format',
                        type=str,
                        default='png',
                        help='Format of the output image file. Default is "png".')
    parser.add_argument('--legend-title',
                        type=str,
                        default='Techniques',
                        help='Title of the legend. Default is "Techniques".')
    parser.add_argument('--no-print-stats',
                        action='store_true',
                        help='Do not print statistics about the techniques used in the publications. Default is False.')
    parser.add_argument('--no-show-legend',
                        action='store_true',
                        help='Do not show the legend on the plot. Default is False.')
    parser.add_argument('--pad-inches',
                        type=float,
                        default=0.1,
                        help='Padding of the output image file. Default is 0.1.')
    parser.add_argument('--title',
                        type=str,
                        default=None,
                        help='Title of the plot. Default is None.')
    parser.add_argument('--xlabel',
                        type=str,
                        default='Year',
                        help='Label for the x-axis. Default is "Year".')
    parser.add_argument('--ylabel',
                        type=str,
                        default='Number of Papers',
                        help='Label for the y-axis. Default is "Number of Papers".')

    return parser.parse_args()

def format_df(df):
    """
    Format the dataframe to be used in the stacked barchart.
    
    Args:
        df (pandas.core.frame.DataFrame): A pandas dataframe containing the publication data.
        
    Returns:
        df_techs (pandas.core.frame.DataFrame):
            A pandas dataframe containing the publication data with the techniques formatted.
    """
    df_techs = df[['Year', 'Image_Processing', 'Machine_Learning', 'Deep_Learning']]
    df_techs.columns = ['Year', 'Image Processing', 'Machine Learning', 'Deep Learning']

    df_techs = df_techs.groupby('Year').sum()
    return df_techs

def generate_stacked_barchart(df, args):
    """
    Generate a stacked barchart showing the progression of computer vision-based benthic biodiversity
    monitoring literature over time, subdivided by techniques utilised.
    
    Args:
        df (pandas.core.frame.DataFrame):
            A pandas dataframe containing the publication data with the techniques formatted.
        args (argparse.Namespace): An argparse namespace containing the parsed arguments.
    """
    show_legend = not args.no_show_legend

    df.plot(kind='bar', stacked=True,
            figsize=args.fig_size,
            xlabel=args.xlabel,
            ylabel=args.ylabel,
            legend=show_legend)

    plt.legend(['Image Processing',
                'Machine Learning',
                'Deep Learning'],
               title=args.legend_title)

    if args.title is not None:
        plt.title(args.title)

    filename = f"{args.filename}.{args.format}"
    full_path = os.path.join(args.output, filename)
    plt.savefig(full_path, dpi=args.dpi, format=args.format,
                bbox_inches=args.bbox_inches, pad_inches=args.pad_inches)

def print_stats(df, after_year_only):
    """
    Print statistics about the techniques used in the publications.
    
    Args:
        df (pandas.core.frame.DataFrame):
            A pandas dataframe containing the publication data with the techniques formatted.
        after_year_only (int): Only show statistics after this year.
    """
    if after_year_only is not None:
        df = df[df.index >= after_year_only]
        print(f'Stats after {after_year_only}:')

    percent_ip = df['Image Processing'].sum() / df.sum().sum() * 100
    percent_ml = df['Machine Learning'].sum() / df.sum().sum() * 100
    percent_dl = df['Deep Learning'].sum() / df.sum().sum() * 100

    print('Percentage of papers that used Image Processing:', percent_ip)
    print('Percentage of papers that used Machine Learning:', percent_ml)
    print('Percentage of papers that used Deep Learning:', percent_dl)

def main():
    """
    Parse arguments and generate a stacked barchart showing the progression of
    computer vision-based benthic biodiversity monitoring literature over time,
    subdivided by techniques utilised.
    """
    args = parse_args()
    df = pd.read_csv(args.input)
    df = format_df(df)

    generate_stacked_barchart(df, args)

    if not args.no_print_stats:
        print_stats(df, args.after_year_only)

if __name__ == '__main__':
    main()
