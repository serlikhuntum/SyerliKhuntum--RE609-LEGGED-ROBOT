import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def run_forward_kaki_nyata():
    # =========================
    # PARAMETER ASLI KAKI KAMU
    # =========================
    L_coxa  = 22.50
    L_femur = 60.00
    L_tibia = 71.45

    # Membuat deret waktu untuk pergerakan sudut
    t = np.linspace(0, 40, 1200)

    # Trajectory Sudut (Dalam Radian)
    # Kita buat gerakan osilasi (maju-mundur/naik-turun)
    theta_femur = 0.5 * np.sin(0.3 * t)  # Gerakan paha
    theta_tibia = -0.8 * np.cos(0.5 * t) # Gerakan lutut

    # =========================
    # SETUP VISUAL
    # =========================
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8,8))

    # Skala disesuaikan dengan jangkauan total kaki (~154mm)
    ax.set_xlim(-10, 180)
    ax.set_ylim(-100, 100)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)

    # Robot links
    line_coxa,  = ax.plot([], [], '-', color='white', lw=6, label='Coxa (Static)')
    line_femur, = ax.plot([], [], 'o-', color='cyan', lw=5, label='Femur')
    line_tibia, = ax.plot([], [], 'o-', color='magenta', lw=5, label='Tibia')

    # Trajectory (Jejak Permanen)
    traj, = ax.plot([], [], color='orange', lw=1.5, alpha=0.6)

    text = ax.text(5, -90, '', color='white', family='monospace',
                   bbox=dict(facecolor='black', alpha=0.6, edgecolor='white'))

    x_hist, z_hist = [], []

    # =========================
    # UPDATE ANIMATION
    # =========================
    def update(i):
        # Sudut saat ini
        tf = theta_femur[i]
        tt = theta_tibia[i]

        # Forward Kinematics (X, Z view samping)
        # Titik 0: Base
        x0, z0 = 0, 0
        
        # Titik 1: Akhir Coxa (Static offset)
        x1, z1 = L_coxa, 0
        
        # Titik 2: Akhir Femur (Lutut)
        x2 = x1 + L_femur * np.cos(tf)
        z2 = z1 + L_femur * np.sin(tf)
        
        # Titik 3: Akhir Tibia (Ujung Kaki)
        # Ingat: Tibia dipengaruhi oleh sudut Femur juga
        x3 = x2 + L_tibia * np.cos(tf + tt)
        z3 = z2 + L_tibia * np.sin(tf + tt)

        # Draw Robot
        line_coxa.set_data([x0, x1], [z0, z1])
        line_femur.set_data([x1, x2], [z1, z2])
        line_tibia.set_data([x2, x3], [z2, z3])

        # Jejak Permanen (Tetap berjalan)
        x_hist.append(x3)
        z_hist.append(z3)
        traj.set_data(x_hist, z_hist)

        # Info text
        text.set_text(
            f"Forward Kinematics\n"
            f"X: {x3:.2f} mm\n"
            f"Z: {z3:.2f} mm"
        )

        return line_coxa, line_femur, line_tibia, traj, text

    # =========================
    # ANIMATION (Looping Non-stop)
    # =========================
    anim = FuncAnimation(
        fig,
        update,
        frames=len(t),
        interval=30,
        repeat=True # Putaran tidak berhenti
    )

    plt.title(f"3 DOF Real Scale: Forward Kinematics\nCoxa:{L_coxa} Femur:{L_femur} Tibia:{L_tibia}", 
              fontsize=12, weight='bold')
    plt.legend(loc='upper right')
    plt.show()

# RUN
if __name__ == "__main__":
    run_forward_kaki_nyata()