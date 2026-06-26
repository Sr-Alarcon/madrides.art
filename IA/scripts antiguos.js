var imageNames = [];

function addImages() {
  var files = document.getElementById('image-input').files;

  for (var i = 0; i < files.length; i++) {
    let file = files[i];
    imageNames.push({ name: file.name });
    displayImageNames();
  }
}

function displayImageNames() {
  var container = document.getElementById('image-names');
  container.innerHTML = imageNames.map(function (image, index) {
    return '<div><input type="checkbox" class="image-checkbox" data-index="' + index + '"> ' + image.name + '</div>';
  }).join('');
}

function filterImages() {
  var searchValue = document.getElementById('search-input').value.toLowerCase();
  var container = document.getElementById('image-names');
  var children = container.children;
  var filteredNames = [];

  for (var i = 0; i < children.length; i++) {
    var child = children[i];
    var name = child.textContent.trim();

    if (searchValue === '' || name.toLowerCase().includes(searchValue)) {
      filteredNames.push(name);
    }
  }

  container.innerHTML = '';

  if (searchValue === '') {
    for (var i = 0; i < imageNames.length; i++) {
      var imageName = imageNames[i].name;
      container.innerHTML += '<div><input type="checkbox" class="image-checkbox" data-index="' + i + '"> ' + imageName + '</div>';
    }
  } else {
    for (var i = 0; i < imageNames.length; i++) {
      var imageName = imageNames[i].name;

      if (filteredNames.includes(imageName)) {
        container.innerHTML += '<div><input type="checkbox" class="image-checkbox" data-index="' + i + '"> ' + imageName + '</div>';
      }
    }
  }
}

function removeSelectedImages() {
  var checkboxes = document.querySelectorAll('.image-checkbox');
  var indicesToRemove = Array.from(checkboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => parseInt(checkbox.getAttribute('data-index'), 10));

  indicesToRemove.sort((a, b) => b - a);

  for (var index of indicesToRemove) {
    imageNames.splice(index, 1);
  }

  displayImageNames();
}
