function openPopup() {
    var popupContainer = document.getElementById('post-popup-page');
    var popupContent = document.getElementById('popup-content');
    var dimmerOverlay = document.getElementById('bg-dim');

    // load content of post.html into popupContent
    fetch('/Bytehub/post/')
        .then(response => response.text())
        .then(html => {
            popupContent.innerHTML = html;
            popupContainer.style.display = 'block'; // display the popup
            dimmerOverlay.style.display = 'block';
            ClassicEditor
                .create(document.querySelector('#popup-content #post-editor'))
        });
}
function closePopup() {
    var popupContainer = document.getElementById('post-popup-page');
    var dimmerOverlay = document.getElementById('bg-dim');
    popupContainer.style.display = 'none';
    dimmerOverlay.style.display = 'none';
}

function toggle() {
  var elt = document.getElementById('dropmenu');
  elt.style.display = elt.style.display == 'block' ? 'none' : 'block';
}