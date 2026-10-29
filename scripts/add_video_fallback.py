with open(r"c:\Users\manpr\Documents\42 Kalidasa\website\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update header actions to include video tour button
target_header = '<button class="btn-blueprint" id="btn-open-blueprint" aria-haspopup="dialog" aria-expanded="false">Architectural Sanctions</button>'
replacement_header = '''<button class="btn-blueprint" id="btn-open-video" aria-haspopup="dialog" aria-expanded="false">Play Cinematic Tour</button>
      <button class="btn-blueprint" id="btn-open-blueprint" aria-haspopup="dialog" aria-expanded="false">Architectural Sanctions</button>'''

if target_header in html and 'btn-open-video' not in html:
    html = html.replace(target_header, replacement_header, 1)

# 2. Add video modal markup right before blueprint-modal
video_modal_markup = '''  <!-- Cinematic Video Modal Fallback -->
  <div class="blueprint-modal" id="video-modal" role="dialog" aria-modal="true" aria-labelledby="video-modal-title">
    <div class="blueprint-card" style="max-width: 960px; padding: 24px;">
      <button class="blueprint-close" id="btn-close-video" aria-label="Close video player">&times;</button>
      <div class="card-meta">CINEMATIC PREVIEW &bull; 26.85S CAMERA JOURNEY</div>
      <h2 class="card-title" id="video-modal-title" style="margin-bottom: 16px;">Autonomous Orbital Flythrough</h2>
      <video id="tour-video" controls playsinline preload="metadata" style="width: 100%; border-radius: 8px; border: 1px solid var(--border-subtle); background: #000;">
        <source src="camera_path_preview.mp4" type="video/mp4">
        Your browser does not support HTML5 video playback.
      </video>
    </div>
  </div>

'''
if '<div class="blueprint-modal" id="blueprint-modal"' in html and 'id="video-modal"' not in html:
    html = html.replace('<div class="blueprint-modal" id="blueprint-modal"', video_modal_markup + '  <div class="blueprint-modal" id="blueprint-modal"', 1)

# 3. Add JS event listeners for video modal
target_script = '// Modal Events'
replacement_script = '''// Video Modal Events
    const videoModal = document.getElementById('video-modal');
    const openVideoBtn = document.getElementById('btn-open-video');
    const closeVideoBtn = document.getElementById('btn-close-video');
    const tourVideo = document.getElementById('tour-video');

    if (openVideoBtn && videoModal) {
      openVideoBtn.addEventListener('click', () => {
        videoModal.classList.add('open');
        openVideoBtn.setAttribute('aria-expanded', 'true');
        if (tourVideo) tourVideo.play();
      });
      closeVideoBtn.addEventListener('click', () => {
        videoModal.classList.remove('open');
        openVideoBtn.setAttribute('aria-expanded', 'false');
        if (tourVideo) tourVideo.pause();
      });
      videoModal.addEventListener('click', (e) => {
        if (e.target === videoModal) {
          videoModal.classList.remove('open');
          openVideoBtn.setAttribute('aria-expanded', 'false');
          if (tourVideo) tourVideo.pause();
        }
      });
    }

    // Modal Events'''

if target_script in html and 'const videoModal' not in html:
    html = html.replace(target_script, replacement_script, 1)

with open(r"c:\Users\manpr\Documents\42 Kalidasa\website\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated index.html with video modal fallback!")

