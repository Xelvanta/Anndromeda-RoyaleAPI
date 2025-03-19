const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin()); // Enable the stealth plugin

async function scrapeTraderie(pageNumber) {
    /**
     * Fetches items from the Traderie API using Puppeteer.
     *
     * @param pageNumber - The page number to fetch.
     * @return {Promise<Array>} - A promise that resolves to an array of items.
     */
    const url = `https://traderie.com/api/royalehigh/items?variants=&tags=true&page=${pageNumber}`;

    try {
        console.log(`🌐 Fetching data from API: ${url}`);
        
        // Launch puppeteer browser
        const browser = await puppeteer.launch({
            headless: "new", // Run in headless mode
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();

        // Open the URL in Puppeteer
        await page.goto(url, { waitUntil: 'domcontentloaded' });

        // Extract the data from the page
        const data = await page.evaluate(() => {
            // Make sure to adjust the selector based on what the actual data looks like
            const items = JSON.parse(document.querySelector('pre').innerText); // Assuming data is inside a <pre> tag
            return items;
        });

        await browser.close();

        if (!data) {
            throw new Error('No data found');
        }

        console.log(`✅ Successfully fetched ${data.length} items from page ${pageNumber}`);
        return data;

    } catch (error) {
        console.error(`❌ Error fetching data from API (page ${pageNumber}):`, error);
        return [];
    }
}

(async () => {
    /**
     * Main function to fetch and print data from the Traderie API.
     */
    const pageNumber = parseInt(process.argv[2], 10) || 0;

    try {
        const scrapedData = await scrapeTraderie(pageNumber);
        console.log(JSON.stringify({ items: scrapedData }));
    } catch (error) {
        console.error("❌ Fetching failed:", error);
        process.exit(1);
    } finally {
        console.log("✅ Finished Fetching");
    }
})();