// script.js

document.addEventListener('DOMContentLoaded', function () {
  const modal = document.createElement('div');
  modal.id = 'img-modal';
  modal.style.display = 'none';
  modal.innerHTML = '<span id="close-modal">&times;</span><img id="modal-img" src="" alt="">';
  document.body.appendChild(modal);

  const modalImg = document.getElementById('modal-img');
  const closeModal = document.getElementById('close-modal');

  document.body.addEventListener('click', function (e) {
    if (e.target.classList.contains('gallery-img')) {
      modal.style.display = 'flex';
      modalImg.src = e.target.src;
    } else if (e.target === modal || e.target === closeModal) {
      modal.style.display = 'none';
      modalImg.src = '';
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      modal.style.display = 'none';
      modalImg.src = '';
    }
  });
}); 