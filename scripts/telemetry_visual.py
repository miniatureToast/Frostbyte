import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output/plow_telemetry.csv")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot Linear Forces
ax1.plot(df["Time (s)"], df["Force_X (N)"], label="X (Forward Resistance)", color="tab:red")
ax1.plot(df["Time (s)"], df["Force_Y (N)"], label="Y (Sideways Load)", color="tab:blue", alpha=0.7)
ax1.plot(df["Time (s)"], df["Force_Z (N)"], label="Z (Vertical Lift/Press)", color="tab:green", alpha=0.7)
ax1.set_ylabel("Force (Newtons)")
ax1.set_title("Snow Plow Structural Load Telemetry")
ax1.legend()
ax1.grid(True)

# Plot Rotational Torques
ax2.plot(df["Time (s)"], df["Torque_Pitch (Nm)"], label="Pitch Torque (Blade Tipping)", color="tab:orange")
ax2.plot(df["Time (s)"], df["Torque_Yaw (Nm)"], label="Yaw Torque (Steering Twist)", color="tab:purple", alpha=0.7)
ax2.plot(df["Time (s)"], df["Torque_Roll (Nm)"], label="Roll Torque", color="tab:brown", alpha=0.7)
ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Torque (N·m)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("output/stress_telemetry.png", dpi=300)
plt.show()