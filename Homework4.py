import matplotlib.pyplot as plt

def calculate_energy(power, duration_min):
    duration_hr = duration_min / 60
    return power * duration_hr

def get_battery_status(remaining, capacity):
    if remaining <= 0:
        return "BATTERY DEPLETED"
    elif remaining / capacity <= 0.20:
        return "LOW BATTERY"
    else:
        return "NORMAL"

battery_capacity = 36.0
battery_remaining = battery_capacity
total_time = 0.0
total_energy = 0.0

power_dict = {
    "standby": 3,
    "sensing": 8,
    "drive": 30,
    "transmit": 18
}

times = [0]
battery_levels = [battery_capacity]

with open("battery_schedule.csv", "r") as file:
    header = file.readline()
    for line in file:
        line = line.strip()
        if line:
            parts = line.split(",")
            mode = parts[0]
            duration = float(parts[1])
            
            power = power_dict[mode]
            energy_used = calculate_energy(power, duration)
            
            total_time += duration
            battery_remaining -= energy_used
            total_energy += energy_used
            
            times.append(total_time)
            battery_levels.append(battery_remaining)
            
            status = get_battery_status(battery_remaining, battery_capacity)
            print(f"Mode: {mode}, Duration: {duration} min, Energy Used: {energy_used:.2f} Wh, Battery Remaining: {battery_remaining:.2f} Wh, Status: {status}")

percent_remaining = (battery_remaining / battery_capacity) * 100

print("\nFinal Simulation Summary:")
print(f"Total operating time: {total_time} minutes")
print(f"Total energy required: {total_energy:.2f} Wh")
print(f"Battery energy remaining: {battery_remaining:.2f} Wh")
print(f"Percentage of battery remaining: {percent_remaining:.1f}%")

if battery_remaining > 0:
    print("The battery can complete the full schedule.")
else:
    print("The battery cannot complete the full schedule.")

plt.figure()
plt.plot(times, battery_levels, marker="o")
plt.title("Battery Energy Remaining Over Time")
plt.xlabel("Elapsed Time (minutes)")
plt.ylabel("Battery Remaining (Wh)")
plt.grid(True)
plt.savefig("battery_runtime.png")
