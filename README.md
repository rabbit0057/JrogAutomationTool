# JrogAutomationTool

# 🔄 Automation Framework (UI + API)

A test automation framework designed to support **both UI and API testing**.

## 🛠️ Tech Stack

| Layer      | Technology                       |
|------------|----------------------------------|
| Language   | Python                           |
| UI Testing | Selenium                         |
| API Testing| Requests                         |
| Reporting  | Allure                           |
| Runner     | Pytest                           |

## 🐍 Installing Python (macOS, Windows, Linux)
To run this project, you need Python 3.8+ installed on your system.

## 📊 Allure Report Installation
Allure is a flexible, lightweight, multi-language test report tool. Below are instructions to install it on macOS, Windows, and Linux.

##🖥 macOS
Using Homebrew (Recommended)
```bash
brew install allure
```
Verify installation:
```bash
allure --version
```
🪟 Windows
Download Allure CLI from:
https://github.com/allure-framework/allure2/releases

Extract the ZIP to a folder (e.g., C:\allure)

Add the bin directory to your system PATH:

Open System Properties → Environment Variables

Under System variables, edit the Path variable and add:
```bash
C:\allure\bin
```
```bash
allure --version
```
🐧 Linux
Using Snap (Ubuntu/Debian-based):
Download Allure CLI:
https://github.com/allure-framework/allure2/releases

Extract it and move to /opt/allure:

```bash
sudo unzip allure-2.x.x.zip -d /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/bin/allure
```
Verify:
```bash
allure --version
```

---

## 📁 Framework Setup & Execution Steps
```bash
# Clone the repo
git clone https://github.com/rabbit0057/JrogAutomationTool.git
```
```bash
# Clone the repo
cd JrogAutomationTool
```
```bash
# Install dependencies
pip install -r requirements.txt
```
```bash
# For Window in Powershell
$env:PYTHONPATH = Get-Location
```
```bash
# For Mac 
export PYTHONPATH=$(pwd)
```
```bash
# Make Sure Docker daemon is running  
```
```bash
# To Clean or generate allure-report foler 
allure generate allure-results -- clean -o allure-report
```

```bash
# To Clean or generate allure-report foler 
allure generate allure-results -- clean -o allure-report
```
```bash
# To Execute API Related Tests
pytest -v -s  -m "api" Tests/ --alluredir=allure-report/
```
```bash
# To Execute UI Related Tests
pytest -v -s  -m "ui" Tests/ --alluredir=allure-report/
```
```bash
# To Execute both UI and API Tests
pytest -v -s  -m "testsuite" Tests/ --alluredir=allure-report/
```
```bash
# Post test execution need to serve allure-reports
allure serve allure-report/
```

```bash
# Terminal & Allure Report Output
```
![My Screenshot](https://drive.google.com/uc?export=view&id=1vTZZKJm5eazft1ip9yJ-au5ShOTYLU_m)

![My Screenshot](https://drive.google.com/uc?export=view&id=1LQ1RU97qByUAN6Afn6gh9mACgygf5O8p)

![My Screenshot](https://drive.google.com/uc?export=view&id=1uAlL2ztnUmD_1XA3w4TBYWF7ACo4kDX7)

![My Screenshot](https://drive.google.com/uc?export=view&id=1Ky5fzs8JGGBbOr5mCeIpn2pQXAgkySoY)










