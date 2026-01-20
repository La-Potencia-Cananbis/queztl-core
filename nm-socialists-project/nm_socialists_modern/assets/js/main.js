
// main.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("join-form");
  const statusEl = document.getElementById("join-status");
  const fbShareLink = document.getElementById("fb-share-link");

  // Build Facebook share link for the whole site
  if (fbShareLink) {
    const siteUrl = window.location.href.split('#')[0];
    const shareUrl = new URL("https://www.facebook.com/sharer/sharer.php");
    shareUrl.searchParams.set("u", siteUrl);
    fbShareLink.href = shareUrl.toString();
  }

  // Helper for Netlify AJAX submissions
  function encode(data) {
    return Object.keys(data)
      .map(
        (key) =>
          encodeURIComponent(key) + "=" + encodeURIComponent(data[key])
      )
      .join("&");
  }

  if (form && statusEl) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      statusEl.textContent = "Sending / Enviando...";
      statusEl.style.color = "#f6c745";

      const formData = new FormData(form);
      const payload = {};
      formData.forEach((value, key) => {
        payload[key] = value;
      });

      // Add the Netlify form-name explicitly
      payload["form-name"] = form.getAttribute("name");

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: encode(payload),
      })
        .then(() => {
          statusEl.textContent =
            "Thanks for signing up! ¡Gracias por unirte!";
          statusEl.style.color = "#77e89f";
          form.reset();
        })
        .catch((error) => {
          console.error("Form submission error:", error);
          statusEl.textContent =
            "Error sending form. Please try again / Por favor intenta de nuevo.";
          statusEl.style.color = "#ffb3b3";
        });
    });
  }

  // Meme modal + per-meme share/download
  const modal = document.getElementById("meme-modal");
  const modalImg = document.getElementById("meme-modal-img");
  const modalDownload = document.getElementById("meme-download");
  const modalShare = document.getElementById("meme-share");
  const modalCopy = document.getElementById("meme-copy-link");
  const modalCopyStatus = document.getElementById("meme-copy-status");
  const modalClose = document.querySelector(".meme-modal-close");
  const modalBackdrop = document.querySelector(".meme-modal-backdrop");

  function getAbsoluteUrl(relativePath) {
    const loc = window.location;
    const basePath = loc.pathname.replace(/index\.html$/, "");
    return loc.origin + basePath + relativePath;
  }

  function openMemeModal(imgPath) {
    const absolute = getAbsoluteUrl(imgPath);
    modalImg.src = imgPath;
    modalDownload.href = imgPath;
    modalShare.dataset.shareUrl = absolute;
    modalCopy.dataset.copyUrl = absolute;
    modalCopyStatus.textContent = "";
    modal.classList.add("active");
    modal.setAttribute("aria-hidden", "false");
  }

  function closeMemeModal() {
    modal.classList.remove("active");
    modal.setAttribute("aria-hidden", "true");
    modalImg.src = "";
  }

  document.querySelectorAll(".js-view-meme").forEach((btn) => {
    btn.addEventListener("click", () => {
      const imgPath = btn.getAttribute("data-img");
      openMemeModal(imgPath);
    });
  });

  document.querySelectorAll(".js-share-meme").forEach((btn) => {
    btn.addEventListener("click", () => {
      const imgPath = btn.getAttribute("data-img");
      const absolute = getAbsoluteUrl(imgPath);
      const shareUrl = new URL("https://www.facebook.com/sharer/sharer.php");
      shareUrl.searchParams.set("u", absolute);
      window.open(shareUrl.toString(), "_blank", "noopener");
    });
  });

  if (modalClose) {
    modalClose.addEventListener("click", closeMemeModal);
  }
  if (modalBackdrop) {
    modalBackdrop.addEventListener("click", closeMemeModal);
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) {
      closeMemeModal();
    }
  });

  if (modalShare) {
    modalShare.addEventListener("click", () => {
      const url = modalShare.dataset.shareUrl;
      if (!url) return;
      const shareUrl = new URL("https://www.facebook.com/sharer/sharer.php");
      shareUrl.searchParams.set("u", url);
      window.open(shareUrl.toString(), "_blank", "noopener");
    });
  }

  if (modalCopy) {
    modalCopy.addEventListener("click", async () => {
      const url = modalCopy.dataset.copyUrl;
      if (!url) return;
      try {
        await navigator.clipboard.writeText(url);
        modalCopyStatus.textContent = "Link copied! / ¡Enlace copiado!";
        modalCopyStatus.style.color = "#77e89f";
      } catch (err) {
        console.error("Clipboard error:", err);
        modalCopyStatus.textContent =
          "Couldn't copy link. / No se pudo copiar el enlace.";
        modalCopyStatus.style.color = "#ffb3b3";
      }
    });
  }

  // Also allow clicking the thumbnail image itself to open the modal
  document.querySelectorAll(".gallery-item img").forEach((img) => {
    img.addEventListener("click", () => {
      const src = img.getAttribute("src");
      openMemeModal(src);
    });
  });
});
