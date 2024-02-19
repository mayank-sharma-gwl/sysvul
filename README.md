### System Vulnerability Checker

* **System Vulnerability Checker** : This Python-based application utilizes the Windows registry to identify software installed on a Windows system and automatically checks for related vulnerabilities reported in the National Vulnerability Database (NVD). The tool provides a dashboard view of potential security risks associated with installed software versions, enhancing system security management.
* **Real-Time Vulnerability Monitoring and Reporting** : Integrating Flask for web interface development, the tool displays vulnerabilities that potentially affect the installed software, offering a real-time, easily accessible summary via a web browser. This enables system administrators to proactively manage patches and updates, ensuring software security and compliance with minimal manual intervention.

### Instructions for Running the Application:

1. Ensure Python and the required libraries (`flask` and `requests`) are installed on your Windows machine.
2. Save the Python script in a file, for example, `app.py`.
3. Create a directory named `templates` in the same folder as your Python script and place the `index.html` file inside it.
4. Run the script with administrative privileges to access the registry for installed software.
5. Open a web browser and go to `http://127.0.0.1:5000/` to view the dashboard.
