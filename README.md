# Google Chrome Extension for ExineLab Bugzilla RecSys

A Google Chrome Extension that recommends (predicts) the image type to attach with bug report created in Firefox Bugzilla incident report system.

# Steps to install google chrome extension

1. Clone or download repository.
2. Open Google Chrome
3. Navigate to chrome://extensions/
4. Click "Load Unpacked"
5. Use the file browser to browse to chromeExtension directory and click "Select"
6. Ensure the extension is enabled

# Testing without backend API

1. Update RQ2 api response manually in the file '/api/rq2_api_response.json'
2. Update recommender system messages mapping class labels in the file '/api/recommender_msgs.json'
3. Open url in google chrome browser to create a bugzilla ticket. URL: 'https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&format=__default__'
4. Describe bug/incident report details (Text and Metadata information)
5. Click on chrome extension "ExineLab Bugzilla RecSys'

# Testing with backend API

1. Open url in google chrome browser to create a bugzilla ticket.
   - URL: 'https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&format=__default__'
2. Describe bug/incident report details (Text and Metadata information)
3. Click on chrome extension "ExineLab Bugzilla RecSys'

# Output

1. Verify if extension trigger popup screen to user for processing the bug information
2. Verify if extension responds with recommended message prompting user to upload image type matching with bug/incident report
