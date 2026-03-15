from PIL import Image, ImageDraw
import os

# ==========================================
# ⚙️ CONFIGURACIÓN DEL PORTRAIT MANUAL
# ==========================================

# 1. ¿Qué myth vas a ajustar?
numero_myth = 1

# 2. Mueve el círculo de recorte (en píxeles)
mover_x = 0   # Positivo: mueve el círculo a la DERECHA | Negativo: IZQUIERDA
mover_y = 0   # Positivo: mueve el círculo hacia ABAJO  | Negativo: ARRIBA

# 3. Tamaño del círculo
# Por defecto se ajusta al ancho del primer tercio. 
# Si el círculo es muy grande, pon un número negativo (ej: -20). Si es pequeño, positivo (ej: 30).
ajuste_tamano = 0 

# ==========================================

carpeta_base = './myths'
numero_formateado = f"{numero_myth:03d}"
carpeta_myth = os.path.join(carpeta_base, numero_formateado)

# Leemos SIEMPRE la imagen original para no perder datos si te equivocas
ruta_imagen = os.path.join(carpeta_myth, f"{numero_formateado}.png")
ruta_guardado = os.path.join(carpeta_myth, 'portrait.png')

if os.path.exists(ruta_imagen):
    try:
        img = Image.open(ruta_imagen).convert("RGBA")
        ancho_total, alto = img.size
        
        # 1. Separamos el área del portrait (el primer tercio de la imagen)
        tercio = ancho_total // 3
        area_portrait = img.crop((0, 0, tercio, alto))
        
        # 2. Calculamos el tamaño final del círculo con tu ajuste
        lado = min(tercio, alto) + ajuste_tamano
        
        # 3. Calculamos dónde está el centro del círculo
        # Por defecto, centrado horizontalmente y pegado arriba
        centro_x = (tercio // 2) + mover_x
        centro_y = (lado // 2) + mover_y
        
        # 4. Sacamos las coordenadas del cuadrado a recortar
        izquierda = centro_x - (lado // 2)
        arriba = centro_y - (lado // 2)
        derecha = centro_x + (lado // 2)
        abajo = centro_y + (lado // 2)
        
        # Recortamos esa zona específica (Pillow maneja automáticamente si te sales de los bordes)
        recorte_cuadrado = area_portrait.crop((izquierda, arriba, derecha, abajo))
        
        # 5. Creamos la máscara redonda
        mascara = Image.new('L', (lado, lado), 0)
        dibujo = ImageDraw.Draw(mascara)
        dibujo.ellipse((0, 0, lado, lado), fill=255)
        
        # 6. Pegamos el recorte en un lienzo transparente usando la máscara
        resultado = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
        resultado.paste(recorte_cuadrado, (0, 0), mascara)
        
        # Guardamos el resultado sobrescribiendo solo el portrait.png
        resultado.save(ruta_guardado, 'PNG', optimize=True)
        
        print(f"✅ Portrait del Myth {numero_formateado} ajustado y guardado.")
        print(f"   -> Centro X: {centro_x}, Centro Y: {centro_y}, Tamaño: {lado}px")
        
    except Exception as e:
        print(f"❌ Error procesando el Myth {numero_formateado}: {e}")
else:
    print(f"⚠️ No se encontró la imagen original en {ruta_imagen}")