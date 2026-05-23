Este código permite la simulación visual de un agujero de gusano transitable a partir de la integración numérica de las geodésicas nulas en la métrica de Ellis.

* **`geodesics.py`**: Integra las las geodésicas nulas y genera un mapa de datos en formato `.npy` con los ángulos y universos de salida finales para cada rayo de luz.
* **`visualizacion.py`**: Carga el mapa `.npy` precalculado y renderiza la imagen final aplicando un mapeo equirectangular sobre las texturas de los universos de fondo (`univ1.jpg` y `univ2.jpg`). 

El repositorio ya incluye un mapa de ejemplo precalculado (`map720p D=5.npy`) con una resolución de 720p y un parámetro $D=5$. Si se desea modificar la resolución o las condiciones iniciales, se pueden cambiar estos parámetros directamente en `geodesics.py`.

Al ejecutar `visualizacion.py`, además de mostrar un render de prueba, se generará una secuencia de 120 fotogramas dentro de la carpeta `/frames` que simulan una órbita completa alrededor del agujero de gusano.

### Cómo generar el vídeo
Para unir los fotogramas generados en un vídeo a 30 FPS, se puede utilizar la herramienta **FFmpeg** ejecutando el siguiente comando en la consola:

```bash
ffmpeg -r 30 -i frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p wormhole_animation.mp4
