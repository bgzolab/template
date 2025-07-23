console.log("Chrome extension go.")

chrome.runtime.onMessage.addListener(gotMessage);

function gotMessage(message, sender, sendResponse){
    console.log(message.txt);

    if(message.txt == "hello") {
        // fill extension color
        let paragraphs = document.getElementsByTagName('p');
        for(elt of paragraphs){
            elt.style['background-color'] = '#FF00FF';
        }

        // replace img idea
        let filenames = [ "rainbow.png" ];
        
        let imgs = document.getElementsByTagName('img');

        for(imgElt of imgs){
            let r = Math.floor(Math.random() * filenames.length);
            let file = 'asserts/' + filenames[r];
            let url = chrome.extension.getURL(file);
            imgElt.src = url;
            console.log(url);
        }
    }
}