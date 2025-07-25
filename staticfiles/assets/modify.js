const fs = require('fs');
const path = require('path');

const folderPath = path.resolve('./js');
fs.readdir(folderPath, (err, files) => {
  if (err) {
    console.error('Folder oxunmadı:', err);
    return;
  }

  files.forEach((file) => {
    if (path.extname(file) === '.js' && !file.endsWith('.min.js')) {
      const sourcePath = path.join(folderPath, file);
      const destPath = path.join(folderPath, file.replace('.js', '.min.js'));

      fs.readFile(sourcePath, 'utf8', (err, data) => {
        if (err) {
          console.error(`Fayl oxunmadı: ${file}`, err);
          return;
        }

        // Sadə minify: boşluqları və sətir sonlarını silir
        const minifiedData = data.replace(/\s+/g, ' ').trim();

        fs.writeFile(destPath, minifiedData, 'utf8', (err) => {
          if (err) {
            console.error(`Fayl yazılmadı: ${destPath}`, err);
            return;
          }
          console.log(`${file} faylından ${path.basename(destPath)} yaradıldı.`);
        });
      });
    }
  });
});
