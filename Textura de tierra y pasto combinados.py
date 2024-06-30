import numpy as np
import noise
import matplotlib.pyplot as plt
import random

# Función para generar ruido Perlin
def generate_perlin_noise(scale, width, height, seed, octaves, persistence, lacunarity):
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
                                        base=seed)
    layer = (layer - np.min(layer)) / (np.max(layer) - np.min(layer))  # Normalizar
    return layer

# Función para mapear los colores de tierra
def map_colors_tierra(layer):
    return np.stack((
        np.interp(layer, (0, 1), (139/255, 205/255)),  # Red
        np.interp(layer, (0, 1), (69/255, 133/255)),   # Green
        np.interp(layer, (0, 1), (19/255, 56/255))     # Blue
    ), axis=-1)

# Parámetros ajustados para tierra
scale_tierra = 50.0
octaves_tierra = 6
persistence_tierra = 0.6
lacunarity_tierra = 2.0

# Función para mapear los colores de pasto
def map_colors_pasto(layer):
    return np.stack((
        np.interp(layer, (0, 1), (34/255, 85/255)),   # Red
        np.interp(layer, (0, 1), (139/255, 180/255)),  # Green
        np.interp(layer, (0, 1), (34/255, 85/255))     # Blue
    ), axis=-1)

# Parámetros ajustados para pasto
scale_pasto = 25.0
octaves_pasto = 3
persistence_pasto = 0.5
lacunarity_pasto = 2.0

# Dimensiones de la textura
width, height = 1024, 1024
seed_tierra = random.randint(0, 100)
seed_pasto = random.randint(0, 100)

# Generar ruido Perlin para tierra y piedra
layer_tierra = generate_perlin_noise(scale_tierra, width, height, seed_tierra, octaves_tierra, persistence_tierra, lacunarity_tierra)
layer_pasto = generate_perlin_noise(scale_pasto, width, height, seed_pasto, octaves_pasto, persistence_pasto, lacunarity_pasto)


# Mapear los colores de tierra y piedra
textura_tierra = map_colors_tierra(layer_tierra)
textura_pasto = map_colors_pasto(layer_pasto)
# Crear una máscara de gradiente horizontal
gradient = np.linspace(0, 1, width)

# Expandir la máscara de gradiente para que se aplique a toda la altura de la imagen
mask = np.tile(gradient, (height, 1))

# Añadir una nueva dimensión a la máscara para que coincida con las dimensiones de las texturas
mask = mask[:, :, np.newaxis]

# Mezclar las dos texturas usando la máscara
combined_texture = textura_tierra * (1 - mask) + textura_pasto * mask

# Mostrar la textura combinada
plt.imshow(combined_texture)
plt.title(f'Textura de tierra con pasto (Semilla tierra: {seed_tierra} Semilla pasto: {seed_pasto} )')
plt.axis('off')
plt.show()
