const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

/**
 * Fetches data from the Traderie API.
 * 
 * @async
 * @function scrapeTraderie
 * @param {number} pageNumber - The page number to fetch from the API.
 * @returns {Promise<Object[]>} A promise that resolves to an array of scraped data objects.
 * @throws {Error} If Puppeteer fails to launch.
 * @throws {Error} If navigation to the URL fails.
 * @throws {TypeError} If the expected <pre> element is missing from the page.
 * @throws {SyntaxError} If the JSON data is malformed.
 * @see https://traderie.com/api/royalehigh/items?variants=&tags=true&page=${pageNumber}
 */
async function scrapeTraderie(pageNumber) {
    const url = `https://traderie.com/api/royalehigh/items?variants=&tags=true&page=${pageNumber}`;

    try {
        const browser = await puppeteer.launch({
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();

        await page.goto(url, { waitUntil: 'domcontentloaded' });

        /**
         * Extracts JSON data from the page content.
         * 
         * @returns {Object[]} Parsed JSON data from the page.
         */
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

/**
 * Immediately Invoked Function Expression (IIFE) to execute scraping.
 * Retrieves the page number from command-line arguments and calls scrapeTraderie.
 */
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
