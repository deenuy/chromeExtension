// Temporary accomodation for Backend API response results
const rq2 = {
  Code: 0.98,
  "Run Time Error": 0.71,
  "Menus and Preferences": 0.22,
  "Program Input": 0.21,
  "Desired Output": 0.11,
  "Program Output": 0.18,
  "Dialog Box": 0.52,
  "Steps and Processes": 0.25,
  "CPU/GPU Performance": 0.18,
  "Algorithm/Concept Description": 0.13,
};

// Template for recommender system messages
const messages = {
  msg01: {
    classes: ["Code", "Run Time Error", "Dialog Box"],
    message: "Recommender message template 01",
  },
  msg02: {
    classes: ["Menus and Preferences", "Program Input", "Desired Output"],
    message: "Recommender message template 02",
  },
  msg03: {
    classes: ["Program Output", "Steps and Processes", "CPU/GPU Performance"],
    message: "Recommender message template 03",
  },
  msg04: {
    classes: ["Algorithm/Concept Description"],
    message: "Recommender message template 04",
  },
};

// Fetch Bugzilla Form Data
function fetchData() {
  let data = {};

  try {
    let short_desc = document.getElementById("short_desc");
    let bug_steps = document.getElementById("bug_steps")
      ? document.getElementById("bug_steps")
      : document.getElementById("comment");
    let expected = document.getElementById("expected")
      ? document.getElementById("expected")
      : document.getElementById("comment");
    let product_label = document.getElementById("product_label")
      ? document.getElementById("product_label")
      : document.getElementById("field_container_product");
    let version_select = document.getElementById("version_select")
      ? document.getElementById("version_select")
      : document.getElementById("version");

    let bug_type = document.querySelector('input[name="bug_type"]:checked')
      ? document.querySelector('input[name="bug_type"]:checked').value
      : "defect";

    let hardware = document.getElementById("rep_platform")
      ? document.getElementById("rep_platform").value
      : null;
    let os = document.getElementById("op_sys")
      ? document.getElementById("op_sys").value
      : null;

    data = {
      short_desc: short_desc.value,
      bug_steps: bug_steps.value,
      description: expected.value,
      product_label: product_label.innerHTML,
      version_select: version_select.value,
      bug_type: bug_type,
      hardware: hardware,
      os: os,
    };
  } catch (e) {
    data = {
      short_desc: "",
      bug_steps: "",
      description: "",
      product_label: "",
      version_select: "",
      bug_type: "",
      hardware: "",
      os: "",
    };
  }
  // console.log(short_desc, short_desc.value);
  return data;
}

async function getCurrentTab() {
  let queryOptions = { currentWindow: true, active: true };
  console.log(queryOptions);
  let [tab] = await chrome.tabs.query(queryOptions);
  console.log([tab][0].url);
  return [tab];
}

// Temporary implementation for wait time and popup success message
getCurrentTab().then(async (tab) => {
  const id = tab[0].id;
  const sampleHTML = await fetchHTML();
  // console.log("sampleHTML", sampleHTML);

  chrome.scripting.executeScript(
    {
      target: { tabId: tab[0].id },
      function: fetchData,
    },
    (results) => {
      console.log("Popup script:", results[0].result);

      let result = results[0].result;
      const message = main();
      // console.log(result);

      setTimeout(() => {
        chrome.scripting.executeScript(
          {
            target: { tabId: id },
            // Invoke RQ2 mapping with recommended message to prompt recommendation result
            files: ["./scripts/popup.js"],
          },
          () => {
            // console.log("Popup script is injected");
          }
        );
        chrome.scripting.executeScript(
          {
            target: { tabId: id },
            // Invoke RQ2 mapping with recommended message to prompt recommendation result
            function: customPrompt,
            args: [message, sampleHTML],
          },
          () => {
            //Update message as task is completed
            document.getElementById("root").innerHTML =
              "Task is Completed Successfully";
          }
        );
      }, 5 * 1000);
    }
  );
});

const text = document.getElementsByClassName("text")[0];
// console.log(text);

// RQ2 mapping with recommended message to prompt recommendation result
async function customPrompt(message, sampleHTML) {
  let body = document.createElement("div");

  document.body.appendChild(body);

  var alertDiv = document.createElement("div");

  alertDiv.setAttribute(
    "style",
    "position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); color:black; background-color: #fff;" +
      "padding: 20px; border: 1px solid #000; z-index: 9999; text-align: center; font-size: 20px; border-radius: 5px;"
  );

  alertDiv.innerHTML = sampleHTML;
  alertDiv.setAttribute("class", "alert-div");
  alertDiv.setAttribute("id", "alert-div");

  // alertDiv.getElementById("recommender_message").innerHTML = message;

  document.body.appendChild(alertDiv);

  document.getElementById("recommender_message").innerHTML = message;
}

// Logic to iterate throguh recommender messages mapping with RQ2 result for comparision of label and corresponding message
const main = () => {
  let keys_arr = [];
  for (key in rq2) {
    if (rq2[key] > 0.5) {
      keys_arr.push(key);
    }
  }

  for (key in messages) {
    if (JSON.stringify(messages[key].classes) === JSON.stringify(keys_arr)) {
      // console.log(messages[key].message)
      return messages[key].message;
    }
  }
  return false;
};

// Fetch popup html
const fetchHTML = async () => {
  let response = await fetch("popup.html");
  let data = await response.text();
  // console.log(typeof(data));
  return data;
};
