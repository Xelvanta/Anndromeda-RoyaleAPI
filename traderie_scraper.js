const puppeteer = require('puppeteer-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(stealthPlugin());

async function scrapeTraderie(page, pageNumber) {
    const url = `https://traderie.com/royalehigh/products?page=${pageNumber}`;

    try {
        console.log(`🌐 Navigating to ${url}`);
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });

        // ** Wait for items to load **
        await page.waitForSelector('div.item-img-container', { timeout: 15000 });

        // ** Debugging: Check if elements exist **
        const elementsCount = await page.evaluate(() => document.querySelectorAll('div.item-img-container').length);
        console.log(`🔍 Found ${elementsCount} items on page ${pageNumber}`);

        // ** Extract items **
        const items = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('div.item-img-container')).map(itemElement => {
                let itemName = 'Unknown';
                try {
                    itemName = itemElement.querySelector('div.sc-bkEOxz.fSHNlx')?.innerText || 'Unknown';
                } catch {}

                let itemValue = '0';
                try {
                    const valueElement = itemElement.querySelector('div.item-currencies > div.listing-bells');
                    itemValue = valueElement ? valueElement.innerText : '0';
                } catch {}

                return { name: itemName, value: itemValue };
            });
        });

        return items;

    } catch (error) {
        console.error(`❌ Error scraping page ${pageNumber}:`, error);
        return [];
    }
}

(async () => {
    const pageNumber = parseInt(process.argv[2], 10) || 0;
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // ** Reduce bot detection **
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
        await page.setViewport({ width: 1280, height: 800 });

        await page.evaluateOnNewDocument(() => {
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
        });

        const scrapedData = await scrapeTraderie(page, pageNumber);
        console.log(JSON.stringify(scrapedData));

    } catch (error) {
        console.error("❌ Scraping failed:", error);
        process.exit(1);
    } finally {
        console.log("✅ Finished Scraping");
        await browser.close();
    }
})();
