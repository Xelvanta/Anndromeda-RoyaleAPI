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

### 3️⃣ **Get Data from Web**  
- In the ribbon, select **From Web**.
- In the dialog that appears, enter the API endpoint:

```text
http://127.0.0.1:5000/items
```

or add a parameter:

```text
http://127.0.0.1:5000/items?name=<ITEM_NAME>
```

Click **OK** to proceed. You will see the program start scraping data in the terminal.

### 4️⃣ **Opening the Advanced Editor in Power Query**  
- After the data loads, navigate to the **View** tab.
- In the ribbon, click on **Advanced Editor**.

### 5️⃣ **Example Usage: Paste the M Code**  
In the **Advanced Editor**, you could replace the default code with something like this M code:

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

    // Extract All Field Names
    AllFieldNames = if List.IsEmpty(AllRecords) then {} else List.Distinct(List.Combine(List.Transform(AllRecords, each Record.FieldNames(_)))),

    // Dynamically Construct the Table
    TableFromRecords =  if List.IsEmpty(AllRecords) then Table.FromColumns({}) else Table.FromRecords(AllRecords, AllFieldNames),
    #"Expanded name" = Table.ExpandRecordColumn(TableFromRecords, "name", {"name", "value"}, {"name", "value"})

in
    #"Expanded name"
```

- Once you’ve pasted the M code, you should see that the `List` column has expanded into `name` and `value` columns.
- Click the expand icon (the small icon with two arrows) next to the `List` column to proceed with this transformation.
- This is just one approach for loading and transforming your data!

### 6️⃣ **Loading the Data into Excel**  
- After you’re happy with the data, load it into Excel by clicking **Close & Load**. This will populate the table with the transformed data.

---

## ⚠️ Troubleshooting

- **🔍 Connection Issue**: If Excel is unable to connect to the endpoint, double-check that the Quart server is running.  If the server isn't running, Excel won't be able to fetch the data.
