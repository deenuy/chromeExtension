
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
  return data;
}

async function getCurrentTab() {
  let queryOptions = { currentWindow: true, active: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return [tab];
}

// Temporary implementation for wait time and popup success message
getCurrentTab().then(async (tab) => {
  const id = tab[0].id;
  const sampleHTML = await fetchHTML();

  chrome.scripting.executeScript(
    {
      target: { tabId: tab[0].id },
      function: fetchData,
    },
    async (results) => {

      if (chrome.runtime.lastError) {
        alert('Sometging went wrong!');
        return;
     }

      let result = results[0].result;
      const message = await main(result);

      setTimeout(() => {
        chrome.scripting.executeScript(
          {
            target: { tabId: id },
            // Invoke RQ2 mapping with recommended message to prompt recommendation result
            files: ["./scripts/popup.js"],
          },
          () => {
            if (chrome.runtime.lastError) {
              alert('Sometging went wrong!');
              return;
            }
          }
        );

        //injecting css
        chrome.scripting.insertCSS(
          {
            target: { tabId: id },
            files: ["./css/popup.css"],
          },
          () => {
            console.log("Popup css is injected");
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
            if (chrome.runtime.lastError) {
              alert('Sometging went wrong!');
              return;
            }
            //Update message as task is completed
            document.getElementById("root").innerHTML =
              "Task is Completed Successfully";
          }
        );

        //closing the extension popup
        window.close();

      }, 3 * 1000);

    }
  );
});

const text = document.getElementsByClassName("text")[0];

// RQ2 mapping with recommended message to prompt recommendation result
async function customPrompt(message, sampleHTML) {
  try{
    let body = document.createElement("div");

  document.body.appendChild(body);

  var alertDiv = document.createElement("div");

  alertDiv.innerHTML = sampleHTML;
  alertDiv.setAttribute("class", "alert-div");
  alertDiv.setAttribute("id", "alert-div");
  document.body.appendChild(alertDiv);
  let results = document.getElementById("results");

  let j = 1;
  for(i in message){
    const result_p = document.createElement("p");
    result_p.setAttribute("class", "recommender-body");
    result_p.innerHTML = j++ + ". " + i + " (" + message[i] + "% relevance)";
    results.appendChild(result_p);
  }

  }
  catch(e){
    console.log(e);
  }
}

// Logic to iterate throguh recommender messages mapping with RQ2 result for comparision of label and corresponding message
const main = async (data) => {
  let keys_arr = {};

  //
  try{
    let rq2 = {};
    try{
      rq2 = await fetch('http://127.0.0.1:5000/imager_predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body : JSON.stringify(data),
      });
      rq2 = await rq2.json();
    }
    catch(e){
      console.log(e);
    }


    for (key in rq2) {
      if (rq2[key] > 0.5) {
        keys_arr[key] = rq2[key];
      }
    }

    // console.log(keys_arr);
    return keys_arr;
  }
  catch(e){
    console.log(e);
  }

};

// Fetch popup html
const fetchHTML = async () => {
  try{
    let response = await fetch("popup.html");
  let data = await response.text();
  // console.log(typeof(data));
  return data;
  }
  catch(e){
    return false;
  }
};
