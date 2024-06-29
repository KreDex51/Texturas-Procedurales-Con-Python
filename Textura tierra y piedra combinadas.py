import numpy as np
import noise
import matplotlib.pyplot as plt

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

# Función para mapear los colores de piedra
def map_colors_piedra(layer):
    return np.stack((
        np.interp(layer, (0, 1), (105/255, 169/255)),  # Red
        np.interp(layer, (0, 1), (105/255, 169/255)),  # Green
        np.interp(layer, (0, 1), (105/255, 169/255))   # Blue
    ), axis=-1)

# Parámetros ajustados para tierra
scale_tierra = 50.0
octaves_tierra = 6
persistence_tierra = 0.6
lacunarity_tierra = 2.0

# Parámetros ajustados para piedra
scale_piedra = 100.0
octaves_piedra = 8
persistence_piedra = 0.6
lacunarity_piedra = 2.5

# Dimensiones de la textura
width, height = 512, 512
seed_tierra = 42
seed_piedra = 43

# Generar ruido Perlin para tierra y piedra
layer_tierra = generate_perlin_noise(scale_tierra, width, height, seed_tierra, octaves_tierra, persistence_tierra, lacunarity_tierra)
layer_piedra = generate_perlin_noise(scale_piedra, width, height, seed_piedra, octaves_piedra, persistence_piedra, lacunarity_piedra)

# Mapear los colores de tierra y piedra
texture_tierra = map_colors_tierra(layer_tierra)
texture_piedra = map_colors_piedra(layer_piedra)

# Crear una máscara de gradiente horizontal
gradient = np.linspace(0, 1, width)

# Expandir la máscara de gradiente para que se aplique a toda la altura de la imagen
mask = np.tile(gradient, (height, 1))

# Añadir una nueva dimensión a la máscara para que coincida con las dimensiones de las texturas
mask = mask[:, :, np.newaxis]

# Mezclar las dos texturas usando la máscara
combined_texture = texture_tierra * (1 - mask) + texture_piedra * mask

# Mostrar la textura combinada
plt.imshow(combined_texture)
plt.axis('off')
plt.show()
