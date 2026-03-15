from PIL import Image
import os

# Configuración
carpeta_base = './myths'

# Recorremos del 1 al 50
for i in range(1, 2):
    # Generamos el formato con ceros (001, 002, 003...)
    numero_formateado = f"{i:03d}"
    
    # Busca la carpeta "001", "002"...
    carpeta_myth = os.path.join(carpeta_base, numero_formateado)
    
    # Genera el nombre exacto de la imagen: "001.png", "002.png"...
    nombre_imagen = f"{numero_formateado}.png"
    ruta_imagen = os.path.join(carpeta_myth, nombre_imagen) 
    
    if os.path.exists(ruta_imagen):
        try:
            # Abrir imagen conservando el canal Alpha (transparencia)
            img = Image.open(ruta_imagen).convert("RGBA")
            ancho, alto = img.size
            
            # Calculamos el ancho de cada una de las 3 partes
            tercio = ancho // 3
            
            # Cortar la imagen (Izquierda, Arriba, Derecha, Abajo)
            portrait = img.crop((0, 0, tercio, alto))
            front = img.crop((tercio, 0, tercio * 2, alto))
            back = img.crop((tercio * 2, 0, ancho, alto))
            
            # Guardar optimizado reduciendo drásticamente el peso
            portrait.quantize().save(os.path.join(carpeta_myth, 'portrait.png'), 'PNG', optimize=True)
            front.quantize().save(os.path.join(carpeta_myth, 'front.png'), 'PNG', optimize=True)
            back.quantize().save(os.path.join(carpeta_myth, 'back.png'), 'PNG', optimize=True)
            
            print(f"✅ Myth {numero_formateado} procesado: divido en portrait, front y back.")
        except Exception as e:
            print(f"❌ Error procesando Myth {numero_formateado}: {e}")
    else:
        print(f"⚠️ No se encontró la imagen en {ruta_imagen}")