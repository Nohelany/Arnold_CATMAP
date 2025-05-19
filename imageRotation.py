# Librerías
from PIL import Image
import numpy as np
# Carga la imagen y la convuierte a escala de grises y la redimensiona
imag=Image.open("imagenOriginal.JPG")
imag=imag.resize((255,255))
imagen = imag.convert("L")

arr = np.array(imagen)

Image.fromarray(arr).save("original.jpg")
# Hacer la imegen de 255 x 255
TAM = 255
arr = arr[:TAM, :TAM]
#Imagen con correlación menor
min_correlacion=101.0
min_img= None

# Generar 3 versiones con 1, 5 y 10 iteraciones
for n in [1, 5, 10]:
    transform = arr.copy()

    # Aplica n veces el Arnold Cat Map
    for _ in range(n):
        nueva = np.zeros_like(transform)
        for y in range(TAM):              
            for x in range(TAM):        
                px = (x + y) % TAM
                py = (x + 2*y) % TAM
                nueva[py][px] = transform[y][x]
        transform = nueva

    # Guarda la versión transformada
    fname = f"transform_{n}iter.jpg"
    Image.fromarray(transform).save(fname)

    # Calcula % de píxeles idénticos respecto al original
    iguales = np.sum(transform == arr)
    porcent = iguales * 100.0 / transform.size
    print(f"{n} iter → {porcent:.2f}% píxeles idénticos")

    #Version con menor correlacion
    if porcent <min_correlacion:
        min_correlacion=porcent
        min_img=transform.copy()

#Guarda imagen con menor correlacion
Image.fromarray(min_img).save("menor_correlacion.jpg")
print(f"Imagen con menor correlacion = {min_correlacion:.2f}% pixeles identicos")
# Busca cuántas iteraciones hacen falta para recuperar la original
current = arr.copy()
count = 0
MAX_ITERACIONES = 1000
while True:
    count += 1
    nueva = np.zeros_like(current)
    for y in range(TAM):
        for x in range(TAM):
            px = (x + y) % TAM
            py = (x + 2*y) % TAM
            nueva[py][px] = current[y][x]
    current = nueva

    # Cuando vuelve a coincidir completamente, guardamos y rompemos
    if (current == arr).all():
        Image.fromarray(current).save("recuperada.jpg")
        print(f"Recuperada en {count} iteraciones")
        break
    if count >= MAX_ITERACIONES:
        print(f"No recuperó en {MAX_ITERACIONES} iteraciones, abortando.")
        break