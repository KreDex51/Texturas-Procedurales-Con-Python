import noise
import numpy as np
import matplotlib.pyplot as plt
import random

def generate_noise_layer(scale, octaves, persistence, lacunarity, width, height, seed):
    random.seed(seed)
    base = random.randint(0, 100)
    
    layer = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            layer[y][x] = noise.pnoise2(x / scale,
                                        y / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=width,
                                        repeaty=height,
                                        base=base)
    layer = (layer - np.min(layer)) / (np.max(layer) - np.min(layer))  # Normalizar
    return layer

# Parámetros de la textura
width, height = 512, 512
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

# Semilla para la generación del ruido
seed = random.randint(0, 10000)  # Cambia la semilla en cada ejecución

# Generar capas de ruido para cada canal de color
red_layer = generate_noise_layer(scale, octaves, persistence, lacunarity, width, height, seed)
green_layer = generate_noise_layer(scale * 1.5, octaves, persistence, lacunarity, width, height, seed + 1)
blue_layer = generate_noise_layer(scale * 2.0, octaves, persistence, lacunarity, width, height, seed + 2)

# Combinar las capas en una imagen RGB
texture_color = np.dstack((red_layer, green_layer, blue_layer))

# Mostrar la textura en color
plt.imshow(texture_color)
plt.title(f'Textura Procedural en Color con Ruido Perlin (Semilla: {seed})')
plt.show()

def map_colors_tierra(layer):
    return np.stack((
        np.interp(layer, (0, 1), (139/255, 205/255)),  # Red
        np.interp(layer, (0, 1), (69/255, 133/255)),   # Green
        np.interp(layer, (0, 1), (19/255, 56/255))     # Blue
    ), axis=-1)

# Parámetros ajustados para tierra
scale_tierra = 50.0
octaves_tierra = 4
persistence_tierra = 0.4
lacunarity_tierra = 2.0

# Generar capa de ruido
layer_tierra = generate_noise_layer(scale_tierra, octaves_tierra, persistence_tierra, lacunarity_tierra, width, height, seed)
texture_tierra = map_colors_tierra(layer_tierra)

# Mostrar textura de tierra
plt.imshow(texture_tierra)
plt.title(f'Textura de Tierra (Semilla: {seed})')
plt.show()

def map_colors_cielo(layer):
    return np.stack((
        np.interp(layer, (0, 1), (135/255, 255/255)),  # Red
        np.interp(layer, (0, 1), (206/255, 255/255)),  # Green
        np.interp(layer, (0, 1), (235/255, 255/255))   # Blue
    ), axis=-1)

# Parámetros ajustados para cielo
scale_cielo = 150.0
octaves_cielo = 3
persistence_cielo = 0.5
lacunarity_cielo = 2.0

# Generar capa de ruido
layer_cielo = generate_noise_layer(scale_cielo, octaves_cielo, persistence_cielo, lacunarity_cielo, width, height, seed)
texture_cielo = map_colors_cielo(layer_cielo)

# Mostrar textura de cielo
plt.imshow(texture_cielo)
plt.title(f'Textura de Cielo (Semilla: {seed})')
plt.show()


def map_colors_pared_rocosa(layer):
    return np.stack((
        np.interp(layer, (0, 1), (105/255, 169/255)),  # Red
        np.interp(layer, (0, 1), (105/255, 169/255)),  # Green
        np.interp(layer, (0, 1), (105/255, 169/255))   # Blue
    ), axis=-1)

# Parámetros ajustados para pared rocosa
scale_pared_rocosa = 30.0
octaves_pared_rocosa = 5
persistence_pared_rocosa = 0.6
lacunarity_pared_rocosa = 2.5

# Generar capa de ruido
layer_pared_rocosa = generate_noise_layer(scale_pared_rocosa, octaves_pared_rocosa, persistence_pared_rocosa, lacunarity_pared_rocosa, width, height, seed)
texture_pared_rocosa = map_colors_pared_rocosa(layer_pared_rocosa)

# Mostrar textura de pared rocosa
plt.imshow(texture_pared_rocosa)
plt.title(f'Textura de Pared Rocosa (Semilla: {seed})')
plt.show()
