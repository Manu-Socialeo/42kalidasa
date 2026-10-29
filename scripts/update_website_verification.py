with open(r"c:\Users\manpr\Documents\42 Kalidasa\website\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update header actions to include Exterior Match Verification button
target_header = '<button class="btn-blueprint" id="btn-open-video" aria-haspopup="dialog" aria-expanded="false">Play Cinematic Tour</button>'
replacement_header = '''<button class="btn-blueprint" id="btn-open-verify" aria-haspopup="dialog" aria-expanded="false">Exterior Verification</button>
      <button class="btn-blueprint" id="btn-open-video" aria-haspopup="dialog" aria-expanded="false">Play Cinematic Tour</button>'''

if target_header in html and 'btn-open-verify' not in html:
    html = html.replace(target_header, replacement_header, 1)

# 2. Add verification modal markup
verify_modal_markup = '''  <!-- Exterior Verification Modal -->
  <div class="blueprint-modal" id="verify-modal" role="dialog" aria-modal="true" aria-labelledby="verify-modal-title">
    <div class="blueprint-card" style="max-width: 1100px; padding: 24px; max-height: 90vh; overflow-y: auto;">
      <button class="blueprint-close" id="btn-close-verify" aria-label="Close verification modal">&times;</button>
      <div class="card-meta">GROUND TRUTH VERIFICATION &bull; SITE PHOTOGRAPH VS 3D MASTER</div>
      <h2 class="card-title" id="verify-modal-title" style="margin-bottom: 8px;">Exterior Facade Photorealism Match</h2>
      <p class="card-desc" style="margin-bottom: 16px;">
        Certified side-by-side comparison between the client-approved building photograph (Site No. 42 Kalidasa Road) and the calibrated Cycles 3D architectural master.
      </p>
      <img src="exterior_comparison_side_by_side_v003.png" alt="Side-by-Side Architectural Comparison" style="width: 100%; height: auto; border-radius: 8px; border: 1px solid var(--border-subtle); display: block;">
    </div>
  </div>

'''

if '<div class="blueprint-modal" id="video-modal"' in html and 'id="verify-modal"' not in html:
    html = html.replace('<div class="blueprint-modal" id="video-modal"', verify_modal_markup + '  <div class="blueprint-modal" id="video-modal"', 1)

# 3. Add JS event listeners for verify modal
target_script = '// Video Modal Events'
replacement_script = '''// Verification Modal Events
    const verifyModal = document.getElementById('verify-modal');
    const openVerifyBtn = document.getElementById('btn-open-verify');
    const closeVerifyBtn = document.getElementById('btn-close-verify');

    if (openVerifyBtn && verifyModal) {
      openVerifyBtn.addEventListener('click', () => {
        verifyModal.classList.add('open');
        openVerifyBtn.setAttribute('aria-expanded', 'true');
      });
      closeVerifyBtn.addEventListener('click', () => {
        verifyModal.classList.remove('open');
        openVerifyBtn.setAttribute('aria-expanded', 'false');
      });
      verifyModal.addEventListener('click', (e) => {
        if (e.target === verifyModal) {
          verifyModal.classList.remove('open');
          openVerifyBtn.setAttribute('aria-expanded', 'false');
        }
      });
    }

    // Video Modal Events'''

if target_script in html and 'const verifyModal' not in html:
    html = html.replace(target_script, replacement_script, 1)

with open(r"c:\Users\manpr\Documents\42 Kalidasa\website\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated website/index.html with Exterior Verification dialog!")
