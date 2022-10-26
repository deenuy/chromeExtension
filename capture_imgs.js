chrome.action.onClicked.addListener(function (tab) {
  chrome.desktopCapture.chooseDesktopMedia(
    ["screen", "window", "tab"],
    tab,
    (streamId) => {
      //check whether the user canceled the request or not
      if (streamId && streamId.length) {
        setTimeout(() => {
          chrome.tabs.sendMessage(
            tab.id,
            { name: "stream", streamId },
            (response) => console.log(response)
          );
        }, 200);
      }
    }
  );
});

chrome.runtime.onMessage.addListener((message, sender, senderResponse) => {
  if (message.name === "download" && message.url) {
    chrome.downloads.download(
      {
        filename: "screenshot.png",
        url: message.url,
      },
      (downloadId) => {
        senderResponse({ success: true });
      }
    );

    return true;
  }
});

short_desc = document.getElementById("short_desc");
bug_steps = document.getElementById("bug_steps");
console.log(short_desc, short_desc.value);

chrome.runtime.onMessage.addListener((message, sender, senderResponse) => {
  if (message.name === "stream" && message.streamId) {
    let track, canvas;
    navigator.mediaDevices
      .getUserMedia({
        video: {
          mandatory: {
            chromeMediaSource: "desktop",
            chromeMediaSourceId: message.streamId,
          },
        },
      })
      .then((stream) => {
        track = stream.getVideoTracks()[0];
        const imageCapture = new ImageCapture(track);
        return imageCapture.grabFrame();
      })
      .then((bitmap) => {
        track.stop();
        canvas = document.createElement("canvas");
        canvas.width = bitmap.width; //if not set, the width will default to 200px
        canvas.height = bitmap.height; //if not set, the height will default to 200px
        let context = canvas.getContext("2d");
        context.drawImage(bitmap, 0, 0, bitmap.width, bitmap.height);
        return canvas.toDataURL();
      })
      .then((url) => {
        chrome.runtime.sendMessage({ name: "download", url }, (response) => {
          if (response.success) {
            alert("Screenshot saved");
          } else {
            alert("Could not save screenshot");
          }
          canvas.remove();
          senderResponse({ success: true });
        });
      })
      .catch((err) => {
        alert("Could not take screenshot");
        senderResponse({ success: false, message: err });
      });
    return true;
  }
});
