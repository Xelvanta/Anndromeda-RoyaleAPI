# TO-DO

## **RHAPI7 Tasks (Version 7; Breaking Change)**

These tasks need to be completed before the release of RHAPI7:

---

## **1. Update `/item` Endpoint** (High Priority)

* **Goal**: Refactor the `/item` endpoint to utilize the item ID for identification instead of the URL-encoded item name.
* **Subtasks**:

  * Review current endpoint implementation.
  * Implement item ID-based identification.
  * Write tests to validate new functionality.

---

## **2. Revise `/item` Endpoint Response Format** (High Priority)

* **Goal**: Modify the `/item` endpoint to return JSON in the same format as the `/items` endpoint, in alignment with changes from RHAPI6.
* **Subtasks**:

  * Review `/items` endpoint response format.
  * Update `/item` endpoint to match the format.

---

## **3. Implement Improved Error Handling**

* **Goal**: Add comprehensive error handling to both `/item` and `/items` endpoints to provide consistent, detailed error messages for invalid requests.
* **Subtasks**:

  * Identify potential failure points in both endpoints.
  * Implement error handling mechanisms.
  * Test error handling with different invalid request scenarios.

---

## **4. Optimize Database Queries**

* **Goal**: Refactor `/item` and `/items` endpoints to improve database query performance and reduce latency, especially for large datasets.
* **Subtasks**:

  * Profile current query performance.
  * Identify and resolve performance bottlenecks.
  * Test and validate improvements.

---

## **5. Document API Changes**

* **Goal**: Update API documentation to reflect the changes made in the `/item` endpoint (new request format and response structure).
* **Subtasks**:

  * Revise API documentation for `/item` endpoint.
  * Add examples for new request/response format.
  * Review and update versioning in the docs.

---

## **6. Deprecate Old URL-Encoded Item Name Support**

* **Goal**: Implement a deprecation plan for the old URL-encoded item name support, with clear messages for users transitioning to the new item ID system.
* **Subtasks**:

  * Define a deprecation timeline.
  * Implement warning messages in the API for the old item name format.
  * Update API docs to highlight the deprecation.

---

**Notes**:
- Make sure the changes to the `/item` endpoint do not affect the GitHub Action cron jobs. However, these changes **should not** impact the cron jobs as long as the `/items` endpoint remains unchanged and the method to start the server stays the same. Please verify that no other parts of the system are inadvertently impacted by these updates.
