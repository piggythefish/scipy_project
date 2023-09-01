# Formula 1 Race Data Visualization Tool

This project is a Formula 1 race data visualization tool created using Python. The tool allows the user to select a year between 1996 and 2022, choose a specific grand prix from that year, and then select one of five different types of plots to visualize the race data. 

## Getting Started

To use this tool, follow the steps below:

1. Ensure that you have all the necessary dependencies installed. The tool requires the following packages: pandas, tkinter, numpy and matplotlib. You can also just use the requirements.txt file for that.

2. Download or clone the repository to your local machine.

3. Open the main Python script file, `main.py`, in your preferred Python IDE.

4. Run the script to start the application. A GUI window will open.

## Usage

1. In the GUI window, select a year between 1996 and 2022 from the "Select Year" combobox.

2. After selecting a year, the "Select Race" combobox will automatically display the names of the grand prix races that occurred in that year. Choose a specific grand prix from the combobox.

3. Select one of the available plot options from the "Select Type of Plot" combobox.

4. Click the "Plot" button to generate the selected plot based on the chosen year, race, and plot option.

5. The generated plot will be displayed in the GUI window.

## File Structure

The project repository is organized as follows:

- `data/` - This directory contains the CSV files that store the Formula 1 race data.
- `main.py` - The main Python script for running the application and creating the GUI window.
- `constructors_colors.py`- The python script containing the respective colors for the constructors
- `README.md` - This file, providing an overview and instructions for the project.

## Dependencies

This project relies on the following dependencies:

- pandas - Used for data manipulation and analysis.
- tkinter - The standard Python interface to the Tk GUI toolkit.
- numpy - Required for various scientific computing operations.
- matplotlib - Used for creating plots and data visualizations.

Make sure you have these dependencies installed before running the project. You can use the provided requirements.txt file:

`pip install -r requirements.txt`

Run this command in the terminal from the directory containing the requirements.txt file. This will install all necessary dependencies.

## Data

The project uses the following CSV files containing Formula 1 race data:

- `races.csv` - Contains information about each race, including the race ID, year, round, circuit ID, name, date, time, and URL.
- `lap_times.csv` - Contains lap time data for each race, including the race ID, driver ID, lap number, position, time, and milliseconds.
- `drivers.csv` - Contains information about each driver, including the driver ID, driver reference, number, code, forename, surname, date of birth, nationality, and URL.
- `results.csv` - Contains results data for each race, including the result ID, race ID, driver ID, constructor ID, number, grid position, finishing position, position text, position order, points, number of laps, time, milliseconds, fastest lap, rank, fastest lap time, fastest lap speed, and status ID.
- `constructors.csv` - Contains information about each constructor, including the constructor ID, constructor reference, name, nationality, and URL.
- `constructor_standings.csv` - Contains constructor standings data for each race, including the constructor standings ID, race ID, constructor ID, points, position, position text, and number of wins.

The CSV files are read into the project using the pandas library.

## Plotting Functions

The project includes several plotting functions that generate different types of graphs based on the selected year, race, and plot option. These functions make use of the matplotlib library to create the plots. The available plotting functions are as follows:

1. `plot_boxplot(race_id)` - Generates a boxplot of lap times for each driver in the selected grand prix race.
2. `plot_lineplot(race_id)` - Generates a lineplot showing the lap-by-lap race pace smoothed over a moving average window for each driver.
3. `plot_position_per_lap(race_id)` - Generates a line graph showing the position of each driver over the course of the race.
4. `plot_drivers_standings(race_id)` - Generates a horizontal bar graph showing the cumulative points earned by each driver up to and including the selected race.
5. `plot_constructor_standings(race_id)` - Generates a horizontal bar graph showing the cumulative points earned by each constructor up to and including the selected race.

These plotting functions take a `race_id` parameter, which specifies the ID of the race to be plotted. The necessary data is retrieved from the CSV files based on the selected year and grand prix name, and then the respective plot is generated and displayed in the GUI window.

## Color Mapping

The project includes a dictionary, `constructor_colors`, which maps constructor names to specific colors. These colors are used to visually differentiate the data points in the generated plots based on the constructor of each driver. The color mapping can be customized by modifying the `constructor_colors` dictionary in the constructors_colors.py file.

## Acknowledgements

The Formula 1 race data used in this project is obtained from the public Formula 1 data API (https://ergast.com/mrd/).

## Contact

If you find any bugs, want to drop comments or suggestions, feel free to contact via email: piggythefish@proton.me 

# **Have fun! :)**