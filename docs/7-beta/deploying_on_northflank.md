# Deploying RoyaleAPI on Northflank

This guide explains how to deploy **Anndromeda RoyaleAPI** on [Northflank.com](https://northflank.com/) and configure authentication.

---

## **Setup Steps**

1. **Create a new Service on Northflank**

   * Go to Northflank Dashboard → Create new → Build Service.
   * Add [https://github.com/Xelvanta/Anndromeda-RoyaleAPI](https://github.com/Xelvanta/Anndromeda-RoyaleAPI) or your own fork as the repository to build.
   * Choose **Docker** as the build type.

2. **Build**
   * Click build, choose the branch to build, then select the commit to build.
   * Wait for the build process to finish:

   ```
   [YYYY-MM-DDTHH:MM:SSZ INFO ] Process terminated with exit code 0
   [info] BuildService - Build successful.
   ```

3. **Deploy**

   * Go to Northflank Dashboard → Create new → Deployment Service.
   * Select Northflank as the deployment source.
   * Under Networking, add a new port like 10000. Set the protocol to HTTP and publicly expose this port to the internet.
   * Configure Environment Variables:

      * **PORT**: You must set PORT as an environment variable. Use the same number you just used for Networking.
      * **API_KEY** (Optional but Strongly Advised): If set, the Python service will use this environment variable as the authentication key for `/node/restart`.
     If not set, the service will default to the `api_key` defined in `config.json`.
    * After creation, logs should show something like:
    ```
    [YYYY-MM-DDTHH:MM:SSZ INFO ] Starting container entrypoint...
    [YYYY-MM-DDTHH:MM:SSZ INFO ] Successfully fetched environment variables.
    [YYYY-MM-DDTHH:MM:SSZ INFO ] Securely fetching environment variables...
    ```

---

### **End Notes**

* **Health Checks**: When deploying, the `/health` endpoint can be set as the path that Northflank uses for health checks. Use the same port you defined under networking as the port.
* **Memory Considerations**: Each Puppeteer page consumes significant RAM. If using the free Northflank plan (512 MB), reduce node_service `max_pages` and python_service `concurrent_pages` to avoid out-of-memory crashes.
* **Authentication**: Any request to `/node/restart` must include the `X-API-Key` header. If no `API_KEY` environment variable is set, the service falls back to the key in `config.json`.
* **Internal Node Communication**: The Python service communicates with Node.js internally. `/health` will report `ok` only if Node is responding.

---

This setup should allow RoyaleAPI to run on Northflank with proper authentication and configuration.
