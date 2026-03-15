const fs = require("fs");
const path = require("path");
const sharp = require("sharp");
const readline = require("readline");

const inputDir = path.join(__dirname, "assets_raw");
const outputDir = path.join(__dirname, "assets_web");

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const validExt = [".png", ".jpg", ".jpeg", ".webp"];

// Función auxiliar para hacer preguntas en la consola de forma asíncrona
const askQuestion = (rl, query) => new Promise(resolve => rl.question(query, resolve));

async function processImage(file, config) {
  const ext = path.extname(file).toLowerCase();
  if (!validExt.includes(ext)) return;

  const inputPath = path.join(inputDir, file);
  const baseName = path.parse(file).name;

  const avifPath = path.join(outputDir, `${baseName}.avif`);
  const webpPath = path.join(outputDir, `${baseName}.webp`);

  try {
    const image = sharp(inputPath);
    const metadata = await image.metadata();

    // -- GENERACIÓN DEL AVIF (Opcional) --
    if (!config.onlyWebp) {
      const resizeWidthAvif = metadata.width && metadata.width > 1400 ? 1400 : metadata.width;
      
      await sharp(inputPath)
        .resize({ width: resizeWidthAvif, withoutEnlargement: true })
        .avif({ quality: 42, effort: 4 })
        .toFile(avifPath);
    }

    // -- GENERACIÓN DEL WEBP (Basado en la opción elegida) --
    let webpResizeOptions = {};
    const baseWidth = metadata.width && metadata.width > 1400 ? 1400 : metadata.width;

    if (config.mode === 'normal') {
      webpResizeOptions = { width: baseWidth, withoutEnlargement: true };
    } 
    else if (config.mode === 'exact') {
      // fit: 'cover' recorta la imagen al centro para encajar en el cuadrado exacto
      webpResizeOptions = { width: config.size, height: config.size, fit: 'cover' };
    } 
    else if (config.mode === 'divide') {
      webpResizeOptions = { width: Math.round(metadata.width / config.divisor) };
    }

    await sharp(inputPath)
      .resize(webpResizeOptions)
      .webp({ quality: 72, effort: 6 })
      .toFile(webpPath);

    console.log(`✅ Procesada: ${file}`);
  } catch (err) {
    console.error(`❌ Error con ${file}:`, err.message);
  }
}

async function main() {
  if (!fs.existsSync(inputDir)) {
    console.error("❌ No existe la carpeta assets_raw");
    process.exit(1);
  }

  const files = fs.readdirSync(inputDir);

  if (!files.length) {
    console.log("⚠️ No hay imágenes en assets_raw");
    return;
  }

  // Configuración del menú interactivo
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  let config = { mode: 'normal', onlyWebp: false };

  console.log("\n--- CONFIGURACIÓN DE FORMATOS ---");
  const formatChoice = await askQuestion(rl, "¿Qué quieres generar?\n1. AVIF y WEBP (Normal)\n2. SOLO WEBP (Más rápido)\n👉 Elige una opción (1 o 2): ");
  
  if (formatChoice === '2') {
    config.onlyWebp = true;
  }

  console.log("\n--- CONFIGURACIÓN DE WEBP ---");
  console.log("1. Normal (Ancho máximo de 1400px)");
  console.log("2. Tamaño miniatura/exacto (ej. recortar a 56x56)");
  console.log("3. Dividir resolución (ej. dividir el tamaño original por X)\n");

  const choice = await askQuestion(rl, "👉 Elige qué hacer con el WebP (1, 2 o 3): ");

  if (choice === '2') {
    const sizeInput = await askQuestion(rl, "Introduce el tamaño en píxeles (pulsa Enter para 56): ");
    config.mode = 'exact';
    config.size = parseInt(sizeInput) || 56;
  } 
  else if (choice === '3') {
    const divInput = await askQuestion(rl, "Introduce por cuánto quieres dividir (ej. 2, 4, 10): ");
    const divisor = parseFloat(divInput) || 2;
    config.mode = 'divide';
    config.divisor = divisor > 0 ? divisor : 1;
  } 
  else if (choice !== '1') {
    console.log("Opción no válida. Usando configuración normal (1) por defecto.");
  }

  rl.close();
  console.log("\n🚀 Empezando la conversión...\n");

  for (const file of files) {
    await processImage(file, config);
  }

  console.log("\n🎉 Conversión terminada");
}

main();