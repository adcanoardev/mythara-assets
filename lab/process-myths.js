const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const inputDir = "./sprites_raw";
const outputDir = "./sprites_web";

if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir);

async function processImage(file) {
  const inputPath = path.join(inputDir, file);
  const name = path.parse(file).name;

  const img = sharp(inputPath);
  const meta = await img.metadata();

  const width = meta.width;
  const height = meta.height;

  const sliceWidth = Math.floor(width / 3);

  const parts = [
    { name: "portrait", left: 0 },
    { name: "front", left: sliceWidth },
    { name: "back", left: sliceWidth * 2 }
  ];

  for (const part of parts) {
    const output = `${outputDir}/${name}_${part.name}.png`;

    await sharp(inputPath)
      .extract({
        left: part.left,
        top: 0,
        width: sliceWidth,
        height: height
      })
      .trim() // elimina bordes transparentes
      .png({ compressionLevel: 9 })
      .toFile(output);

    console.log("✔ creado", output);
  }
}

async function run() {
  const files = fs.readdirSync(inputDir);

  for (const file of files) {
    if (file.endsWith(".png")) {
      await processImage(file);
    }
  }

  console.log("✨ Todo terminado");
}

run();