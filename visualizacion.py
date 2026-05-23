import matplotlib.pyplot as plt
import numpy as np
import os

def render(mapa, img_a, img_b, rot):
    res = mapa.shape[0]
    universo = mapa[:, :, 0]
    theta = mapa[:, :, 1]
    phi = mapa[:, :, 2]

    # Normalizar ángulos a coordenadas [0, 1]
    v = (theta % np.pi) / np.pi
    u = ((phi + np.radians(rot)) % (2 * np.pi)) / (2 * np.pi)

    #Coordenadas px
    h_a, w_a = img_a.shape[:2]
    y_a = (v * (h_a - 1)).astype(int)
    x_a = (u * (w_a - 1)).astype(int)

    h_b, w_b = img_b.shape[:2]
    y_b = (v * (h_b - 1)).astype(int)
    x_b = (u * (w_b - 1)).astype(int)

    final_img = np.zeros((res, res, 3))

    mask_a = (universo > 0)
    mask_b = (universo < 0)

    final_img[mask_a] = img_a[y_a[mask_a], x_a[mask_a]]
    final_img[mask_b] = img_b[y_b[mask_b], x_b[mask_b]]

    return final_img, res

D = 5
file = 'map720p D=5.npy'
mapa = np.load(file)

img_1 = plt.imread('univ1.jpg')[..., :3]
img_2 = plt.imread('univ2.jpg')[..., :3]

if img_1.max() > 1.0: img_1 = img_1 / 255.0
if img_2.max() > 1.0: img_2 = img_2 / 255.0

imagen_final, res = render(mapa, img_1, img_2, rot=90)
plt.imshow(imagen_final)
plt.axis('off')
plt.imsave(f"wormhole_{res}p_D={D}.png", imagen_final)
plt.show()

#Generamos los frames para crear la animación:
if not os.path.exists('frames'):
    os.makedirs('frames')

num_frames = 120
paso_angulo = 360 / num_frames

print("Generando frames...")
for f in range(num_frames):
    angulo = f * paso_angulo
    frame_img = render(mapa, img_1, img_2, rot=angulo)[0]
    plt.imsave(f'frames/frame_{f:03d}.png', frame_img)
print('Listo!')
#Con estos frames se puede generar un vídeo utilizando, por ejemplo, la herramienta FFmpeg, escribiendo el siguiente comando en la consola:
#ffmpeg -r 30 -i frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p wormhole_animation.mp4