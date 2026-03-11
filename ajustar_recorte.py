from PIL import Image
import os

# ==========================================
# ⚙️ CONFIGURACIÓN DEL RECORTE MANUAL
# ==========================================

# 1. ¿Qué myth quedó mal cortado? (Pon el número aquí, ej: 11 para la carpeta 011)
numero_myth = 1

# 2. Ajuste de las líneas de corte vertical (IZQ/DER) en píxeles
# - Positivo mueve el corte hacia la DERECHA. Negativo hacia la IZQUIERDA.
mover_corte_1 = 0   # Ajusta la línea que separa el PORTRAIT del FRONT
mover_corte_2 = 0  # Ajusta la línea que separa el FRONT del BACK

# 3. Ajuste de los bordes horizontales (ARRIBA/ABAJO) en píxeles
# - Pon un número POSITIVO para "comer" espacio sobrante de la imagen.
recorte_arriba = 220  # Ej: 20 quitará 20 píxeles del techo transparente.
recorte_abajo = 290   # Ej: 30 quitará 30 píxeles del suelo transparente.

# ==========================================

carpeta_base = './myths'
numero_formateado = f"{numero_myth:03d}"
carpeta_myth = os.path.join(carpeta_base, numero_formateado)
ruta_imagen = os.path.join(carpeta_myth, f"{numero_formateado}.png")

if os.path.exists(ruta_imagen):
    try:
        img = Image.open(ruta_imagen).convert("RGBA")
        ancho, alto = img.size
        
        # Calculamos los cortes originales (matemáticamente exactos en anchura)
        tercio = ancho // 3
        
        # Aplicamos tus ajustes manuales X (Izquierda / Derecha)
        corte_1_real = tercio + mover_corte_1
        corte_2_real = (tercio * 2) + mover_corte_2
        
        # Aplicamos tus ajustes manuales Y (Arriba / Abajo)
        techo = recorte_arriba
        suelo = alto - recorte_abajo
        
        # Validamos para que no intente cortar fuera de la imagen o al revés
        corte_1_real = max(0, min(corte_1_real, ancho))
        corte_2_real = max(0, min(corte_2_real, ancho))
        techo = max(0, min(techo, alto - 1))
        suelo = max(techo + 1, min(suelo, alto))

        print(f"🖼️ Imagen original: {ancho}px ancho x {alto}px alto.")
        print(f"✂️ Cortes en X (ancho): {corte_1_real} y {corte_2_real}")
        print(f"✂️ Cortes en Y (alto): Techo en {techo}, Suelo en {suelo}")
        
        # Cortamos la imagen con las nuevas coordenadas
        # El orden es siempre: (Izquierda, Arriba, Derecha, Abajo)
        portrait = img.crop((0, techo, corte_1_real, suelo))
        front = img.crop((corte_1_real, techo, corte_2_real, suelo))
        back = img.crop((corte_2_real, techo, ancho, suelo))
        
        # Guardamos y optimizamos
        portrait.quantize().save(os.path.join(carpeta_myth, 'portrait.png'), 'PNG', optimize=True)
        front.quantize().save(os.path.join(carpeta_myth, 'front.png'), 'PNG', optimize=True)
        back.quantize().save(os.path.join(carpeta_myth, 'back.png'), 'PNG', optimize=True)
        
        print(f"✅ ¡Myth {numero_formateado} reajustado y guardado correctamente!")
        
    except Exception as e:
        print(f"❌ Error procesando Myth {numero_formateado}: {e}")
else:
    print(f"⚠️ No se encontró la imagen original en {ruta_imagen}")