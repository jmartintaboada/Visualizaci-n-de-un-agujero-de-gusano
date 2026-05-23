import numpy as np
from scipy.integrate import solve_ivp
from multiprocessing import Pool
from tqdm import tqdm

def geodesics(t, y, r0, b):

    l, theta, phi, pl, ptheta = y
    r = np.sqrt(r0**2 + l**2)
    B2 = ptheta**2 + b**2 / np.sin(theta)**2

    dl_dt = pl
    dtheta_dt = ptheta / r**2
    dphi_dt = b / (r**2 * np.sin(theta)**2)
    dpl_dt = B2 * l / r**4
    dptheta_dt = b**2 / r**2 * np.cos(theta) / np.sin(theta)**3

    return (dl_dt, dtheta_dt, dphi_dt, dpl_dt, dptheta_dt)

def escape_event(t, y, r0, b):
    # Para cuando el rayo esté muy lejos
    return np.abs(y[0]) - 5000.0
escape_event.terminal = True

def ray_tracing(coords):

    i, j, res, D, r0, r_c, theta_c, fov = coords

    alpha = (np.pi/2) + (i / res - 0.5) * fov
    beta = (j / res - 0.5) * fov

    nl = -np.sin(alpha) * np.cos(beta)
    nphi = -np.sin(alpha) * np.sin(beta)
    ntheta = np.cos(alpha)

    pl = nl
    ptheta = r_c * ntheta
    b = r_c * nphi # * np.sin(theta_c)

    y = [D, theta_c, 0.0, pl, ptheta]

    sol = solve_ivp(geodesics, (0, 10000), y, args=(r0, b), events=escape_event, rtol=1e-5) # Resolvemos las geodésicas

    l_f = sol.y[0][-1]      #l final
    theta_f = sol.y[1][-1]  # Ángulo polar final
    phi_f = sol.y[2][-1]    # Ángulo azimutal final
    
    universe = 1.0 if l_f > 0 else -1.0

    return universe, theta_f, phi_f

if __name__ == '__main__':
    res = 720 
    D, r0 = 5, 1
    r_c = np.sqrt(r0**2 + D**2)
    theta_c = np.pi/2
    fov = np.pi/2

    print(f"Iniciando cálculo de {res}x{res} píxeles...")

    coords = [(i, j, res, D, r0, r_c, theta_c, fov) 
              for i in range(res) for j in range(res)]

    with Pool() as pool:
        results = list(tqdm(pool.imap(ray_tracing, coords, chunksize=100), 
                            total=len(coords), 
                            desc="Progreso", 
                            unit="px"))

    mapa = np.array(results).reshape(res,res,3)
    np.save(f'map{res}p D={D}.npy', mapa)
    print("¡Cálculo finalizado y guardado!")
