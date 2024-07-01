import numpy as np
from noise import snoise2
import matplotlib.pyplot as plt
import random

# Funcion para generar ruido Fbm
def generate_fbm_noise(scale, width, height, seed, octaves, persistence, lacunarity):
    layer = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            amplitude = 1.0
            frequency = 1.0
            noise_value = 0.0
            for o in range(octaves):
                noise_value += amplitude * snoise2(x / (scale / frequency),
                                                   y / (scale / frequency),
                                                   repeatx=width,
                                                   repeaty=height,
                                                   base=seed)
                amplitude *= persistence
                frequency *= lacunarity
            layer[y, x] = noise_value
    layer = (layer - np.min(layer)) / (np.max(layer) - np.min(layer))  # Normalizar
    return layer

# dimensiones de las texturas
width = 512
height = 512

def map_colors_tierra(layer):
    return np.stack((
        np.interp(layer, (0, 1), (139/255, 205/255)),  # Red
        np.interp(layer, (0, 1), (69/255, 133/255)),   # Green
        np.interp(layer, (0, 1), (19/255, 56/255))     # Blue
    ), axis=-1)

# Parámetros para la textura de tierra
scale_tierra = 50.0

seed_tierra = random.randint(0,100)
octaves_tierra = 4
persistence_tierra = 0.8
lacunarity_tierra = 2.0

fbm_noise_tierra = generate_fbm_noise(scale_tierra, width, height, seed_tierra, octaves_tierra, persistence_tierra, lacunarity_tierra)
texture_tierra = map_colors_tierra(fbm_noise_tierra)

plt.imshow(texture_tierra)
plt.title(f'Textura de Tierra fBM, semilla: {seed_tierra}, 512 x 512')
plt.show()

def map_colors_pasto(layer):
    return np.stack((
        np.interp(layer, (0, 1), (34/255, 85/255)),   # Red
        np.interp(layer, (0, 1), (139/255, 180/255)), # Green
        np.interp(layer, (0, 1), (34/255, 85/255))    # Blue
    ), axis=-1)

# Parámetros para la textura de pasto
scale_pasto = 50.0
octaves_pasto = 4
persistence_pasto = 0.8
lacunarity_pasto = 2.0
seed_pasto = random.randint(0,100)

fbm_noise_pasto = generate_fbm_noise(scale_pasto, width, height, seed_pasto, octaves_pasto, persistence_pasto, lacunarity_pasto)
texture_pasto = map_colors_pasto(fbm_noise_pasto)

plt.imshow(texture_pasto)
plt.title(f'Textura de Pasto fBM, semilla: {seed_pasto}, 512 x 512 ')
plt.show()

# Crear una máscara de gradiente horizontal
gradient = np.linspace(0, 1, width)

# Expandir la máscara de gradiente para que se aplique a toda la altura de la imagen
mask = np.tile(gradient, (height, 1))

# Añadir una nueva dimensión a la máscara para que coincida con las dimensiones de las texturas
mask = mask[:, :, np.newaxis]

# Mezclar las dos texturas usando la máscara
combined_texture = texture_tierra * (1 - mask) + texture_pasto * mask

# Mostrar la textura combinada
plt.imshow(combined_texture)
plt.title(f'Textura de tierra con pasto fBM, 512 x 512)')
plt.axis('off')
plt.show()

# Crear una máscara difuminada para la transición entre tierra y pasto
def create_blend_mask(width, height):
    mask = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            mask[y, x] = np.sin(np.pi * x / width) * np.sin(np.pi * y / height)
    return mask

blend_mask = create_blend_mask(width, height)

# Combinar las texturas utilizando la máscara
combined_texture = texture_pasto * (1 - blend_mask[:, :, np.newaxis]) + texture_tierra * blend_mask[:, :, np.newaxis]

plt.imshow(combined_texture)
plt.title('Textura difuminada de Tierra y Pasto fBM, 512 x 512')
plt.show()
