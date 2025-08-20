// script.js

document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('imageModal');
  const modalImage = document.getElementById('modalImage');
  const modalBackground = document.getElementById('modalBackground');
  const modalClose = document.getElementById('modalClose');
  const searchBar = document.querySelector('.search-bar');
  const galleryItems = document.querySelectorAll('.gallery-item');
  const header = document.querySelector('header');



  let lastScrollTop = 0;
  let scrollThreshold = 100;

  // Scroll handler for header visibility
  window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > scrollThreshold) {
      if (scrollTop > lastScrollTop) {
        // Scrolling down - hide header
        header.classList.add('scrolled');
      } else {
        // Scrolling up - show header
        header.classList.remove('scrolled');
      }
    } else {
      // Near top - always show header
      header.classList.remove('scrolled');
    }
    
    lastScrollTop = scrollTop;
  });

  // Modal functionality
  galleryItems.forEach(item => {
    item.addEventListener('click', function() {
      const img = this.querySelector('img');
      
      // Use full-size image for modal, thumbnail for grid
      const fullImageSrc = img.dataset.full || img.src;
      
      modalImage.src = fullImageSrc;
      modalImage.alt = img.alt;
      modalBackground.style.backgroundImage = `url(${fullImageSrc})`;
      
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  // Close modal
  modalClose.addEventListener('click', closeModal);
  modal.addEventListener('click', function(e) {
    if (e.target === modal || e.target === modalBackground) {
      closeModal();
    }
  });
  
  // Prevent modal content from capturing clicks
  const modalContent = document.querySelector('.modal-content');
  modalContent.addEventListener('click', function(e) {
    e.stopPropagation();
  });

  // Keyboard navigation
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });

  function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Search functionality
  searchBar.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    
    galleryItems.forEach(item => {
      const title = item.getAttribute('data-title').toLowerCase();
      const place = item.getAttribute('data-place').toLowerCase();
      const location = item.querySelector('.image-location').textContent.toLowerCase();
      
      const matches = title.includes(searchTerm) || 
                     place.includes(searchTerm) || 
                     location.includes(searchTerm);
      
      if (matches) {
        item.style.display = 'block';
        item.style.animation = 'fadeInUp 0.6s ease-out';
      } else {
        item.style.display = 'none';
      }
    });
  });

  // Helper function to get country from place
  function getCountry(place) {
    const countries = {
      'Paris': 'France',
      'London': 'UK',
      'Tokyo': 'Japan',
      'New York': 'USA',
      'Venice': 'Italy',
      'Barcelona': 'Spain'
    };
    return countries[place] || '';
  }

  // Image loading optimization
  const images = document.querySelectorAll('.gallery-item img');
  images.forEach(img => {
    img.classList.add('loading');
    
    img.addEventListener('load', function() {
      this.classList.remove('loading');
      this.classList.add('loaded');
    });
    
    img.addEventListener('error', function() {
      this.classList.remove('loading');
      console.error('Failed to load image:', this.src);
    });
  });

  // Smooth scroll animation for gallery items
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe gallery items for animation
  galleryItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(30px)';
    item.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(item);
  });

  // Add hover sound effect (optional)
  galleryItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
      // Add subtle hover effect
      this.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    item.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });


}); 