import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import numpy as np
import traceback 

DATA_DIR = "data"
grid = np.array([])
loaded_steps = 0

def unpack(v):
    # Function is required to convert agent variable steps from array to scalars due to bug in RC3
    # I.e. [123] to 123
    return v[0] if isinstance(v, list) else v


def load_data(step_count):
    """Function loads FLAME GPU sugarscape simulation output data (in json format) and stores it in the global grid array"""
    global grid
    global loaded_steps
    try:
        for i in range(step_count+1):
            file_path = f"{DATA_DIR}/{i}.json"
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
    
            agents = data.get("agents", {}).get("agent", {}).get("default", [])
            
            if not agents:
                print("No agent data found.")
                return
            
            # Determine grid size
            max_x = unpack(max(agent.get('x', 0) for agent in agents))
            max_y = unpack(max(agent.get('y', 0) for agent in agents))

            if not grid.any():
                grid = np.zeros((max_x + 1, max_y + 1, step_count+1))
                
            for agent in agents:
                x, y = unpack(agent.get('x', 0)), unpack(agent.get('y', 0))
                env_sugar_level = unpack(agent.get('env_sugar_level', 0))
                agent_id = unpack(agent.get('agent_id', -1))
                
                if agent_id != -1:
                    grid[x, y, i] = -1  # Mark active agents with -1
                else:
                    grid[x, y, i] = env_sugar_level
        loaded_steps = step_count
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        print(traceback.format_exc())


def plot_step(step):
    """
    Plots a single agent step as a matplotlib plot.
    If the data is not loaded then it will be loaded first.
    """

    # if grid is empty force reload of data
    if not grid.any() or loaded_steps < step:
        load_data(step)
        
    # Plotting
    plt.figure(figsize=(8, 6))
    cmap = plt.cm.viridis
    cmap.set_under(color='red')  # Mark active agents with a distinct color
    
    im = plt.imshow(grid[:,:,step], origin='lower', cmap=cmap, interpolation='nearest', vmin=0)

    #plot
    plt.title(f"Agent Sugar Level and Active Agents Step {step}")
    plt.colorbar(im)
    plt.show()


def animate_steps(step_count):
    """
    Plots the simulation outputs as a looping animation.
    If the data is not loaded then it will be loaded first.
    """
    global ani

    # if grid is empty force reload of data
    if not grid.any():
        load_data(step_count)
        
    fig, ax = plt.subplots()
    cmap = plt.cm.viridis
    cmap.set_under(color='red')  # Mark active agents with a distinct color
    
    ims = [] # ims is a list of lists, each row is a list of artists to draw in the
    for i in range(step_count):
        im = ax.imshow(grid[:,:,i], animated=True, cmap=cmap, interpolation='nearest', vmin=0.0)
        if i == 0:
            ax.imshow(grid[:,:,i], animated=True, cmap=cmap, interpolation='nearest', vmin=0.0)  # show an initial one first
        ims.append([im])
    
    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)
    
    # Plotting
    plt.colorbar(im, ax=ax)
    plt.show()



def display_steps(step_count):
    """
    Plots the simulation outputs as an interactive plot with a slider controlling the step number.
    If the data is not loaded then it will be loaded first.
    """
    global im
    global slider
    im = slider = None

    # if grid is empty force reload of data
    if not grid.any():
        load_data(step_count)
    
    fig, ax = plt.subplots()
    cmap = plt.cm.viridis
    cmap.set_under(color='red')  # Mark active agents with a distinct color
    ims = [] # ims is a list of lists
    im = ax.imshow(grid[:,:,0], cmap=cmap, interpolation='nearest', vmin=0.0)
    ax_depth = plt.axes([0.23, 0.02, 0.56, 0.04])
    slider = Slider(ax_depth, 'iteration', 0, grid.shape[2]-1, valinit=0)
    update_slider = lambda v: im.set_data(grid[:, :, int(round(v))])
    slider.on_changed(update_slider)
    
    # Plotting
    plt.colorbar(im, ax=ax)
    plt.show()


