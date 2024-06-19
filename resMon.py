import paramiko
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.64.34.32', username='suraj', password='suraj')

# Lists to store values
cpu_percentages = []
ram_percentages = []
timestamps = []
curr_op = ['']

# Create figure for plotting
fig, ax1 = plt.subplots()

# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_xlabel('time (s)')
ax1.set_ylabel('CPU Usage (%)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('RAM Usage (%)', color='tab:red')  # we already handled the x-label with ax1
ax2.tick_params(axis='y', labelcolor='tab:red')

# Function to get data
def get_data():
    stdin, stdout, stderr = ssh.exec_command("echo $(ps -eo pcpu | awk 'BEGIN {sum=0.0f} {sum+=$1} END {print sum}') $(free | grep Mem | awk '{print $3/$2 * 100.0}')")
    output = stdout.readlines()[0].strip().split()
    cpu_percentages.append(float(output[0]))
    ram_percentages.append(float(output[1]))
    timestamps.append(time.time())
    curr_op[0] = output

    # Keep only last 3 minutes of data
    current_time = time.time()
    
    while timestamps and current_time - timestamps[0] > 180:
        timestamps.pop(0)
        cpu_percentages.pop(0)
        ram_percentages.pop(0)

# Function to update plot
def update(i):
    get_data()
    ax1.clear()
    ax2.clear()
    ax1.plot(timestamps, cpu_percentages, label='CPU Usage (%)', color='tab:blue')
    ax2.plot(timestamps, ram_percentages, label='RAM Usage (%)', color='tab:red')
    ax1.set_xlabel(curr_op[0])
    ax1.set_ylabel('CPU Usage (%)', color='tab:blue')
    ax2.set_ylabel('RAM Usage (%)', color='tab:red')  # we already handled the x-label with ax1
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.yaxis.set_label_position("right")

# Create animation
ani = animation.FuncAnimation(fig, update, interval=1000)

# Show plot
plt.show()
