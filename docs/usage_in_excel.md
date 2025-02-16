# 🌐 Anndromeda RoyaleAPI | Usage in Excel

This documentation assumes the program is already installed with all necessary dependencies and binaries. If the server is not yet set up for use, follow the instructions in the `README.md` to set it up.

### 1️⃣ **Ensure the Quart Server is Running**  
Before attempting to connect Excel to RoyaleAPI, start the Quart server:

```bash
quart run
```

### 2️⃣ **Open Excel**  
- Open a new or existing workbook in Excel.
- Navigate to the **Data** tab.

### 3️⃣ **Access the API**  
#### Using Get Data From Web
- In the ribbon, select **From Web**.
- In the dialog that appears, enter an API endpoint:
```text
http://127.0.0.1:5000/items?name=<ITEM_NAME>
```
- After you’re happy with the data, load it into Excel by clicking **Close & Load**. This will populate the table with the data.

#### Using the WEBSERVICE function
- Paste the following function into an empty cell. Replace the example with a valid API endpoint:
```text
=WEBSERVICE("http://127.0.0.1:5000/item?name=<ITEM_NAME>"
```
- Excel will automatically populate the cell with the JSON response.

📌 Note: See the **usage_in_excel.xlsx** file to see an example of how to use the API to fetch a specific item's value (Recommended to view).

---

## ⚙️ Example #1: Fetch All Items  
In **Excel**, you can get a list of all items available via the API.
1. In the ribbon, select **From Web**.
2. In the dialog that appears, enter the API endpoint:
```text
http://127.0.0.1:5000/items
```
3. Click **OK** to proceed. You will see the program start scraping data in the terminal.
4. After the data loads, navigate to the **View** tab.
5. In the ribbon, click on **Advanced Editor**.
6. The following M code will retrieve data from `http://127.0.0.1:5000/items`:

```m
let
    // Connect to the endpoint
    Source = Json.Document(Web.Contents("http://127.0.0.1:5000/items")),

    // Check if the source is empty
    SourceToList = if Source = null or Source = {} then {} else
    if Source is list then Source else {Source}, // Ensures source is a list

    // Convert to table, handling empty source case
    SourceToTable = 
        if List.IsEmpty(SourceToList) then
            Table.FromColumns({}) // Creates an empty table if no data
        else
            Table.FromList(SourceToList, Splitter.SplitByNothing(), null, null, ExtraValues.Error),

    // Extract All Records
    AllRecords = if Table.IsEmpty(SourceToTable) then {} else SourceToTable[Column1],

    // Dynamically Construct the Table
    TableFromRecords = if List.IsEmpty(AllRecords) then Table.FromColumns({}) else Table.FromRecords(AllRecords),
    #"Expanded name" = Table.ExpandRecordColumn(TableFromRecords, "name", {"name", "value"}, {"name", "value"})

in
    #"Expanded name"
```

7. Once you’ve pasted the M code, you should see that the `List` column has expanded into `name` and `value` columns.
8. Click the expand icon (the small icon with two arrows) next to the `List` column to proceed with this transformation.
9. This will provide you with a table of all available items and their corresponding values.

---

## ⚙️ Example #2: Fetch a Specific Item's Value  
To fetch a specific item’s value, you can input the item name in a cell and dynamically retrieve its value from the API.

1. Input the Item Name: Type the name of the item you want to fetch in **cell A2**.
2. Fetch Data from the API: In **cell B2**, use the following formula to request data:

```excel
=WEBSERVICE("http://127.0.0.1:5000/item?name=" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A2, " ", "%20"), ",", "%2C"), "&", "%26"))
```

This will make a request to the API with the item name provided in **A2**.

3. Extract the Value: In **cell C2**, use this formula to extract and sanitize the JSON response:

```excel
=MID(B2, FIND(":", B2) + 2, FIND("}", B2) - FIND(":", B2) - 3)
```

### Example Usage:  
- **A2**: `14 Karat Gold Infinity Chain`  
- **B2**: `=WEBSERVICE("http://127.0.0.1:5000/item?name=" & SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A2, " ", "%20"), ",", "%2C"), "&", "%26"))`  
- **C2**: `=MID(B2, FIND(":", B2) + 2, FIND("}", B2) - FIND(":", B2) - 3)`

**Result**:  
- **B2** will contain the full JSON response:  
   `{"value": 14,000}`  
- **C2** will extract the value:  
   `14,000`

---

## ⚠️ Troubleshooting

- **🔍 Connection Issue**: If Excel is unable to connect to the endpoint, double-check that the Quart server is running.  If the server isn't running, Excel won't be able to fetch the data.
