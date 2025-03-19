const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

async function scrapeTraderie(pageNumber) {
    const url = `https://traderie.com/api/royalehigh/items?variants=&tags=true&page=${pageNumber}`;

    try {
        const browser = await puppeteer.launch({
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();

        await page.goto(url, { waitUntil: 'domcontentloaded' });

        const data = await page.evaluate(() => {
            return JSON.parse(document.querySelector('pre').innerText);
        });

        await browser.close();

        if (!data) {
            throw new Error('No data found');
        }

        return data;

    } catch (error) {
        console.error(`❌ Error fetching data from API (page ${pageNumber}):`, error);
        return [];
    }
}

(async () => {
    const pageNumber = parseInt(process.argv[2], 10) || 0;

    try {
        const scrapedData = await scrapeTraderie(pageNumber);
        console.log(JSON.stringify(scrapedData));
    } catch (error) {
        console.error(JSON.stringify({ error: "Fetching failed", details: error.toString() }));
        process.exit(1);
    }
})();
