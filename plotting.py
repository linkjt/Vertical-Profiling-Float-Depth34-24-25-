import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import pyautogui
import platform
from AppKit import NSApplication, NSApp, NSWindow

# TODO (for fun): Just make buttons in order to actually implement my original idea of consts however, isn't necessary
# TODO: Set up server with appropriate data 
url = 'http://127.0.0.1:5000/data'
unit = "hPa"
consts = {"hPa": 1013.25, "atm": 1, "Pa": 101325, "mmHg": 760}
begin_const = consts[unit]
times = [0]
pressures = [begin_const]
distances = [0]
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.2) 
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

graph, = ax.plot(times, pressures, color=colors[0])
graph2, = ax2.plot(times, distances, color=colors[1])

test = input("T or F: ")
flag = (test == 'T')
counter = 0
pCounter = 0
dCounter = 0
def pToDistance(pressure):
    """
    p = pgh
    where,

    p is the pressure exerted by the liquid in N.m-2 or Pa
    ρ is the density of the liquid in kg.m-3, slugs.ft-3
    g is the acceleration due to gravity taken as 9.81m.s-2
    h is the height of the fluid column in m

    """
    convert_p = pressure/consts[unit] * consts["Pa"]
    h = convert_p/(9.81*997)
    return h
    
# Update our graph by grabbing a request
def update(frame):
    global times
    global pressures
    global counter
    global pCounter
    if flag:
        counter += 1
        times.append(counter)  
        pCounter += 1
        pressures.append(pCounter) 
    else:
        response = requests.get(url)
        # Response will be a JSON file
        if response.status_code == 200:
            d = response.json()
            items_list = list(d.items())
            time = items_list[-1][0]
            pressure = items_list[-1][1]
            pressure *= consts[unit]
            times.append(time) 
            pressures.append(pressure)  
        else:
            sys.exit("Server error [Can't receive data]")
    
    graph.set_xdata(times)
    graph.set_ydata(pressures)
    ax.relim()
    ax.autoscale_view()
    ax.set_xlim([min(times), max(times)])  # Explicitly set x-axis limits
    ax.set_ylim([min(pressures), max(pressures)])  # Explicitly set y-axis limits

    # Redraw the canvas
    fig.canvas.draw()

def update2(frame):
    global times
    global distances
    global counter
    global dCounter
    if flag:
        dCounter += 10
        distances.append(dCounter) 
    else:
        response = requests.get(url)
        # Response will be a JSON file
        if response.status_code == 200:
            d = response.json()
            items_list = list(d.items())
            time = items_list[-1][0]
            pressure = items_list[-1][1]
            pressure *= consts[unit]
            newD = pToDistance(pressure)
            times.append(time)  # Corrected to append a new value
            distances.append(newD)  # Corrected to append a new value
        else:
            sys.exit("Server error [Can't receive data]")
    
    graph2.set_xdata(times)
    graph2.set_ydata(distances)
    ax2.relim()
    ax2.autoscale_view()
    ax2.set_ylim([min(distances), max(distances)])  # Explicitly set x-axis limits
    ax2.set_xlim([min(times), max(times)]) # Explicitly set y-axis limits
    print(f"{times[-1]} {distances[-1]}")

    # Redraw the canvas
    fig.canvas.draw()


# Use set_ylabel() and set_xlabel() instead of ylabel() and xlabel()
ax.set_ylabel(f"Pressure ({unit})")
ax.set_xlabel(f"Time (s)")
ax.set_title(f"Pressure vs Time")
ax2.set_xlabel(f"Time (s)")
ax2.set_ylabel(f"Distance (m)")
ax2.set_title(f"Distance vs Time")

# Set up the animation
anim = animation.FuncAnimation(fig, update, interval=1000, frames=None, cache_frame_data=False)
anim2 = animation.FuncAnimation(fig, update2, interval = 1000, frames=None, cache_frame_data=False)
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()

