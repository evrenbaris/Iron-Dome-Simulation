import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from IPython.display import HTML
from google.colab import files

# Simulation parameters
time_step = 0.1
simulation_time = 20
num_threats = 5  # Number of threat rockets

# Generate random threat rockets
threat_starts = np.random.rand(num_threats, 2) * 100  # Random starting positions
threat_targets = np.random.rand(num_threats, 2) * 100  # Random target positions
threat_positions = threat_starts.copy()
threat_velocities = (threat_targets - threat_starts) / 100  # Fixed speed for all threats

# Defense rockets
defense_start = np.array([50, 50], dtype=float)  # Launch position for all defense rockets
defense_positions = np.array([defense_start] * num_threats)
defense_velocities = np.zeros((num_threats, 2), dtype=float)

# Defense zone parameters
defense_radius = 20

# Function to calculate defense velocity
def calculate_defense_velocity(threat_pos, defense_pos):
    direction = threat_pos - defense_pos
    norm = np.linalg.norm(direction)
    if norm == 0:  # Avoid division by zero
        return np.array([0, 0], dtype=float)
    return direction / norm * 1.5  # Slightly faster than threat rocket

# Visualization setup
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Add defense zone
defense_circle = plt.Circle(defense_start, defense_radius, color='blue', fill=False, linestyle='--', label="Defense Zone")
ax.add_artist(defense_circle)

# Add rocket launch pad
ax.scatter(defense_start[0], defense_start[1], color='black', marker='^', s=100, label="Rocket Launch Pad")

# Scatter plots for rockets and collisions
threat_scatter = ax.scatter([], [], color='red', label="Threat Rockets")
defense_scatter = ax.scatter([], [], color='green', label="Defense Rockets")
collision_marker = ax.scatter([], [], color='orange', label="Collisions", s=100)

# Collision detection
collision_detected = np.zeros(num_threats, dtype=bool)

# Update function for animation
def update(frame):
    global threat_positions, defense_positions, defense_velocities, collision_detected

    for i in range(num_threats):
        if not collision_detected[i]:
            # Update threat position
            threat_positions[i] += threat_velocities[i] * time_step

            # Update defense position
            defense_velocities[i] = calculate_defense_velocity(threat_positions[i], defense_positions[i])
            defense_positions[i] += defense_velocities[i] * time_step

            # Check for collision
            distance = np.linalg.norm(threat_positions[i] - defense_positions[i])
            if distance < 1:  # Collision threshold
                collision_detected[i] = True

    # Update visualization
    active_threat_positions = threat_positions[~collision_detected]
    active_defense_positions = defense_positions[~collision_detected]
    collision_positions = (threat_positions[collision_detected] + defense_positions[collision_detected]) / 2

    threat_scatter.set_offsets(active_threat_positions)
    defense_scatter.set_offsets(active_defense_positions)
    if collision_positions.size > 0:
        collision_marker.set_offsets(collision_positions)

    return threat_scatter, defense_scatter, collision_marker

ani = FuncAnimation(fig, update, frames=int(simulation_time / time_step), interval=50, blit=True)

# Save animation as GIF
gif_filename = "iron_dome_simulation.gif"
ani.save(gif_filename, writer=PillowWriter(fps=20))

# Download the GIF
files.download(gif_filename)
