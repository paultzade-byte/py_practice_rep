# 🐍 Python Sandbox & Portfolio

Hello! 👋 This is my personal sandbox repository where I store my practical tasks, code experiments, 
and examples of using various Python tools.

Here you can find everything from unit tests to algorithm performance measurements and UI automation. 
The repository is constantly updated with new pet projects and snippets.

---

## 🗂️ What's inside (Repository structure)

The projects are divided into folders according to the technologies and concepts I studied or tested:

### 🧪 1. Pytest & Fixtures (`/pytest`)
Practice writing tests using the `pytest` framework.
* Using fixtures to prepare test data.
* Parameterizing tests.
* Writing unit and integration tests to verify application logic.

### ⏱️ 2. Performance & Benchmarks (`/performance`)
My research on code performance and algorithm optimization.
* **Humanoid vs Siliconoid (timeit_experiment.py):** 
Measuring the execution time (via the `timeit` module) of two different mathematical algorithms 
for calculating currency rates. 
Demonstrates the difference between a mathematical approach and using the remainder of a division.

### 🎭 3. Playwright Automation (`/vis_mon_system`) 
* **Visual Content Integrity Monitoring System**
Link for the used page https://www.saucedemo.com/
This project began as a proof of concept for image validation using SauceDemo. Tests compare locally stored images with the images served by the application by converting both into binary data, Base64 strings, and SHA-256 hashes, ensuring their integrity through value comparison.

The repository is being expanded into a complete UI automation suite, including negative login tests and Page Object scenarios covering shopping cart functionality and regression checks for intentionally broken application behavior.

### 🇺🇦 4. EDRPOU & IPN Generator (`/edrpou_rnokpp_generator`)
* **Ukrainian Mock Data Utility**
A Python tool with a Tkinter GUI for generating and validating 8-digit EDRPOU codes and IPNs according to Ukrainian state standards. Useful for QA engineers and developers who need to quickly create valid test data for local systems. 
*(For detailed mathematical algorithms and check-digit logic, see the README inside this folder).*

### API 5. REQUESTS (`/requests`)
* **Practical sprint focused on REST API testing using the requests library and the Restful-booker training service.
Features:
Automated CRUD tests for the Booking entity. 
Authentication using access tokens in request headers and cookies. 
Validation of HTTP status codes, response headers, and JSON data. 
Reusable base API client to separate request logic from test cases. 
Clean and maintainable test structure following basic API testing practices
Link for the used resource https://restful-booker.herokuapp.com/ 

### 🛠️ 6. Other experiments (`/misc`)
Various scripts, solving algorithmic problems, and other interesting things that I threw here while studying.

📬 Contact me
If you have any questions or suggestions about the code, you can mail me:

Email: paultzade@gmail.com
