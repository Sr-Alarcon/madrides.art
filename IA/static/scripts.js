function updateImageList() {
  const input = document.getElementById('image-input');
  const imageNamesDiv = document.getElementById('image-names');
  imageNamesDiv.innerHTML = ''; // Limpiar la lista actual

  Array.from(input.files).forEach((file, index) => {
      const fileRowDiv = document.createElement('div');
      fileRowDiv.innerHTML = `<input type="checkbox" class="image-checkbox" data-index="${index}"> ${file.name}`;
      imageNamesDiv.appendChild(fileRowDiv);
  });
}

function filterImages() {
  const searchInput = document.getElementById('search-input').value.toLowerCase();
  const images = document.getElementById('image-names').querySelectorAll('div');

  Array.from(images).forEach((imgDiv) => {
      const imgName = imgDiv.textContent.toLowerCase();
      if (imgName.includes(searchInput)) {
          imgDiv.style.display = '';
      } else {
          imgDiv.style.display = 'none';
      }
  });
}

function removeSelectedImages() {
  const checkboxes = document.querySelectorAll('.image-checkbox:checked');
  const input = document.getElementById('image-input');
  
  // Crear una nueva lista de archivos excluyendo los seleccionados
  let newFileList = new DataTransfer();
  
  Array.from(input.files).forEach((file, index) => {
      if (!Array.from(checkboxes).find(checkbox => parseInt(checkbox.getAttribute('data-index'), 10) === index)) {
          newFileList.items.add(file);
      }
  });
  
  // Establecer la nueva lista de archivos al input
  input.files = newFileList.files;
  
  // Actualizar la lista de nombres de archivos mostrada
  updateImageList();
}

function uploadFilesAndShowMatches(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    const contentGrid = document.getElementById('content-grid');
    contentGrid.innerHTML = ''; // Limpiar el grid antes de añadir nuevos elementos

    // Mostrar las imágenes resultantes si las hay
    if (data.imagenes_resultantes && data.imagenes_resultantes.length > 0) {
      data.imagenes_resultantes.forEach(imgSrc => {
        const imgElement = document.createElement('img');
        imgElement.src = imgSrc;
        imgElement.className = 'grid-item';
        contentGrid.appendChild(imgElement);
      });
    } else {
      contentGrid.innerHTML = 'No se encontraron coincidencias.';
    }
  })
  .catch(error => {
    console.error('Error:', error);
    const contentGrid = document.getElementById('content-grid');
    contentGrid.innerHTML = 'Hubo un error al procesar las imágenes.';
  });
}

// Vincular la función al evento de submit del formulario
document.querySelector('form').addEventListener('submit', uploadFilesAndShowMatches);