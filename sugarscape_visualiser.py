import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import numpy as np
import traceback # temp

DATA_DIR = "data"

def plot_state(state):
    """Reads a JSON file and plots sugar levels and active agents."""
    try:
        file_path = f"{DATA_DIR}/{state}.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        agents = data.get("agents", {}).get("agent", {}).get("default", [])
        
        if not agents:
            print("No agent data found.")
            return
        
        # Determine grid size
        max_x = max(agent.get('x', 0) for agent in agents)
        max_y = max(agent.get('y', 0) for agent in agents)
        grid = np.zeros((max_x + 1, max_y + 1))
        
        for agent in agents:
            x, y = agent.get('x', 0), agent.get('y', 0)
            env_sugar_level = agent.get('env_sugar_level', 0)
            sugar_level = agent.get('sugar_level', 0)
            agent_id = agent.get('agent_id', -1)
            
            if agent_id != -1:
                grid[y, x] = -1  # Mark active agents with -1
            else:
                grid[y, x] = env_sugar_level

            #grid[x, y] = sugar_level
        
        # Plotting
        plt.figure(figsize=(8, 6))
        cmap = plt.cm.viridis
        cmap.set_under(color='red')  # Mark active agents with a distinct color
        
        plt.imshow(grid, origin='lower', cmap=cmap, interpolation='nearest', vmin=0)
        plt.colorbar(label='Sugar Level')
        plt.title("Agent Sugar Level and Active Agents")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.show()
    except Exception as e:
        print(f"Error reading JSON file: {e}")

def animate_states(state_count):
    """Reads a JSON file and plots sugar levels and active agents."""
    try:
        fig, ax = plt.subplots()
        cmap = plt.cm.viridis
        cmap.set_under(color='red')  # Mark active agents with a distinct color
        
        ims = [] # ims is a list of lists, each row is a list of artists to draw in the
        for i in range(state_count):
            file_path = f"{DATA_DIR}/{i+1}.json"
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
    
            agents = data.get("agents", {}).get("agent", {}).get("default", [])
            
            if not agents:
                print("No agent data found.")
                return
            
            # Determine grid size
            max_x = max(agent.get('x', 0) for agent in agents)
            max_y = max(agent.get('y', 0) for agent in agents)
            
            grid = np.zeros((max_x + 1, max_y + 1))
                
            for agent in agents:
                x, y = agent.get('x', 0), agent.get('y', 0)
                env_sugar_level = agent.get('env_sugar_level', 0)
                sugar_level = agent.get('sugar_level', 0)
                agent_id = agent.get('agent_id', -1)
                
                if agent_id != -1:
                    grid[y, x] = -1  # Mark active agents with -1
                else:
                    grid[y, x] = env_sugar_level
    
                #grid[x, y] = sugar_level

            im = ax.imshow(grid, animated=True, cmap=cmap, interpolation='nearest', vmin=0.0)
            if i == 0:
                ax.imshow(grid, animated=True, cmap=cmap, interpolation='nearest', vmin=0.0)  # show an initial one first
            ims.append([im])


        
        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
        
        # Plotting

        plt.show()

        return ani
    except Exception as e:
        print(f"Error reading JSON file: {e}")


def display_states(state_count):
    """Reads a JSON file and plots sugar levels and active agents."""
    global grid
    global im
    global slider
    grid = np.array([])
    im = slider = None
    try:
        fig, ax = plt.subplots()
        cmap = plt.cm.viridis
        cmap.set_under(color='red')  # Mark active agents with a distinct color
        
        ims = [] # ims is a list of lists, each row is a list of artists to draw in the
        for i in range(state_count):
            file_path = f"{DATA_DIR}/{i+1}.json"
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
                grid = np.zeros((max_x + 1, max_y + 1, state_count))
                
            for agent in agents:
                x, y = agent.get('x', 0), agent.get('y', 0)
                env_sugar_level = agent.get('env_sugar_level', 0)
                sugar_level = agent.get('sugar_level', 0)
                agent_id = agent.get('agent_id', -1)
                
                if agent_id != -1:
                    grid[x, y, i] = -1  # Mark active agents with -1
                else:
                    grid[x, y, i] = env_sugar_level
    
                #grid[x, y] = sugar_level

        im = ax.imshow(grid[:,:,0], cmap=cmap, interpolation='nearest', vmin=0.0)

        ax_depth = plt.axes([0.23, 0.02, 0.56, 0.04])
        slider = Slider(ax_depth, 'iteration', 0, grid.shape[2], valinit=idx)

        update_slider = lambda v: im.set_data(grid[:, :, int(round(v))])
        slider.on_changed(update_slider)
        
        # Plotting
        plt.show()
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        print(traceback.format_exc())




    

if __name__ == "__main__":
    file_path = "data/6.json"  # Change this to your actual JSON file path
    animate_states(10)
