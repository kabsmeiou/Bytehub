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

function toggle(postid) {
  var elt = document.getElementById('dropmenu-'+postid);
  elt.style.display = elt.style.display == 'block' ? 'none' : 'block';
}

function profile() {
    var elt = document.getElementById('profile-dropdown');
    elt.style.display = elt.style.display == 'block' ? 'none' : 'block';
}

function goBack() {
    window.history.back();
}

function handleBookmark(event) {
        event.preventDefault();
        const formData = new FormData(event.target);

        fetch(event.target.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        return false;
}