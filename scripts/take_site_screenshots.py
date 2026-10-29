import asyncio
import os
from playwright.async_api import async_playwright

async def take_screenshots():
    out_dir = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview"
    brain_dir = r"C:\Users\manpr\.gemini\antigravity\brain\7124d6d3-c54e-48d1-8f3e-ef74da11c511"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(brain_dir, exist_ok=True)

    async with async_playwright() as p:
        # Try system chrome or chromium
        try:
            browser = await p.chromium.launch(channel="chrome", headless=True)
        except Exception:
            browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        print("Navigating to http://localhost:3000...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # 1. Hero screenshot
        hero_path = os.path.join(out_dir, "live_site_hero.png")
        await page.screenshot(path=hero_path)
        print(f"Captured hero: {hero_path}")

        # 2. Scroll 25% (scrubbing animation)
        await page.evaluate("window.scrollTo(0, window.innerHeight * 1.5)")
        await page.wait_for_timeout(1000)
        scroll1_path = os.path.join(out_dir, "live_site_scroll_25.png")
        await page.screenshot(path=scroll1_path)
        print(f"Captured scroll 25%: {scroll1_path}")

        # 3. Scroll to Section 2 (Why 42 Kalidasa)
        await page.evaluate("document.getElementById('vision').scrollIntoView()")
        await page.wait_for_timeout(1000)
        sec2_path = os.path.join(out_dir, "live_site_section2_vision.png")
        await page.screenshot(path=sec2_path)
        print(f"Captured Section 2: {sec2_path}")

        # 4. Scroll to Section 3 (Discover the Vision)
        await page.evaluate("document.getElementById('amenities').scrollIntoView()")
        await page.wait_for_timeout(1000)
        sec3_path = os.path.join(out_dir, "live_site_section3_showcase.png")
        await page.screenshot(path=sec3_path)
        print(f"Captured Section 3: {sec3_path}")

        # 5. Scroll to Section 5 (Brand statement)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        sec5_path = os.path.join(out_dir, "live_site_section5_brand.png")
        await page.screenshot(path=sec5_path)
        print(f"Captured Section 5: {sec5_path}")

        await browser.close()

    # Copy to brain dir so antigravity read_file can view them
    import shutil
    for fname in ["live_site_hero.png", "live_site_scroll_25.png", "live_site_section2_vision.png", "live_site_section3_showcase.png", "live_site_section5_brand.png"]:
        src = os.path.join(out_dir, fname)
        dst = os.path.join(brain_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {fname} to brain directory.")

if __name__ == '__main__':
    asyncio.run(take_screenshots())
