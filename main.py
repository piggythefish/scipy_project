import pandas as pd
import tkinter as tk
import numpy as np
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Read the CSV files
races_df = pd.read_csv('data/races.csv') #raceId,year,round,circuitId,name,date,time,url,fp1_date,fp1_time,fp2_date,fp2_time,fp3_date,fp3_time,quali_date,quali_time,sprint_date,sprint_time
lap_times_df = pd.read_csv('data/lap_times.csv') #raceId,driverId,lap,position,time,milliseconds
drivers_df = pd.read_csv('data/drivers.csv') #driverId,driverRef,number,code,forename,surname,dob,nationality,url
results_df = pd.read_csv('data/results.csv') #resultId,raceId,driverId,constructorId,number,grid,position,positionText,positionOrder,points,laps,time,milliseconds,fastestLap,rank,fastestLapTime,fastestLapSpeed,statusId
constructors_df = pd.read_csv('data/constructors.csv') #constructorId,constructorRef,name,nationality,url
constructors_standings_df = pd.read_csv('data/constructor_standings.csv') #constructorStandingsId,raceId,constructorId,points,position,positionText,wins

# Handpicked colors for constructors
constructor_colors = {
    'Red Bull': 'navy',
    'Mercedes': 'cyan',
    'Ferrari': 'red',
    'Alfa Romeo': 'darkred',
    'AlphaTauri': 'lightslategrey',
    'Williams': 'lightskyblue',
    'McLaren': 'orange',
    'Aston Martin': 'green',
    'Alpine F1 Team': 'dodgerblue',
    'Haas F1 Team': 'silver',
    'Renault': 'gold',
    'Toro Rosso': 'darkgrey',
    'Force India': 'pink',
    'Sauber': 'darkgoldenrod',
    'Manor Marussia': 'grey',
    'Benetton': 'dodgerblue',
    'Jordan': 'yellow',
    'Jaguar': 'green',
    'Ligier': 'darkblue',
    'Footwork': 'chocolate',
    'Prost': 'blueviolet',
    'Stewart': 'snow',
    'BAR': 'lightgray',
    'Honda': 'gainsboro',
    'BMW Sauber': 'powderblue',
    'Toyota': 'tomato',
    'Brawn': 'lawngreen'
    }

# Global canvas variable that gets used across multiple function calls
current_canvas = None

def update_names(event):
    """
    Function to update the names based on the selected year.
    The function retrieves the selected year from the combobox, filters the dataframe for that year, and updates
    the name combobox with the names corresponding to the selected year.

    Args:
        event: This parameter is required for a function to be used as an event handler in Tkinter, even if it is
               not used within the function. Here, it represents the event of selecting a year from the year_combobox.

    Returns:
        None
    """
    selected_year = year_combobox.get()
    if selected_year.isdigit():
        names = races_df[races_df['year'] == int(selected_year)]['name']
        name_combobox['values'] = names.tolist()

def get_race_id_and_plot():
    """
    Function to get the raceId and plot the corresponding graph based on selected year, name, and option.
    The function retrieves the selected year, name, and option from their respective comboboxes, filters the dataframe
    for the selected year and name to get the raceId, and then calls the appropriate plotting function based on the
    selected option.

    Args:
        None

    Returns:
        None
    """
    selected_year = year_combobox.get()
    selected_name = name_combobox.get()
    selected_option = option_combobox.get()
    if selected_year.isdigit():
        race_id = races_df[(races_df['year'] == int(selected_year)) & (races_df['name'] == selected_name)]['raceId'].values[0]
        if selected_option == 'Global Racepace':
            plot_boxplot(race_id)
        elif selected_option == 'Lap-by-Lap Racepace':
            plot_lineplot(race_id)
        elif selected_option == 'Position per Lap':
            plot_position_per_lap(race_id)
        elif selected_option == 'Driver Standings':
            plot_drivers_standings(race_id)
        elif selected_option == 'Constructor Standings':
            plot_constructor_standings(race_id)

def plot_boxplot(race_id):
    """
    Function to plot a boxplot of lap times for each driver in a particular Formula 1 race.

    The function retrieves the lap time data for the specified race, filters out potential pit stop laps,
    sorts the drivers by their mean lap time, gets the team colors for each driver, and then plots the boxplot.

    Args:
        race_id (int): The ID of the race to plot.

    Returns:
        None

    """
    global current_canvas
    # Retrieve the lap time data for the specified race, excluding the first 2 laps
    race_data = lap_times_df[lap_times_df['raceId'] == race_id].query('lap > 2')
    
    # Compute the mean and standard deviation of milliseconds for the race
    mean_milliseconds = race_data['milliseconds'].mean()
    std_milliseconds = race_data['milliseconds'].std()

    # Exclude laps that are likely to be pit stops, based on a threshold of mean + 2 standard deviations
    threshold = mean_milliseconds + 2 * std_milliseconds
    race_data = race_data[race_data['milliseconds'] < threshold]

    # Create a mapping between driverId and constructorId for the specific raceId
    driver_constructor_mapping = results_df[results_df['raceId'] == race_id].set_index('driverId')['constructorId'].to_dict()
    
    # Create a mapping between constructorId and constructor name
    constructor_names = constructors_df.set_index('constructorId')['name'].to_dict()

    # Group by driverId and sort by the mean of the 'milliseconds' column
    sorted_drivers = race_data.groupby('driverId')['milliseconds'].mean().sort_values()
    sorted_driver_ids = sorted_drivers.index.tolist()

    # Mapping between driverId and driver codes
    driver_codes = drivers_df.set_index('driverId')['code'].to_dict()

    # Get the data for each driver in the sorted order and divide by 1000 to get seconds
    data_to_plot = [race_data[race_data['driverId'] == driver_id]['milliseconds'] / 1000 for driver_id in sorted_driver_ids]
    
    # Get the mean and median lap times for each driver in the sorted order
    means = [f'{np.mean(data):.2f}' for data in data_to_plot]
    medians = [f'{np.median(data):.2f}' for data in data_to_plot]
    
    # Update driver codes for drivers with "\N" code
    for driver_id, code in driver_codes.items():
        if code == "\\N":
            surname = drivers_df[drivers_df['driverId'] == driver_id]['surname'].values[0]
            driver_codes[driver_id] = surname[:3].upper()

    # Get the colors for each driver based on the constructor's team colors
    colors_to_plot = []
    for driver_id in sorted_driver_ids:
        constructor_id = driver_constructor_mapping.get(driver_id)
        constructor_name = constructor_names.get(constructor_id, 'Unknown') # set team 'Unknown' as default
        color = constructor_colors.get(constructor_name, 'black') # set color 'black' as default
        colors_to_plot.append(color)
        
    # Get the driver codes for each driver in the sorted order
    labels_to_plot = [f'{driver_codes.get(driver_id, f"Driver {driver_id}")}\n{mean}\n{median}' for driver_id, mean, median in zip(sorted_driver_ids, means, medians)]
    
    fig, ax = plt.subplots(figsize=(15,6))
    bp = ax.boxplot(data_to_plot, patch_artist=True, showmeans=True, meanline=True)
    
    # Set the colors of the boxplots and style of median and mean lines
    for patch, color, meanline, medianline in zip(bp['boxes'], colors_to_plot, bp['means'], bp['medians']):
        patch.set_facecolor(color)
        meanline.set_linestyle('-')  # Solid line for mean
        meanline.set_color('black')
        medianline.set_linestyle('--')  # Dashed line for median
        medianline.set_color('black')
        
    grand_prix_name = races_df[races_df['raceId'] == race_id]['name'].values[0]
    grand_prix_year = races_df[races_df['raceId'] == race_id]['year'].values[0]

    # Set the title, labels, and x-ticks of the graph
    ax.set_title(f'Global Racepace - {grand_prix_name} {grand_prix_year}')    
    ax.set_xlabel('Driver')
    ax.set_ylabel('Seconds')
    ax.set_xticklabels(labels_to_plot, ha='center')  
    
    # Add mean and median labels to the left of the graph
    ax.text(0.0, -0.075, "Mean:", transform=ax.transAxes, ha='right', fontsize=10)
    ax.text(0.0, -0.11, "Median:", transform=ax.transAxes, ha='right', fontsize=10)
    
    # Remove the current canvas if it exists
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Create a new canvas and add the figure to it
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea
    current_canvas = canvas
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=2)    
    plt.tight_layout(rect=[0, 0, 1, 1])  # Adjusts the plot to make room for the legend
    canvas.draw()

def plot_lineplot(race_id):
    """
    Plots a lineplot of lap times for a given race.
    
    This function takes a race_id, retrieves the relevant race data, excludes likely pitstop laps and plots 
    the lap-by-lap race pace smoothed over a moving average window for each driver, colouring lines based on team.

    Args:
        race_id (int): The ID of the race to be plotted

    Returns:
        None
    """
    global current_canvas
    # Select the data for the specific race and exclude the first two laps
    race_data = lap_times_df[lap_times_df['raceId'] == race_id].query('lap > 2')
    
    # Compute the mean and standard deviation of milliseconds for the race
    mean_milliseconds = race_data['milliseconds'].mean()
    std_milliseconds = race_data['milliseconds'].std()
    
    # Exclude laps that are likely to be pit stops, based on a threshold of mean + 2 standard deviations
    threshold = mean_milliseconds + 2 * std_milliseconds
    race_data = race_data[race_data['milliseconds'] < threshold]    

    # Create a mapping between driverId and constructorId for the specific raceId
    driver_constructor_mapping = results_df[results_df['raceId'] == race_id].set_index('driverId')['constructorId'].to_dict()

    # Create a mapping between constructorId and constructor name
    constructor_names = constructors_df.set_index('constructorId')['name'].to_dict()

    # Get the drivers codes from their driverId
    driver_codes = drivers_df.set_index('driverId')['code'].to_dict()
    
    # Update driver codes for drivers with "\N" code, set code as the first three letters of the driver's surname
    for driver_id, code in driver_codes.items():
        if code == "\\N":
            surname = drivers_df[drivers_df['driverId'] == driver_id]['surname'].values[0]
            driver_codes[driver_id] = surname[:3].upper()

    # Create a new plot
    fig, ax = plt.subplots(figsize=(15,6))
    
    # Keep track of the drivers plotted for each constructor to vary the line style
    plotted_constructors = {}

    # Plot a line for each driver, using the constructor's specific color and varying the line style
    for driver_id in race_data['driverId'].unique():
        driver_data = race_data[race_data['driverId'] == driver_id]
        
        # Calculate the moving average for the milliseconds column
        window_size = 10  # Adjustable value for window size
        smoothed_milliseconds = (driver_data['milliseconds'] / 1000).rolling(window=window_size, center=True).median().dropna()
        valid_laps = driver_data['lap'].loc[smoothed_milliseconds.index]
        
        constructor_id = driver_constructor_mapping.get(driver_id)
        name_code = driver_codes.get(driver_id, f'Driver {driver_id}')
        constructor_name = constructor_names.get(constructor_id, 'Unknown')
        color = constructor_colors.get(constructor_name, 'black')

        # Set line style based on whether this is the first or second driver for the constructor
        linestyle = '-' if constructor_id not in plotted_constructors else '--'
        plotted_constructors[constructor_id] = True

        ax.plot(valid_laps, smoothed_milliseconds, label=f'{name_code}', color=color, linestyle=linestyle)
        
    # Set the title, labels and legend for the plot
    grand_prix_name = races_df[races_df['raceId'] == race_id]['name'].values[0]
    grand_prix_year = races_df[races_df['raceId'] == race_id]['year'].values[0]
    ax.set_title(f'Smoothed Lap-by-Lap Racepace - {grand_prix_name} {grand_prix_year}')  
    ax.set_xlabel('Lap')
    ax.set_ylabel('Seconds')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

    # If a canvas already exists, destroy it to prevent overlap with the new plot
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Create a new canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea
    current_canvas = canvas
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=2)  
    
    # Adjust the plot to make room for the legend
    plt.tight_layout(rect=[0, 0, 1, 1])
    
    # Draw the plot
    canvas.draw()

def plot_position_per_lap(race_id):
    """
    Plots a line graph showing the position of each driver over the course of a race.
    
    This function takes a race_id, retrieves the relevant race data, and plots 
    the position of each driver for each lap, colouring lines based on team.

    Args:
        race_id (int): The ID of the race to be plotted

    Returns:
        None
    """
    global current_canvas
    # Select the data for the specific race
    race_data = lap_times_df[lap_times_df['raceId'] == race_id]

    # Create a mapping between driverId and constructorId for the specific raceId
    driver_constructor_mapping = results_df[results_df['raceId'] == race_id].set_index('driverId')['constructorId'].to_dict()

    # Create a mapping between constructorId and constructor name
    constructor_names = constructors_df.set_index('constructorId')['name'].to_dict()

    # Get the final positions of the drivers, sorted by positionOrder
    sorted_drivers = results_df[results_df['raceId'] == race_id].sort_values(by='positionOrder', ascending=True)['driverId']

    # Get the drivers codes from their driverId
    driver_codes = drivers_df.set_index('driverId')['code'].to_dict()

    # Update driver codes for drivers with "\N" code, set code as the first three letters of the driver's surname
    for driver_id, code in driver_codes.items():
        if code == "\\N":
            surname = drivers_df[drivers_df['driverId'] == driver_id]['surname'].values[0]
            driver_codes[driver_id] = surname[:3].upper()

    # Create a new plot
    fig, ax = plt.subplots(figsize=(15,6))

    # Plot a line for each driver in the sorted order
    for driver_id in sorted_drivers:
        driver_data = race_data[race_data['driverId'] == driver_id]
        
        # Continue if no race data for the driver
        if driver_data.empty:
            continue
        
        constructor_id = driver_constructor_mapping.get(driver_id)
        constructor_name = constructor_names.get(constructor_id, 'Unknown')
        color = constructor_colors.get(constructor_name, 'black')
        driver_code = driver_codes.get(driver_id, 'Unknown')
        
        # Plot the driver's position per lap
        ax.plot(driver_data['lap'], driver_data['position'], marker='o', color=color, linestyle='-')
        x_last_point = driver_data['lap'].iloc[-1]
        y_last_point = driver_data['position'].iloc[-1]
        x_offset = 0.05
        y_offset = -0.3
        # Annotate the final point of each driver's plot with the driver's code
        ax.text(x_last_point + x_offset, y_last_point + y_offset, driver_code, color=color, verticalalignment='center')

    # Set the title, labels and legend for the plot
    grand_prix_name = races_df[races_df['raceId'] == race_id]['name'].values[0]
    grand_prix_year = races_df[races_df['raceId'] == race_id]['year'].values[0]
    ax.set_title(f'Position per Lap - {grand_prix_name} {grand_prix_year}')  
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')
    
    # Reverse y-axis to make position 1 at the top
    ax.set_ylim(ax.get_ylim()[::-1]) 
    
    # Set yticks to be the finishing positions
    finishing_positions = sorted(results_df[results_df['raceId'] == race_id]['positionOrder'].unique())
    ax.set_yticks(finishing_positions)
    ax.yaxis.set_tick_params(labelright=True)

    # If a canvas already exists, destroy it to prevent overlap with the new plot
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Create a new canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea
    current_canvas = canvas
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=2)  
    
    # Draw the plot
    canvas.draw()

def plot_drivers_standings(race_id):
    """
    Plots a horizontal bar graph showing the drivers' standings up to a specific race.
    
    This function takes a race_id, retrieves the relevant race data and sums up 
    the points each driver has accumulated up to and including this race. It then 
    plots a horizontal bar chart with drivers' codes and the color of each bar 
    representing the team of each driver.

    Args:
        race_id (int): The ID of the race up to which the standings are to be plotted

    Returns:
        None
    """
    global current_canvas
    # Get the season based on race_id
    season = races_df[races_df['raceId'] == race_id]['year'].iloc[0]

    # Filter races up to and including the given race_id for the specific season
    standings_df = results_df[(results_df['raceId'] <= race_id) & (results_df['raceId'].isin(races_df[races_df['year'] == season]['raceId']))]

    # Group by driverId and sum the points they've earned
    driver_points = standings_df.groupby('driverId')['points'].sum().reset_index()

    # Merge with driver information to add driver codes and names
    driver_points = pd.merge(driver_points, drivers_df, on='driverId')

    # Replace '\N' in 'code' with the first three characters of 'surname'
    driver_points['code'] = driver_points.apply(lambda row: row['code'] if row['code'] != '\\N' else row['surname'][:3].upper(), axis=1)

    # Sort the drivers by points earned
    driver_points = driver_points.sort_values('points', ascending=False)
    
    # Define function to retrieve team color for each driver
    def get_team_color(driver_id):
        constructor_id = standings_df[standings_df['driverId'] == driver_id]['constructorId'].iloc[-1]
        constructor_name = constructors_df[constructors_df['constructorId'] == constructor_id]['name'].iloc[0]
        return constructor_colors.get(constructor_name, 'black')

    # Apply the function to get a color for each driver
    driver_points['color'] = driver_points['driverId'].apply(get_team_color)

    # Create a new plot
    fig, ax = plt.subplots(figsize=(15,6))
    
    # Create the horizontal bar plot
    ax.barh(driver_points['code'], driver_points['points'], color=driver_points['color'])
    
    # Invert y-axis so that higher points are shown on top
    ax.invert_yaxis()
    ax.set_xlabel('Points')
    ax.set_ylabel('Driver')
        
    # Set the title for the plot
    grand_prix_name = races_df[races_df['raceId'] == race_id]['name'].values[0]
    grand_prix_year = races_df[races_df['raceId'] == race_id]['year'].values[0]
    ax.set_title(f'Drivers Standings as of the {grand_prix_name} {grand_prix_year}')  

    # If a canvas already exists, destroy it to prevent overlap with the new plot
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Create a new canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=root)
    current_canvas = canvas
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=2)  
    
    # Draw the plot
    canvas.draw()

def plot_constructor_standings(race_id):
    """
    Plots a horizontal bar graph showing the constructors' standings up to a specific race.
    
    This function takes a race_id, retrieves the relevant race data and sums up 
    the points each constructor has accumulated up to and including this race. It then 
    plots a horizontal bar chart with constructors' names and the color of each bar 
    representing the constructor.

    Args:
        race_id (int): The ID of the race up to which the standings are to be plotted

    Returns:
        None
    """
    global current_canvas
    # Get the season based on race_id
    season = races_df[races_df['raceId'] == race_id]['year'].iloc[0]

    # Filter races up to the given race_id for the specific season
    standings_df = constructors_standings_df[(constructors_standings_df['raceId'] <= race_id) & (constructors_standings_df['raceId'].isin(races_df[races_df['year'] == season]['raceId']))]

    # Group by constructorId and take the maximum of points
    # this reflects the cumulative points until the current race
    constructor_points = standings_df.groupby('constructorId')['points'].max().reset_index()

    # Retrieve constructor name and color
    constructor_points['name'] = constructor_points['constructorId'].apply(lambda x: constructors_df[constructors_df['constructorId'] == x]['name'].iloc[0])
    constructor_points['color'] = constructor_points['name'].apply(lambda x: constructor_colors.get(x, 'black'))

    # Sort by points
    constructor_points = constructor_points.sort_values('points', ascending=False)

    # Create a new plot
    fig, ax = plt.subplots(figsize=(15,6))
    
    # Create the horizontal bar plot
    ax.barh(constructor_points['name'], constructor_points['points'], color=constructor_points['color'])
    
    # Invert y-axis so that higher points are shown on top
    ax.invert_yaxis()
    ax.set_xlabel('Points')
    ax.set_ylabel('Constructor')
        
    # Set the title for the plot
    grand_prix_name = races_df[races_df['raceId'] == race_id]['name'].values[0]
    grand_prix_year = races_df[races_df['raceId'] == race_id]['year'].values[0]
    ax.set_title(f'Constructors Standings as of the {grand_prix_name} {grand_prix_year}')  

    # If a canvas already exists, destroy it to prevent overlap with the new plot
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Create a new canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=root)
    current_canvas = canvas
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=5, column=0, columnspan=2)  
    
    # Draw the plot
    canvas.draw()


# Create the main window
root = tk.Tk()
root.title("Formula 1 Race Data Tool")

# Create a label and combobox for selecting the year
year_label = tk.Label(root, text="Select Year:")
year_label.grid(row=0, column=0)
year_combobox = ttk.Combobox(root, values=sorted(year for year in races_df['year'].unique() if (year >= 1996 and year != 2023)), width=30)
year_combobox.grid(row=0, column=1)

# Bind the update_names function to the selection event of the year_combobox
year_combobox.bind('<<ComboboxSelected>>', update_names)

# Create a label and combobox for displaying the names corresponding to the selected year
name_label = tk.Label(root, text="Select Race:")
name_label.grid(row=1, column=0)
name_combobox = ttk.Combobox(root, width=30)
name_combobox.grid(row=1, column=1)

# Create a label and combobox for selecting the option
option_label = tk.Label(root, text="Select Type of Plot:")
option_label.grid(row=2, column=0)
options = ['Global Racepace', 'Lap-by-Lap Racepace', 'Position per Lap', 'Driver Standings', 'Constructor Standings']
option_combobox = ttk.Combobox(root, values=options, width=30)
option_combobox.grid(row=2, column=1)

# Button to get the raceId and plot the graph based on the selected year, name, and option
get_race_id_button = tk.Button(root, text="Plot", command=get_race_id_and_plot)
get_race_id_button.grid(row=3, column=0, columnspan=2)

# Label to display the raceId
race_id_label = tk.Label(root, text="")
race_id_label.grid(row=4, column=0, columnspan=2)

# Run the Tkinter event loop
root.mainloop()
