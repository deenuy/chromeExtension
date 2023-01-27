# Image Capturing and Processing in Software Teams

This is the project repository for paper `Image Capturing and Processing in Software Teams`. In this study, we focus on empirical evaluation within Mozilla Foundation to (i) determine the development tasks that benefit from image sharing and processing, (ii) develop a recommender system, and (iii) develop a web extension to identify and capture informative images from open windows.

# Folder Structure

### Folder structure and naming conventions for this project

    .
    ├── archive                 # Reference work
    ├── readings                # Papers refered for this research
    ├── browserExtension        # Google chrome extension and flask API
    ├── ml-model-dev            # Machine learning model development work
    ├── docs                    # Documentation files
    ├── LICENSE
    └── README.md

# Steps to install google chrome extension

1. Clone or download repository.
2. Open Google Chrome
3. Navigate to chrome://extensions/
4. Click "Load Unpacked"
5. Use the file browser to browse to chromeExtension directory and click "Select"
6. Ensure the extension is enabled

# Steps to Install Python Packages and start Python Flask API

1. Assuming user machine already has Python 3.x
2. Install python packages for server side code "pip install -r server/requirements.txt"
3. Start Python Flask to run backend server API from following steps

- cd server
- flask run

# Testing ImageR chrome extension from Google Chrome browser

1. Open following hyperlink in Google chrome browser to create a new bug report in Bugzilla.

- Link: 'https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&format=__default__'

2. Instead of wizard, switch the interface to standard bug entry form. You can locate at bottom right corner.
3. Select a product category of your bug report, e.g. Firefox
4. Describe bug report details (Text and Metadata information)
5. Once you enter bug report with all the details, click on chrome extension "ExineLab Bugzilla RecSys'

# Output

1. Verify if ImageR extension triggers a popup screen with recommendation to select image type for bug report

# Sample Test Scenarios

1. macOS Share menu icons are missing (Bug report ID: 1629533)
2. Text fields and search fields no longer respect the Aqua override (Bug report ID: 1702877)
3. strange password auto-fill behavior when entering a differently-cased version of the saved username (Bug report ID: 499649)
