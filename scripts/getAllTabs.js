document.getElementById("getAllTabs").addEventListener("click", () => {
  const tabData = getTabsData();
  const windowData = getBrowserWindowsData();
  console.log(tabData);
  console.log(windowData);
});

document.getElementById("getAllWindows").addEventListener("click", () => {
  // const windowAppData = getAppWindowsData();
  // console.log(windowAppData);
  getAppWindowsData();
});

const getTabsData = () => {
  let tabsData = [];
  chrome.tabs.query({}, (tabs) => {
    // console.log(tabs);
    tabs.forEach((tab) => {
      tabsData.push({
        title: tab.title,
        url: tab.url,
      });
    });
  });
  return tabsData;
};

// Use the chrome.windows API to interact with browser windows. You can use this API to create, modify, and rearrange windows in the browser.
const getBrowserWindowsData = () => {
  let windowsData = [];
  chrome.windows.getAll({ populate: true }, (windows) => {
    // console.log(windows);
    windows.forEach((window) => {
      windowsData.push({
        title: window.title,
        tabs: window.tabs,
      });
    });
  });
  return windowsData;
};

const getAppWindowsData = () => {
  chrome.tabs.query({ active: true }, (tabs) => {
    if (tabs.length) {
      const tab = tabs[0];
      chrome.desktopCapture.chooseDesktopMedia(["window"], tab, (streamId) => {
        console.log(streamId, tab);
      });
    }
  });
  return false;
};
