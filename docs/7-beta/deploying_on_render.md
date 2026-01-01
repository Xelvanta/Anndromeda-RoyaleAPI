# Deploying RoyaleAPI on Render

This guide explains how to deploy **Anndromeda RoyaleAPI** on [Render.com](https://render.com/) and configure authentication.

---

## **Setup Steps**

1. **Create a Web Service on Render**

   * Go to Render Dashboard → New → Web Service.
   * Connect your GitHub repository containing the RoyaleAPI code.
   * Choose **Docker** as the environment.

2. **Configure Environment Variables (Optional but Strongly Advised)**

   * **API_KEY**: If set, the Python service will use this environment variable as the authentication key for `/node/restart`.
     If not set, the service will default to the `api_key` defined in `config.json`.

3. **Deploy**

   * Render will build the environment, install dependencies, and start the service.
   * Logs should show something like:

     ```
     Pushing image to registry...
     Upload succeeded
     ==> Setting WEB_CONCURRENCY=1 by default, based on available CPUs in the instance
     ==> Deploying...
     ==> Your service is live 🎉
     ```

---

### **End Notes**

* **Memory Considerations**: Each Puppeteer page consumes significant RAM. If using the free Render plan (512 MB), reduce node_service `max_pages` and python_service `concurrent_pages` to avoid out-of-memory crashes.
* **Authentication**: Any request to `/node/restart` must include the `X-API-Key` header. If no `API_KEY` environment variable is set, the service falls back to the key in `config.json`.
* **Internal Node Communication**: The Python service communicates with Node.js internally. `/health` will report `ok` only if Node is responding.

---

This setup should allow RoyaleAPI to run on Render with proper authentication and configuration.
