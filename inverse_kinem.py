import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def run_simulasi_kaki_nonstop():
    # ==========================================
    # 1. PARAMETER ASLI KAKI KAMU (mm)
    # ==========================================
    L_coxa  = 22.50
    L_femur = 60.00
    L_tibia = 71.45

    # Titik target untuk membentuk jalur gerakan (X, Z)
    targets = [(100, -40), (140, -40), (140, 20), (100, 40), (70, 0)]

    x_traj, z_traj = [], []
    for i in range(len(targets)):
        p0 = targets[i]
        p1 = targets[(i+1) % len(targets)]
        t = np.linspace(0, 1, 50) 
        x_traj.extend(p0[0] + (p1[0] - p0[0]) * t)
        z_traj.extend(p0[1] + (p1[1] - p0[1]) * t)

    # =========================
    # SETUP VISUAL
    # =========================
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.set_xlim(-10, 180)
    ax.set_ylim(-100, 100)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.2)

    # Objek Gambar
    line_coxa, = ax.plot([], [], color='white', lw=6, label='Coxa Offset')
    line_femur, = ax.plot([], [], 'o-', color='cyan', lw=5, label='Femur')
    line_tibia, = ax.plot([], [], 'o-', color='magenta', lw=5, label='Tibia')
    
    # Trajectory (Jejak Permanen)
    traj, = ax.plot([], [], color='yellow', lw=1.5, alpha=0.6)
    target_dot, = ax.plot([], [], 'ro', markersize=6)
    
    text_info = ax.text(5, -90, '', color='white', family='monospace')

    x_hist, z_hist = [], []

    def update(i):
        tx = x_traj[i]
        tz = z_traj[i]

        # --- INVERSE KINEMATICS ---
        r = tx - L_coxa
        s = math.sqrt(r**2 + tz**2)

        cos_gamma = (L_femur**2 + L_tibia**2 - s**2) / (2 * L_femur * L_tibia)
        cos_gamma = np.clip(cos_gamma, -1, 1)
        gamma = math.acos(cos_gamma) - math.pi 

        phi1 = math.atan2(tz, r)
        cos_beta_inner = (L_femur**2 + s**2 - L_tibia**2) / (2 * L_femur * s)
        cos_beta_inner = np.clip(cos_beta_inner, -1, 1)
        beta = phi1 + math.acos(cos_beta_inner)

        # --- FORWARD KINEMATICS ---
        x1, z1 = L_coxa, 0
        x2 = x1 + L_femur * math.cos(beta)
        z2 = z1 + L_femur * math.sin(beta)
        x3 = x2 + L_tibia * math.cos(beta + gamma)
        z3 = z2 + L_tibia * math.sin(beta + gamma)

        # Update data visual
        line_coxa.set_data([0, x1], [0, 0])
        line_femur.set_data([x1, x2], [z1, z2])
        line_tibia.set_data([x2, x3], [z2, z3])
        target_dot.set_data([tx], [tz])
        
        # Tambahkan ke histori tanpa reset
        x_hist.append(x3)
        z_hist.append(z3)
        traj.set_data(x_hist, z_hist) 

        text_info.set_text(
            f"POS X: {x3:>6.2f} | Z: {z3:>6.2f}\n"
            f"BETA : {math.degrees(beta):>5.1f}°\n"
            f"GAMMA: {math.degrees(gamma):>5.1f}°"
        )

        return line_coxa, line_femur, line_tibia, target_dot, traj, text_info

    # repeat=True agar animasi terus berputar
    anim = FuncAnimation(fig, update, frames=len(x_traj), interval=20, repeat=True)
    
    plt.title("Simulasi Kaki Hexapod - Loop Non-Stop", weight='bold', pad=20)
    plt.show()

if __name__ == "__main__":
    run_simulasi_kaki_nonstop()