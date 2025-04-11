// Функция для обработки лайков
function handleLike(postId) {
  fetch(`/like/${postId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      const likeBtn = document.querySelector(`#like-btn-${postId}`);
      const likeCount = document.querySelector(`#like-count-${postId}`);

      if (data.status === 'liked') {
        likeBtn.classList.add('active');
        likeCount.textContent = parseInt(likeCount.textContent) + 1;
      } else {
        likeBtn.classList.remove('active');
        likeCount.textContent = parseInt(likeCount.textContent) - 1;
      }
    });
}

// Функция для обработки избранного
function handleFavorite(postId) {
  fetch(`/favorite/${postId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      const favBtn = document.querySelector(`#fav-btn-${postId}`);

      if (data.status === 'added') {
        favBtn.classList.add('active');
        favBtn.innerHTML = '<i class="fas fa-star"></i>';
      } else {
        favBtn.classList.remove('active');
        favBtn.innerHTML = '<i class="far fa-star"></i>';
      }
    });
}

// Предварительный просмотр изображения
function previewImage(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function (e) {
      const preview = document.querySelector('#image-preview');
      preview.src = e.target.result;
      preview.style.display = 'block';
    }

    reader.readAsDataURL(input.files[0]);
  }
}

// Анимация появления элементов при прокрутке
function handleScrollAnimation() {
  const elements = document.querySelectorAll('.post-card, .note-card');

  elements.forEach(element => {
    const position = element.getBoundingClientRect();

    if (position.top < window.innerHeight - 100) {
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
    }
  });
}

// Обработка поиска
function handleSearch(event) {
  event.preventDefault();
  const query = document.querySelector('#search-query').value;
  const city = document.querySelector('#search-city').value;

  window.location.href = `/search?q=${encodeURIComponent(query)}&city=${encodeURIComponent(city)}`;
}

// Валидация форм
function validateForm(formId) {
  const form = document.querySelector(`#${formId}`);
  if (!form) return true;

  const inputs = form.querySelectorAll('input[required], textarea[required]');
  let isValid = true;

  inputs.forEach(input => {
    if (!input.value.trim()) {
      input.classList.add('is-invalid');
      isValid = false;
    } else {
      input.classList.remove('is-invalid');
    }
  });

  return isValid;
}

// Обработчики событий
document.addEventListener('DOMContentLoaded', function () {
  // Инициализация тултипов Bootstrap
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

  // Обработка прокрутки
  window.addEventListener('scroll', handleScrollAnimation);

  // Инициализация форм поиска
  const searchForm = document.querySelector('#search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', handleSearch);
  }

  // Обработка загрузки изображений
  const imageInput = document.querySelector('#image-input');
  if (imageInput) {
    imageInput.addEventListener('change', function () {
      previewImage(this);
    });
  }

  // Анимация появления алертов
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    alert.style.animation = 'fadeIn 0.5s ease-out';
    setTimeout(() => {
      alert.style.animation = 'fadeOut 0.5s ease-out';
      setTimeout(() => {
        alert.remove();
      }, 500);
    }, 3000);
  });
});

// Плавная прокрутка
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

function editNote(noteId) {
  const noteElement = document.getElementById(`note-${noteId}`);
  const titleElement = noteElement.querySelector('.note-title');
  const contentElement = noteElement.querySelector('.note-content');
  const editBtn = noteElement.querySelector('.edit-note');

  const title = titleElement.textContent;
  const content = contentElement.textContent;

  titleElement.innerHTML = `<input type="text" class="form-control" value="${title}">`;
  contentElement.innerHTML = `<textarea class="form-control">${content}</textarea>`;

  editBtn.textContent = 'Сохранить';
  editBtn.onclick = () => saveNote(noteId);
}

function saveNote(noteId) {
  const noteElement = document.getElementById(`note-${noteId}`);
  const title = noteElement.querySelector('input').value;
  const content = noteElement.querySelector('textarea').value;
  const editBtn = noteElement.querySelector('.edit-note');

  fetch(`/notes/${noteId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, content })
  })
    .then(response => response.json())
    .then(data => {
      const titleElement = noteElement.querySelector('.note-title');
      const contentElement = noteElement.querySelector('.note-content');

      titleElement.innerHTML = data.title;
      contentElement.innerHTML = data.content;

      editBtn.textContent = 'Редактировать';
      editBtn.onclick = () => editNote(noteId);
    });
}

function deleteNote(noteId) {
  if (confirm('Вы уверены, что хотите удалить эту заметку?')) {
    fetch(`/notes/${noteId}`, {
      method: 'DELETE'
    })
      .then(response => response.json())
      .then(data => {
        const noteElement = document.getElementById(`note-${noteId}`);
        noteElement.remove();
      });
  }
} 