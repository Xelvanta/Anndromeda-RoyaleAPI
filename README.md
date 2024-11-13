# Anndromeda RoyaleAPI

**Anndromeda RoyaleAPI** (formerly Royale High API) is a Quart API to fetch Royale High item names and their community values from Traderie, returning results in JSON format.

## Features

- **Item Fetching**: Retrieves Royale High item names and their associated community values.

## Requirements

- Python 3.x
- Pip (Python package manager; usually comes with Python)

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ProjectAnndromeda/royalehigh-api.git
    cd royalehigh-api
    ```

2. **Create a Virtual Environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:

    - **Windows Command Prompt**:

        ```bash
        venv\Scripts\activate
        ```

    - **Windows PowerShell**:

        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

    - **macOS/Linux**:

        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Install Playwright Browsers**:

    After installing the dependencies, you need to install the necessary browser binaries for Playwright:

    ```bash
    playwright install
    ```

## Running the Application


1. **Run the Quart Application**:

    ```bash
    quart run
    ```

2. **Access the API**:

    Open Google Chrome or an API client (like Insomnia) and navigate to:

    ```bash
    http://127.0.0.1:5000/items
    ```

## Key Considerations

- API Response Time: The API may take a while to return data due to pagination and multiple page loads.
-  Handling: Includes basic error handling to manage network issues and timeouts.
- Dependencies: Ensure all packages in requirements.txt are installed, ideally within a virtual environment.
- Playwright Management: Playwright is required for browser automation; make sure to install necessary binaries.

## Contributing

We welcome contributions! Feel free to fork the project and submit a pull request if you’d like to help improve or expand **RoyaleAPI**.

## License

**RoyaleAPI** is open source and available under the GPL-3.0 license. See the LICENSE file for more details.

---

By **Anndromeda** (formerly Project Anndromeda)   
**Xelvanta Group Systems**  
For support or inquiries, please contact us at [enquiry.information@proton.me](mailto:enquiry.information@proton.me).  
GitHub: [https://github.com/Xelvanta](https://github.com/Xelvanta)