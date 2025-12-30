/**
 * fetchData.js
 *
 * Long-lived Puppeteer service that fetches Traderie API pages
 * using a single Chromium instance and a reusable page pool.
 *
 * This avoids repeatedly launching browsers and preserves
 * cookies, TLS fingerprints, and behavioral consistency.
 */

const express = require("express");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const app = express();
app.use(express.json());

/**
 * Puppeteer browser instance (single, global)
 * @type {import('puppeteer').Browser}
 */
let browser;

/**
 * Pool of reusable pages (tabs)
 * @type {import('puppeteer').Page[]}
 */
const pagePool = [];

/**
 * Maximum concurrent pages allowed.
 * This limits load and reduces bot-detection risk.
 */
const MAX_PAGES = 5;

/**
 * Initializes the Puppeteer browser and pre-allocates pages.
 */
async function initBrowser() {
    browser = await puppeteer.launch({
        headless: "new",
        args: [
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    });

    for (let i = 0; i < MAX_PAGES; i++) {
        const page = await browser.newPage();

        // Set a realistic user agent
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) " +
            "Chrome/120.0.0.0 Safari/537.36"
        );

        pagePool.push(page);
    }

    console.log(`✅ Browser initialized with ${MAX_PAGES} pages`);
}

/**
 * Acquires a page from the pool.
 * Waits if no pages are currently available.
 *
 * @returns {Promise<import('puppeteer').Page>}
 */
async function acquirePage() {
    while (pagePool.length === 0) {
        await new Promise(resolve => setTimeout(resolve, 50));
    }
    return pagePool.pop();
}

/**
 * Returns a page back to the pool.
 *
 * @param {import('puppeteer').Page} page
 */
function releasePage(page) {
    pagePool.push(page);
}

/**
 * Fetch Traderie data for a given page number.
 *
 * Endpoint:
 *   GET /traderie?page=<number>
 */
app.get("/traderie", async (req, res) => {
    const pageNumber = Number(req.query.page ?? 0);
    const url = `https://traderie.com/api/royalehigh/items?variants=&tags=true&page=${pageNumber}`;

    let page;

    try {
        page = await acquirePage();

        await page.goto(url, { waitUntil: "domcontentloaded" });

        const data = await page.evaluate(() => {
            const pre = document.querySelector("pre");
            if (!pre) {
                throw new Error("Expected <pre> element not found");
            }
            return JSON.parse(pre.innerText);
        });

        res.json(data);

    } catch (error) {
        console.error(`❌ Failed to fetch page ${pageNumber}:`, error.message);
        res.status(500).json({ error: error.message });

    } finally {
        if (page) {
            // Clear page state between requests
            await page.goto("about:blank");
            releasePage(page);
        }
    }
});

/**
 * Graceful shutdown handler.
 */
async function shutdown() {
    console.log("🛑 Shutting down Puppeteer service...");
    if (browser) {
        await browser.close();
    }
    process.exit(0);
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

/**
 * Service entry point.
 */
// Immediately listen
const server = app.listen(3001, () => {
    console.log("🚀 Puppeteer service listening on port 3001");
    process.stdout.write("NODE_READY\n");
});

// Initialize browser asynchronously in background
initBrowser().catch(err => {
    console.error("❌ Browser init failed:", err);
    process.exit(1);
});


