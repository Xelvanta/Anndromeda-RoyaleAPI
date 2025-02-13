const puppeteer = require('puppeteer-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(stealthPlugin());

async function scrapeTraderie(browser, page, pageNumber) {
    const url = `https://traderie.com/royalehigh/products?page=${pageNumber}`;

    try {
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });  // Wait for page to load
        console.log(`Scraping page: ${pageNumber}`);

        // **Updated Selectors Based on Your Confirmed HTML Structure**
        //const itemElements = Array.from(document.querySelectorAll('div.sc-eqUAAy.sc-kFWlue.cZMYZT.ecXFYy.item-img-container'));  //Root element, as validated.
        //const items = await page.evaluate(() => { //Fix was here, so data has javascript
          const items = await page.evaluate(() => { //Fix was here, so data has javascript
          //Query the items inside the function
          const itemElements = Array.from(document.querySelectorAll('div.sc-eqUAAy.sc-kFWlue.cZMYZT.ecXFYy.item-img-container'));
            //Now all the item are in a try block, so one won't stop the loop
            return itemElements.map(itemElement => {
                let itemName = 'Unknown';
                try {
                    itemName = itemElement.querySelector('div.sc-bkEOxz.fSHNlx').innerText;
                } catch (error) {
                    console.error("Error getting item name: ", error)
                }
                let itemValue = 0;
                 try {
                    const valueElement = itemElement.querySelector('div.item-currencies > div.listing-bells');
                    itemValue = valueElement ? valueElement.innerText : 0;
                 } catch (error){
                    console.error("error getting the bell values", error)
                    itemValue = 0;
                 }

                return {
                    name: itemName,
                    value: itemValue,
                };
            });
        });

        return items;

    } catch (error) {
        console.error(`Error scraping page ${pageNumber}:`, error);
        return [];
    }
}

(async () => {
  // Get the page number from the command line arguments
  const pageNumber = parseInt(process.argv[2], 10) || 0;
  const url = `https://traderie.com/royalehigh/products?page=${pageNumber}`;

    const browser = await puppeteer.launch({ headless: false }); //Launch it OUTSIDE, and pass as argument
    try {
        const page = await browser.newPage();
        const scrapedData = await scrapeTraderie(browser,page,pageNumber);
        //Now return data as an array
        console.log(JSON.stringify(scrapedData));
        //await page.screenshot({path: 'test.png'})
    } catch (error) {
        console.error("Scraping failed:", error);
        process.exit(1); // Exit with a non-zero code to indicate failure
    } finally {
      console.log("Finished Scraping")
        await browser.close();  //Closing the browser AFTER retrieving all values.
        process.exit(0);
    }
})();