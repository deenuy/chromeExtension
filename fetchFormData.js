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

getCurrentTab().then((tab) => {
  chrome.scripting.executeScript(
    {
      target: { tabId: tab[0].id },
      function: fetchData,
    },
    (results) => {
      console.log("Popup script:");

      let result = results[0].result;
      document.getElementById("summary").innerHTML = result.short_desc;
      document.getElementById("description").innerHTML = result.bug_steps;
      document.getElementById("product_label").innerHTML = result.product_label;
      document.getElementById("version_select").innerHTML =
        result.version_select;
      document.getElementById("bug_type").innerHTML = result.bug_type;
      document.getElementById("hardware").innerHTML = result.hardware;
      document.getElementById("os").innerHTML = result.os;
      console.log(result);
    }
  );
});

async function getCurrentTab() {
  let queryOptions = { currentWindow: true, active: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  // console.log([tab]);
  return [tab];
}
