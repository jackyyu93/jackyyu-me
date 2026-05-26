const sharp = require('sharp');
const fs = require('fs');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="#0c0a09"/>
  <text x="32" y="44" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="34" fill="#fbbf24" text-anchor="middle" font-style="italic">JY</text>
</svg>`;

fs.writeFileSync('public/favicon.svg', svg);
console.log('Wrote public/favicon.svg');

(async () => {
  await sharp(Buffer.from(svg)).resize(180, 180).png().toFile('public/apple-touch-icon.png');
  console.log('Wrote public/apple-touch-icon.png');

  await sharp(Buffer.from(svg)).resize(32, 32).png().toFile('public/favicon.ico');
  console.log('Wrote public/favicon.ico');
})();
