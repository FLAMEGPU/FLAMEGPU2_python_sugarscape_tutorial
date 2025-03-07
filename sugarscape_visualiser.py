import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import numpy as np
import traceback 

DATA_DIR = "data"
grid = np.array([])
loaded_steps = 0

def load_data(state_count):
    global grid
    global loaded_steps
    try:
        for i in range(state_count+1):
            file_path = f"{DATA_DIR}/{i}.json"
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
    
            agents = data.get("agents", {}).get("agent", {}).get("default", [])
            
            if not agents:
                print("No agent data found.")
                return
            
            # Determine grid size
            max_x = max(agent.get('x', 0) for agent in agents)
            max_y = max(agent.get('y', 0) for agent in agents)

            if not grid.any():
                grid = np.zeros((max_x + 1, max_y + 1, state_count+1))
                
            for agent in agents:
                x, y = agent.get('x', 0), agent.get('y', 0)
                env_sugar_level = agent.get('env_sugar_level', 0)
                agent_id = agent.get('agent_id', -1)
                
                if agent_id != -1:
                    grid[x, y, i] = -1  # Mark active agents with -1
                else:
                    grid[x, y, i] = env_sugar_level
        loaded_steps = state_count
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        print(traceback.format_exc())


def plot_state(state):
    """Reads a JSON file and plots sugar levels and active agents."""

    # if grid is empty force reload of data
    if not grid.any() or loaded_steps < state:
        load_data(state)
        
    # Plotting
    plt.figure(figsize=(8, 6))
    cmap = plt.cm.viridis
    cmap.set_under(color='red')  # Mark active agents with a distinct color
    
    im = plt.imshow(grid[:,:,state], origin='lower', cmap=cmap, interpolation='nearest', vmin=0)

    #plot
    plt.title(f"Agent Sugar Level and Active Agents Step {state}")
    plt.colorbar(im)
    plt.show()


def animate_states(state_count):
    """Reads a JSON file and plots sugar levels and active agents."""
    global ani

    # if grid is empty force reload of data
    if not grid.any():
        load_data(state_count)
        
    fig, ax = plt.subplots()
    cmap = plt.cm.viridis
    cmap.set_under(color='red')  # Mark active agents with a distinct color
    
    ims = [] # ims is a list of lists, each row is a list of artists to draw in the
    for i in range(state_count):
        im = ax.imshow(grid[:,:,i], animated=True, cmap=cmap, interpolation='nearest', vmin=0.0)
        if i == 0:
            ax.imshow(grid[:,:,i], animated=True, cmap=cmap, interpolation='nearest', vmin=0.0)  # show an initial one first
        ims.append([im])
    
    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)
    
    # Plotting
    plt.colorbar(im, ax=ax)
    plt.show()



def display_states(state_count):
    """Reads a JSON file and plots sugar levels and active agents."""
    global im
    global slider
    im = slider = None

    # if grid is empty force reload of data
    if not grid.any():
        load_data(state_count)
    
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


