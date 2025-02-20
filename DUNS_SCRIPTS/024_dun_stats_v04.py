# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 17:09:35 2025
Using Python 3.11.1

@author: Mike Middleton
@email: mike@dairsieonline.co.uk
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.cbook import boxplot_stats
import matplotlib.patches as patches


def main():
    
    # Load Excel file
    file_path = r'E:\PAPA\PAPA\ArchaeologyProjects\Duns\duns_writing\Fourty_years_on_from_Harding_1984\tables\kilmartin_sites_soils_circularity.xlsx'  # Replace with the path to your file
    df = pd.read_excel(file_path)
    
    # Filter sites with area data
    sorted_df = df[df["area_inner"] > 0]
    
    #columns_to_check = ['diameter_inner_min', 'diameter_inner_max', 'diameter_outer_min', 'diameter_outer_max']
    columns_to_check = ['diameter_inner_min', 'diameter_inner_max']

    # Filter out rows where any of these columns are -1
    df_filter = sorted_df.loc[~(sorted_df[columns_to_check] == -1).any(axis=1)]
    
    df_filtered = df_filter[df_filter["diameter_inner_min"] < 60]
    df_filtered = df_filter.copy()
    
    plot_diameter_scatter(df_filtered, 'diameter_inner_min', 'diameter_inner_max', 'diameter_outer_min', 'diameter_outer_max')
    plot_circularity_scatter(df_filtered, 'area_inner', 'circularity_inner')
    
    #plot_wall_width_scatter(df_filtered, 'circularity_inner', 'av_wall_width')
    plot_wall_width_area_scatter(df_filtered, 'area_inner', 'av_wall_width')
    
    print(sorted_df.columns)
    
    
    
    
    # plot all stats
    #[inner_stats, outer_stats, area_stats, circularity_stats, wall_stats]
    stats = get_stats(df_filtered)
    inner_stats = stats[0]
    outer_stats = stats[1]
    area_stats = stats[2]
    circularity_stats = stats[3]
    wall_stats = stats[4]
    
    # plot all stats
    plot_combined_01(df_filtered, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats)
    
    # remove the group of rare larger structures
    plot2_df = df_filtered[df_filtered['diameter_inner_min'] < 100]
    
    stats = get_stats(plot2_df)
    inner_stats = stats[0]
    outer_stats = stats[1]
    area_stats = stats[2]
    circularity_stats = stats[3]
    wall_stats = stats[4]
    
    # plot the data again
    plot_combined_02(plot2_df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats)
    
    # remove the second group of rare larger structures
    plot3_df = plot2_df.copy()
    plot3_df = plot3_df[plot3_df['diameter_inner_min'] < 50]
    
    stats = get_stats(plot3_df)
    inner_stats = stats[0]
    outer_stats = stats[1]
    area_stats = stats[2]
    circularity_stats = stats[3]
    wall_stats = stats[4]
    
    # plot the data again
    plot_combined_03(plot3_df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats)
    
    # plot the data again
    plot4_df = plot3_df.copy()
    plot4_df = plot4_df[(plot4_df['diameter_inner_min'] < 30) & (plot4_df['diameter_inner_max'] < 60)]
    
    stats = get_stats(plot4_df)
    inner_stats = stats[0]
    outer_stats = stats[1]
    area_stats = stats[2]
    circularity_stats = stats[3]
    wall_stats = stats[4]
    
    # plot the data again
    plot_combined_04(plot4_df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats)
    
    # plot the data again
    plot5_df = plot4_df.copy()
    plot5_df = plot5_df[(plot5_df['diameter_inner_min'] <= 21)]
    
    stats = get_stats(plot5_df)
    inner_stats = stats[0]
    outer_stats = stats[1]
    area_stats = stats[2]
    circularity_stats = stats[3]
    wall_stats = stats[4]
    
    # plot the data again
    plot_combined_05(plot5_df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats)
    
    ### tests
    less_than_20_wall_less_than_2 = df_filtered[
        (df_filtered['diameter_inner_min'] <= 21) &
        #(df_filtered['diameter_inner_min'] < 100) #&
        #(df_filtered['diameter_inner_max'] > 60)
        (df_filtered['diameter_inner_max'] <= df_filtered['diameter_inner_min'] * 1.5) &
        #(df_filtered['diameter_inner_max'] < df_filtered['diameter_inner_min'] * 1.5) &
        (df_filtered['av_wall_width'] >= 2) &
        (df_filtered['av_wall_width'] < 3)
        ]
    
    less_than_20_wall_less_than_2 = less_than_20_wall_less_than_2.sort_values(by='area_inner', ascending=True)
    print(len(less_than_20_wall_less_than_2))
    print(less_than_20_wall_less_than_2[['study_id', 'canmore_id', 'name', 'area_inner']])

    
    
    # #Filter out unroofed structures
    # df_roofed = df_filtered[df_filtered['diameter_inner_min'] < 21]
    
    # plot_combined(df_roofed, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats)
    
    ## END MAIN ##

def get_stats(df):
    area_data = df['area_inner']
    area_stats = plot_data_range(area_data, 'area_inner', 'h')
    #print(area_stats)
    
    circular_data = df['circularity_inner']
    circularity_stats = plot_data_range(circular_data, 'circularity_inner', 'v')
    #print(circularity_stats)
    
    inner_data = df['diameter_inner_min']
    inner_stats = plot_data_range(inner_data, 'diameter_inner_min', 'h')
    #print(inner_stats)
    
    outer_data = df['diameter_inner_max']
    outer_stats = plot_data_range(outer_data, 'diameter_inner_max', 'v')
    #print(outer_stats)
    
    wall_data = df['av_wall_width']
    wall_stats = plot_data_range(wall_data, 'av_wall_width', 'v')
    #print(wall_stats)
    
    return [inner_stats, outer_stats, area_stats, circularity_stats, wall_stats]
    
# box plot
def plot_data_range(data, feature, o="v"):
    # fig = plt.figure(figsize=(12,8))
    # ax = fig.add_axes([0,0,1,1])
    # ax.set_xlabel(feature)
    # plt.title("title")
    # plt.ticklabel_format(style='plain')
    # if o == "v":
    #     sns.boxplot(data=data, orient="v", whis=[2.2, 97.8])
    # else:
    #     sns.boxplot(data=data, orient="h", whis=[2.2, 97.8])
    # #save_fig(feature + " Range")
    # plt.show()

    bp = boxplot_stats(data, whis=[2.2, 97.8])

    low = bp[0].get('whislo')
    q1 = bp[0].get('q1')
    median =  bp[0].get('med')
    q3 = bp[0].get('q3')
    high = bp[0].get('whishi')

    return [low, q1, median, q3, high]

def add_boxplot(ax, a_stats, b_stats, both=True):
    
    if both:
        # Coordinates of the four corners of the rectangle
        x1, y1 = a_stats[1], b_stats[1]  # Bottom-left corner
        x2, y2 = a_stats[3], b_stats[1]  # Bottom-right corner
        x3, y3 = a_stats[3], b_stats[3]
        x4, y4 = a_stats[1], b_stats[3]
        
        # Calculate the rectangle's width, height, and bottom-left corner
        width = x2 - x1
        height = y3 - y1
        
        # Rectangle(x, y, width, height)
        rectangle = patches.Rectangle((x1, y1), width, height, linewidth=0.5, edgecolor='red', facecolor='none', linestyle='-')
        ax.add_patch(rectangle)
    
        x_value = a_stats[2]
        y1, y2 = b_stats[1], b_stats[3]
        ax.plot([x_value, x_value], [y1, y2], color='red', linestyle='--')
        
        y_value = b_stats[2]
        x1, x2 = a_stats[1], a_stats[3]
        ax.plot([x1, x2], [y_value, y_value], color='red', linestyle='--')
    
    # Coordinates of the four corners of the rectangle
    x1, y1 = a_stats[0], b_stats[0]  # Bottom-left corner
    x2, y2 = a_stats[4], b_stats[0]  # Bottom-right corner
    x3, y3 = a_stats[4], b_stats[4]
    x4, y4 = a_stats[0], b_stats[4]
    
    # Calculate the rectangle's width, height, and bottom-left corner
    width = x2 - x1
    height = y3 - y1
    
    # Rectangle(x, y, width, height)
    rectangle = patches.Rectangle((x1, y1), width, height, linewidth=0.5, edgecolor='black', facecolor='none', linestyle='-')
    ax.add_patch(rectangle)
    

def plot_combined_01(df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats):
    # Create a 1x3 grid of subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)  # Single row, three columns
    
    # First subplot - Internal Diameter
    ax1 = axes[0]
    ax1.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax1.plot([0, 160], [0, 160], linestyle='dotted', color='green', lw=2, label="circular")
    ax1.set_xlabel("diameter min (m)")
    ax1.set_ylabel("diameter max (m)")
    ax1.set_title('Internal Diameter')
    ax1.grid(True, linestyle='--', alpha=0.6)
    add_boxplot(ax1, inner_stats, outer_stats, False)  # Ensure `add_boxplot` is correctly implemented
    ax1.legend()
    ax1.text(0.95, 0.05, 'A', transform=ax1.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Second subplot - Circularity vs Area
    ax2 = axes[1]
    ax2.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax2.set_xlabel("internal area (m\u00B2)")
    ax2.set_ylabel("internal circularity")
    ax2.set_title('Internal Circularity vs Internal Area')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylim(bottom=0.5, top=1)
    add_boxplot(ax2, area_stats, circularity_stats, False)
    ax2.text(0.95, 0.05, 'B', transform=ax2.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Third subplot - Wall Width vs Area
    ax3 = axes[2]
    ax3.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax3.set_xlabel("internal area (m\u00B2)")
    ax3.set_ylabel("average wall width (m)")
    ax3.set_title('Average Wall Width vs Internal Area')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.set_ylim(bottom=0.5)
    add_boxplot(ax3, area_stats, wall_stats, False)
    ax3.text(0.95, 0.05, 'C', transform=ax3.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Show the combined plot
    plt.show()
    
def plot_combined_02(df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats):
    # Create a 1x3 grid of subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)  # Single row, three columns
    
    # First subplot - Internal Diameter
    ax1 = axes[0]
    ax1.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax1.plot([0, 100], [0, 100], linestyle='dotted', color='green', lw=2, label="circular")
    ax1.set_xlabel("diameter min (m)")
    ax1.set_ylabel("diameter max (m)")
    ax1.set_title('Internal Diameter')
    ax1.grid(True, linestyle='--', alpha=0.6)
    add_boxplot(ax1, inner_stats, outer_stats, False)  # Ensure `add_boxplot` is correctly implemented
    ax1.legend()
    ax1.text(0.95, 0.05, 'A2', transform=ax1.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Second subplot - Circularity vs Area
    ax2 = axes[1]
    ax2.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax2.set_xlabel("internal area (m\u00B2)")
    ax2.set_ylabel("internal circularity")
    ax2.set_title('Internal Circularity vs Internal Area')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylim(bottom=0.5, top=1)
    add_boxplot(ax2, area_stats, circularity_stats, False)
    ax2.text(0.95, 0.05, 'B2', transform=ax2.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Third subplot - Wall Width vs Area
    ax3 = axes[2]
    ax3.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax3.set_xlabel("internal area (m\u00B2)")
    ax3.set_ylabel("average wall width (m)")
    ax3.set_title('Average Wall Width vs Internal Area')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.set_ylim(bottom=0)
    add_boxplot(ax3, area_stats, wall_stats, False)
    ax3.text(0.95, 0.05, 'C2', transform=ax3.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Show the combined plot
    plt.show()

def plot_combined_03(df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats):
    # Create a 1x3 grid of subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)  # Single row, three columns
    
    # First subplot - Internal Diameter
    ax1 = axes[0]
    ax1.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax1.plot([0, 50], [0, 50], linestyle='dotted', color='green', lw=2, label="circular")
    ax1.set_xlabel("diameter min (m)")
    ax1.set_ylabel("diameter max (m)")
    ax1.set_title('Internal Diameter')
    ax1.grid(True, linestyle='--', alpha=0.6)
    add_boxplot(ax1, inner_stats, outer_stats, False)  # Ensure `add_boxplot` is correctly implemented
    ax1.legend()
    ax1.text(0.95, 0.05, 'A3', transform=ax1.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Second subplot - Circularity vs Area
    ax2 = axes[1]
    ax2.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax2.set_xlabel("internal area (m\u00B2)")
    ax2.set_ylabel("internal circularity")
    ax2.set_title('Internal Circularity vs Internal Area')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylim(bottom=0.5, top=1)
    add_boxplot(ax2, area_stats, circularity_stats, False)
    ax2.text(0.95, 0.05, 'B3', transform=ax2.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Third subplot - Wall Width vs Area
    ax3 = axes[2]
    ax3.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax3.set_xlabel("internal area (m\u00B2)")
    ax3.set_ylabel("average wall width (m)")
    ax3.set_title('Average Wall Width vs Internal Area')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.set_ylim(bottom=0)
    add_boxplot(ax3, area_stats, wall_stats, False)
    ax3.text(0.95, 0.05, 'C3', transform=ax3.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Show the combined plot
    plt.show()
    
def plot_combined_04(df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats):
    # Create a 1x3 grid of subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)  # Single row, three columns
    
    # First subplot - Internal Diameter
    ax1 = axes[0]
    ax1.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax1.plot([0, 35], [0, 35], linestyle='dotted', color='green', lw=2, label="circular")
    ax1.set_xlabel("diameter min (m)")
    ax1.set_ylabel("diameter max (m)")
    ax1.set_title('Internal Diameter')
    ax1.grid(True, linestyle='--', alpha=0.6)
    add_boxplot(ax1, inner_stats, outer_stats, False)  # Ensure `add_boxplot` is correctly implemented
    ax1.legend()
    ax1.text(0.95, 0.05, 'A4', transform=ax1.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Second subplot - Circularity vs Area
    ax2 = axes[1]
    ax2.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax2.set_xlabel("internal area (m\u00B2)")
    ax2.set_ylabel("internal circularity")
    ax2.set_title('Internal Circularity vs Internal Area')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylim(bottom=0.5, top=1)
    add_boxplot(ax2, area_stats, circularity_stats, False)
    ax2.text(0.95, 0.05, 'B4', transform=ax2.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Third subplot - Wall Width vs Area
    ax3 = axes[2]
    ax3.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax3.set_xlabel("internal area (m\u00B2)")
    ax3.set_ylabel("average wall width (m)")
    ax3.set_title('Average Wall Width vs Internal Area')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.set_ylim(bottom=0)
    add_boxplot(ax3, area_stats, wall_stats, False)
    ax3.text(0.95, 0.05, 'C4', transform=ax3.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Show the combined plot
    plt.show()
    
    print(inner_stats)
    print(outer_stats)
    print(area_stats)
    print(circularity_stats)
    print(wall_stats)
    
def plot_combined_05(df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats):
    # Create a 1x3 grid of subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)  # Single row, three columns
    
    # First subplot - Internal Diameter
    ax1 = axes[0]
    ax1.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax1.plot([0, 25], [0, 25], linestyle='dotted', color='green', lw=2, label="circular")
    ax1.plot([5, 21], [7.5, 31.5], linestyle='dotted', color='red', lw=2, label="width x 1.5")
    ax1.plot([5, 21], [12.5, 52.5], linestyle='dotted', color='orange', lw=2, label="width x 2.5")
    ax1.plot([5, 21], [17.5, 73.5], linestyle='dotted', color='purple', lw=2, label="width x 3.5")
    ax1.set_xlabel("diameter min (m)")
    ax1.set_ylabel("diameter max (m)")
    ax1.set_title('Internal Diameter')
    ax1.grid(True, linestyle='--', alpha=0.6)
    add_boxplot(ax1, inner_stats, outer_stats)  # Ensure `add_boxplot` is correctly implemented
    ax1.legend()
    ax1.text(0.95, 0.05, 'A5', transform=ax1.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Second subplot - Circularity vs Area
    ax2 = axes[1]
    ax2.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax2.set_xlabel("internal area (m\u00B2)")
    ax2.set_ylabel("internal circularity")
    ax2.set_title('Internal Circularity vs Internal Area')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylim(bottom=0.5, top=1)
    add_boxplot(ax2, area_stats, circularity_stats)
    ax2.text(0.95, 0.05, 'B5', transform=ax2.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Third subplot - Wall Width vs Area
    ax3 = axes[2]
    ax3.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax3.set_xlabel("internal area (m\u00B2)")
    ax3.set_ylabel("average wall width (m)")
    ax3.set_title('Average Wall Width vs Internal Area')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.set_ylim(bottom=0)
    add_boxplot(ax3, area_stats, wall_stats)
    ax3.text(0.95, 0.05, 'C5', transform=ax3.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    # Show the combined plot
    plt.show()
    
    print(inner_stats)
    print(outer_stats)
    print(area_stats)
    print(circularity_stats)
    print(wall_stats)    


def plot_combined(df, area_stats, circularity_stats, inner_stats, outer_stats, wall_stats):
    # Create a 2x3 grid of subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12), constrained_layout=True)
    
    # First Row - Internal Diameter
    ax1 = axes[0, 0]
    ax1.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax1.plot([0, 160], [0, 160], linestyle='dotted', color='green', lw=2, label="circular")
    ax1.set_xlabel("diameter min (m)")
    ax1.set_ylabel("diameter max (m)")
    ax1.set_title('Internal Diameter')
    ax1.grid(True, linestyle='--', alpha=0.6)
    add_boxplot(ax1, inner_stats, outer_stats, False)
    ax1.legend()
    ax1.text(0.95, 0.05, 'A', transform=ax1.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    
    # First Row - Circularity vs Area
    ax2 = axes[0, 1]
    ax2.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax2.set_xlabel("internal area (m\u00B2)")
    ax2.set_ylabel("internal circularity")
    ax2.set_title('Internal Circularity vs Internal Area')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylim(bottom=0)
    add_boxplot(ax2, area_stats, circularity_stats, False)
    ax2.text(0.95, 0.05, 'B', transform=ax2.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    
    # First Row - Wall Width vs Area
    ax3 = axes[0, 2]
    ax3.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax3.set_xlabel("internal area (m\u00B2)")
    ax3.set_ylabel("average wall width (m)")
    ax3.set_title('Average Wall Width vs Internal Area')
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.set_ylim(bottom=0)
    add_boxplot(ax3, area_stats, wall_stats, False)
    ax3.text(0.95, 0.05, 'C', transform=ax3.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    
    df = df[df["diameter_inner_min"] < 60]
    
    # Second Row - Repeat Internal Diameter
    ax4 = axes[1, 0]
    ax4.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax4.plot([0, 40], [0, 40], linestyle='dotted', color='green', lw=2, label="circular")
    ax4.plot([5, 21], [7.5, 31.5], linestyle='dotted', color='red', lw=2, label="width x 1.5")
    ax4.plot([5, 21], [12.5, 52.5], linestyle='dotted', color='orange', lw=2, label="width x 2.5")
    ax4.plot([5, 21], [17.5, 73.5], linestyle='dotted', color='purple', lw=2, label="width x 3.5")
    ax4.set_xlabel("diameter min (m)")
    ax4.set_ylabel("diameter max (m)")
    ax4.set_title('Internal Diameter')
    ax4.grid(True, linestyle='--', alpha=0.6)
    add_boxplot(ax4, inner_stats, outer_stats)
    ax4.legend()
    ax4.text(0.95, 0.05, 'A2', transform=ax4.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    
    # Second Row - Repeat Circularity vs Area
    ax5 = axes[1, 1]
    ax5.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax5.set_xlabel("internal area (m\u00B2)")
    ax5.set_ylabel("internal circularity")
    ax5.set_title('Internal Circularity vs Internal Area')
    ax5.grid(True, linestyle='--', alpha=0.6)
    ax5.set_ylim(bottom=0)
    add_boxplot(ax5, area_stats, circularity_stats)
    ax5.text(0.95, 0.05, 'B2', transform=ax5.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    
    # Second Row - Repeat Wall Width vs Area
    ax6 = axes[1, 2]
    ax6.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    ax6.set_xlabel("internal area (m\u00B2)")
    ax6.set_ylabel("average wall width (m)")
    ax6.set_title('Average Wall Width vs Internal Area')
    ax6.grid(True, linestyle='--', alpha=0.6)
    ax6.set_ylim(bottom=0)
    add_boxplot(ax6, area_stats, wall_stats)
    ax6.text(0.95, 0.05, 'C2', transform=ax6.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')
    
    # # Third Row - Repeat Internal Diameter
    # ax7 = axes[2, 0]
    # ax7.scatter(df['diameter_inner_min'], df['diameter_inner_max'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    # ax7.plot([0, 40], [0, 40], linestyle='dotted', color='green', lw=2, label="circular")
    # ax7.plot([5, 21], [7.5, 31.5], linestyle='dotted', color='red', lw=2, label="width x 1.5")
    # ax7.plot([5, 21], [12.5, 52.5], linestyle='dotted', color='orange', lw=2, label="width x 2.5")
    # ax7.plot([5, 21], [17.5, 73.5], linestyle='dotted', color='purple', lw=2, label="width x 3.5")
    # ax7.set_xlabel("diameter min (m)")
    # ax7.set_ylabel("diameter max (m)")
    # ax7.set_title('Internal Diameter')
    # ax7.grid(True, linestyle='--', alpha=0.6)
    # add_boxplot(ax7, inner_stats, outer_stats)
    # ax7.legend()
    # ax7.text(0.95, 0.05, 'A3', transform=ax7.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    
    # # Third Row - Repeat Circularity vs Area
    # ax8 = axes[2, 1]
    # ax8.scatter(df['area_inner'], df['circularity_inner'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    # ax8.set_xlabel("internal area (m\u00B2)")
    # ax8.set_ylabel("internal circularity")
    # ax8.set_title('Internal Circularity vs Internal Area')
    # ax8.grid(True, linestyle='--', alpha=0.6)
    # ax8.set_ylim(bottom=0)
    # add_boxplot(ax8, area_stats, circularity_stats)
    # ax8.text(0.95, 0.05, 'B3', transform=ax8.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')

    
    # # Third Row - Repeat Wall Width vs Area
    # ax9 = axes[2, 2]
    # ax9.scatter(df['area_inner'], df['av_wall_width'], alpha=0.7, c='blue', edgecolors='k', label="inner")
    # ax9.set_xlabel("internal area (m\u00B2)")
    # ax9.set_ylabel("average wall width (m)")
    # ax9.set_title('Average Wall Width vs Internal Area')
    # ax9.grid(True, linestyle='--', alpha=0.6)
    # ax9.set_ylim(bottom=0)
    # add_boxplot(ax9, area_stats, wall_stats)
    # ax9.text(0.95, 0.05, 'C9', transform=ax6.transAxes, fontsize=20, verticalalignment='bottom', horizontalalignment='right', weight='bold')


    # Show the combined plot
    plt.show()



def plot_diameter_scatter(df, inner_min, inner_max, outer_min, outer_max):
    
    # Scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(df[inner_min], df[inner_max], alpha=0.7, c='blue', edgecolors='k', label="inner")
    #plt.scatter(df[outer_min], df[outer_max], alpha=0.7, c='red', edgecolors='k', label="outer")
    # Dotted green line
    plt.plot([0, 50], [0, 50], linestyle='dotted', color='green', label="equal")
    
    # Add labels and title
    plt.legend()
    plt.xlabel("diameter min")
    plt.ylabel("diameter max")
    plt.title('Diameter')
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Show plot
    plt.show()
    
def plot_wall_width_area_scatter(df, area, wall_width):
    
    # Scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(df[area], df[wall_width], alpha=0.7, c='blue', edgecolors='k', label="inner")
    
    # Add labels and title
    #plt.legend()
    plt.xlabel("internal area")
    plt.ylabel("iwall width")
    plt.title('internal area v wall width')
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Show plot
    plt.show()

def plot_circularity_scatter(df, area, circularity):
    
    # Scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(df[area], df[circularity], alpha=0.7, c='blue', edgecolors='k', label="inner")
    
    # Add labels and title
    #plt.legend()
    plt.xlabel("internal area")
    plt.ylabel("internal circularity")
    plt.title('internal cirularity v internal area')
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Show plot
    plt.show()
    
if __name__ == "__main__":
    main()