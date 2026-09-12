const { chromium } = require('playwright');
const fs = require('fs');

async function renderHtmlToPng(htmlPath, pngPath, width = 1400, height = 950) {
    const browser = await chromium.launch();
    const page = await browser.newPage({
        viewport: { width, height },
        deviceScaleFactor: 2 // Crisp retina 2x output (>2400px width)
    });
    
    const htmlContent = fs.readFileSync(htmlPath, 'utf-8');
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    await page.screenshot({ path: pngPath, fullPage: true });
    await browser.close();
    console.log(`Rendered ${pngPath} successfully (scale=2x).`);
}

module.exports = { renderHtmlToPng };
