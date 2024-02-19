import winreg
import requests
import datetime
from flask import Flask, render_template

app = Flask(__name__)

def fetch_installed_software():
    """ Fetches installed software from the Windows registry. """
    software_list = {}
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
    
    try:
        i = 0
        while True:
            subkey_name = winreg.EnumKey(reg_key, i)
            subkey = winreg.OpenKey(reg_key, subkey_name)
            try:
                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                software_list[name] = version
            except EnvironmentError:
                pass
            i += 1
    except WindowsError:
        pass
    
    return software_list

def fetch_vulnerabilities(software_list):
    """ Fetches vulnerabilities from the NVD that match installed software. """
    vulnerabilities = []
    one_month_ago = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?pubStartDate={one_month_ago}T00:00:00:000 UTC-00:00"
    response = requests.get(url)
    data = response.json()
    
    for item in data.get("result", {}).get("CVE_Items", []):
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        description = item["cve"]["description"]["description_data"][0]["value"]
        for software, version in software_list.items():
            if software.lower() in description.lower():
                vulnerabilities.append({
                    "id": cve_id,
                    "description": description,
                    "software": software,
                    "version": version
                })
    return vulnerabilities

@app.route('/')
def index():
    """ Main page of the web app, showing potential vulnerabilities. """
    installed_software = fetch_installed_software()
    vulnerabilities = fetch_vulnerabilities(installed_software)
    return render_template('index.html', vulnerabilities=vulnerabilities)

if __name__ == '__main__':
    app.run(debug=True)
