import asyncio
import shutil
from playwright.async_api import async_playwright

async def snap():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chrome', headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto('http://localhost:3000', wait_until='networkidle')
        await page.evaluate("document.getElementById('amenities').scrollIntoView()")
        await page.wait_for_timeout(1500)
        await page.screenshot(path='renders/preview/live_site_section3_v006.png')
        await browser.close()
    shutil.copy2('renders/preview/live_site_section3_v006.png', r'C:\Users\manpr\.gemini\antigravity\brain\7124d6d3-c54e-48d1-8f3e-ef74da11c511\live_site_section3_v006.png')
    print('Captured live_site_section3_v006.png')

if __name__ == '__main__':
    asyncio.run(snap())
