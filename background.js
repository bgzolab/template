console.log("Background Runnning.")

chrome.browserAction.onClicked.addListener(buttionClicked);

function buttionClicked(tab){
    console.log("Button Clicked.")
    // console.log(tab)
    let msg = {
        txt: "hello"
    }
    chrome.tabs.sendMessage(tab.id, msg);
}