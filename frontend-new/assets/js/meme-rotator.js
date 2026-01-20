/**
 * Weekly Meme Rotator for New Mexico Socialists
 * Automatically rotates featured meme each week
 */

class MemeRotator {
    constructor() {
        this.totalMemes = 19; // Update this if you add more memes
        this.storageKey = 'nms-featured-meme';
        this.weekKey = 'nms-current-week';
        this.init();
    }

    init() {
        const currentWeek = this.getCurrentWeek();
        const storedWeek = localStorage.getItem(this.weekKey);

        // If it's a new week, rotate the meme
        if (storedWeek !== currentWeek) {
            this.rotateFeaturedMeme();
            localStorage.setItem(this.weekKey, currentWeek);
        }

        // Display the featured meme
        this.displayFeaturedMeme();
    }

    // Get the current week number of the year
    getCurrentWeek() {
        const now = new Date();
        const start = new Date(now.getFullYear(), 0, 1);
        const diff = now - start;
        const oneWeek = 1000 * 60 * 60 * 24 * 7;
        return Math.floor(diff / oneWeek);
    }

    // Rotate to next featured meme
    rotateFeaturedMeme() {
        let currentFeatured = parseInt(localStorage.getItem(this.storageKey)) || 1;

        // Move to next meme (cycle back to 1 after reaching total)
        currentFeatured = (currentFeatured % this.totalMemes) + 1;

        localStorage.setItem(this.storageKey, currentFeatured);
        console.log(`🔄 Rotated to Meme ${currentFeatured}`);
    }

    // Get current featured meme number
    getFeaturedMeme() {
        return parseInt(localStorage.getItem(this.storageKey)) || 1;
    }

    // Display the featured meme
    displayFeaturedMeme() {
        const memeNum = this.getFeaturedMeme();
        const featuredContainer = document.getElementById('featured-meme');

        if (featuredContainer) {
            const imgSrc = `assets/img/meme_${memeNum}.png`;

            featuredContainer.innerHTML = `
        <div class="featured-meme-wrapper">
          <div class="featured-badge">
            <span class="badge-text">✨ Meme of the Week</span>
          </div>
          <img 
            src="${imgSrc}" 
            alt="Featured Meme ${memeNum}" 
            class="featured-meme-img"
            loading="eager"
          />
          <div class="featured-actions">
            <a href="${imgSrc}" download class="btn primary">
              📥 Download
            </a>
            <button type="button" class="btn secondary js-share-meme" data-img="${imgSrc}">
              🔗 Share
            </button>
            <a href="#memes" class="btn tertiary">
              🖼️ View Gallery
            </a>
          </div>
          <p class="featured-note">
            Featured meme changes every Monday! Check back weekly for new content.
          </p>
        </div>
      `;

            // Add share functionality
            const shareBtn = featuredContainer.querySelector('.js-share-meme');
            if (shareBtn) {
                shareBtn.addEventListener('click', () => this.shareMeme(imgSrc));
            }
        }
    }

    // Share meme functionality
    async shareMeme(imgSrc) {
        const url = window.location.origin + '/' + imgSrc;

        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'New Mexico Socialists Meme',
                    text: 'Check out this meme from New Mexico Socialists!',
                    url: url
                });
            } catch (err) {
                this.copyToClipboard(url);
            }
        } else {
            this.copyToClipboard(url);
        }
    }

    // Copy URL to clipboard
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            alert('✅ Link copied to clipboard!');
        }).catch(() => {
            prompt('Copy this link:', text);
        });
    }

    // Admin function: manually set featured meme (call from console)
    setFeaturedMeme(memeNum) {
        if (memeNum >= 1 && memeNum <= this.totalMemes) {
            localStorage.setItem(this.storageKey, memeNum);
            this.displayFeaturedMeme();
            console.log(`✅ Featured meme set to Meme ${memeNum}`);
        } else {
            console.error(`❌ Invalid meme number. Must be between 1 and ${this.totalMemes}`);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.memeRotator = new MemeRotator();
});

// Make it accessible from console for manual control
// Usage: memeRotator.setFeaturedMeme(5)
