// Configuration
const TOTAL_MEMES = 19;
const MEME_BASE_PATH = 'assets/img/webp/meme_';
const MEME_FALLBACK_PATH = 'assets/img/meme_';

// Get week number of the year
function getWeekNumber(date = new Date()) {
  const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
  const pastDaysOfYear = (date - firstDayOfYear) / 86400000;
  return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
}

// Get current week's featured meme (rotates weekly)
function getFeaturedMemeNumber() {
  const weekNum = getWeekNumber();
  // Rotate through memes based on week number
  return ((weekNum - 1) % TOTAL_MEMES) + 1;
}

// Format date for display
function getWeekDateRange() {
  const today = new Date();
  const dayOfWeek = today.getDay();
  const monday = new Date(today);
  monday.setDate(today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1));
  
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  
  const options = { month: 'short', day: 'numeric' };
  return `${monday.toLocaleDateString('en-US', options)} - ${sunday.toLocaleDateString('en-US', options)}, ${today.getFullYear()}`;
}

// Create picture element with WebP and fallback
function createMemeElement(memeNum, isLazy = true) {
  const picture = document.createElement('picture');
  
  const source = document.createElement('source');
  source.type = 'image/webp';
  source.srcset = `${MEME_BASE_PATH}${memeNum}.webp`;
  
  const img = document.createElement('img');
  img.src = `${MEME_FALLBACK_PATH}${memeNum}.png`;
  img.alt = `Socialist meme ${memeNum}`;
  img.width = 800;
  img.height = 600;
  if (isLazy) img.loading = 'lazy';
  
  picture.appendChild(source);
  picture.appendChild(img);
  
  return picture;
}

// Initialize featured meme of the week
function initFeaturedMeme() {
  const featuredNum = getFeaturedMemeNumber();
  const container = document.getElementById('meme-of-week');
  const weekDate = document.getElementById('week-date');
  
  if (container) {
    const memeElement = createMemeElement(featuredNum, false);
    memeElement.classList.add('meme-featured-img');
    container.appendChild(memeElement);
    
    // Add download button
    const downloadBtn = document.createElement('a');
    downloadBtn.href = `${MEME_BASE_PATH}${featuredNum}.webp`;
    downloadBtn.download = `nmsocialists-meme-week${getWeekNumber()}.webp`;
    downloadBtn.className = 'btn primary';
    downloadBtn.textContent = 'Download / Descargar';
    downloadBtn.style.marginTop = '1rem';
    downloadBtn.style.display = 'inline-block';
    container.appendChild(downloadBtn);
  }
  
  if (weekDate) {
    weekDate.textContent = getWeekDateRange();
  }
}

// Initialize meme gallery
function initMemeGallery() {
  const gallery = document.getElementById('meme-gallery');
  if (!gallery) return;
  
  const featuredNum = getFeaturedMemeNumber();
  
  // Create gallery items for all memes
  for (let i = 1; i <= TOTAL_MEMES; i++) {
    const item = document.createElement('div');
    item.className = 'meme-item';
    
    // Mark featured meme
    if (i === featuredNum) {
      const badge = document.createElement('span');
      badge.className = 'featured-badge';
      badge.textContent = '⭐ Featured This Week';
      item.appendChild(badge);
    }
    
    const memeElement = createMemeElement(i, true);
    item.appendChild(memeElement);
    
    // Add download link
    const downloadLink = document.createElement('a');
    downloadLink.href = `${MEME_BASE_PATH}${i}.webp`;
    downloadLink.download = `nmsocialists-meme-${i}.webp`;
    downloadLink.className = 'meme-download';
    downloadLink.textContent = '⬇ Download';
    item.appendChild(downloadLink);
    
    gallery.appendChild(item);
  }
}

// Share functions
function shareMeme(platform) {
  const featuredNum = getFeaturedMemeNumber();
  const url = encodeURIComponent(window.location.href);
  const text = encodeURIComponent('Check out this week\'s meme from New Mexico Socialists!');
  
  let shareUrl;
  switch(platform) {
    case 'twitter':
      shareUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
      break;
    case 'facebook':
      shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
      break;
    default:
      return;
  }
  
  window.open(shareUrl, '_blank', 'width=600,height=400');
}

function downloadMeme() {
  const featuredNum = getFeaturedMemeNumber();
  const link = document.createElement('a');
  link.href = `${MEME_BASE_PATH}${featuredNum}.webp`;
  link.download = `nmsocialists-meme-week${getWeekNumber()}.webp`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  initFeaturedMeme();
  initMemeGallery();
  
  console.log(`Week ${getWeekNumber()}: Featuring meme #${getFeaturedMemeNumber()}`);
});

// Make share functions globally available
window.shareMeme = shareMeme;
window.downloadMeme = downloadMeme;
