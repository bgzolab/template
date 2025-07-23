### Tree Construction

```shell
mainifest.json          # all configuration of the Chrome extension
    - content.js        # run script after finishing page.
    - background.js     # load when chrome open up and listen some events(action).
                        # get more than page things which could be given through 
                        # message.
    - pop-up            # pop up view html
                        # ! notice: popup view is conflict
                        # with above click listener, view 
                        # more info via:
                        # https://stackoverflow.com/questions/17737263/how-to-tell-when-a-page-action-is-clicked-when-the-page-action-has-a-popup
```

```json
{
    "manifest_version": 2,                      /* Chrome API etc.*/
    "name": "Coding Train Extension",
    "version": "0.0.1",
    "content_scripts": [
        {
            "match": [
                "<all_urls>"                    /* Where js Run. Regex as well.*/
            ],
            "js": [
                "content.js"                    /* Which Would be Loaded.*/
            ]
        }
    ]
}
```

## Tampermonkey vs. Extension

> A practical solution is to start with whatever solution you like then see if has problems, and if there is none then you're fine.


- Tampermonkey gives `GM_` functions to using Chrome/Browser APIs.
- Tampermonkey's security could not be guaranteed.
- Extension must cross different browser platform.
  - Extension code
    - - Full access to all permitted `chrome.*` APIs.
  - Content scripts (via the manifest file or chrome.tabs.executeScript)
    - Executed in an "isolated world" environment.
    - Partial access to some of the chrome APIs, full access to the page's DOM (not to any of the window objects, including frames).
  - Injected scripts (via this method in a Content script) 
    - Full access to all properties in the page.
    - No access to any of the `chrome.*` APIs.
- Chrome apis such as bookmarks, cross-domain XMLHttpRequest etc.

## Refs

- [Chrome Extensions | Daniel Shiffman](https://shiffman.net/a2z/chrome-ext/ )
- [API Reference - Chrome Developers](https://developer.chrome.com/docs/extensions/reference/ )
- [javascript - Chrome extension code vs Content scripts vs Injected scripts - Stack Overflow](https://stackoverflow.com/questions/9915311/chrome-extension-code-vs-content-scripts-vs-injected-scripts )
- [Userscripts vs. Chrome Extension - Stack Overflow](https://stackoverflow.com/questions/13487661/userscripts-vs-chrome-extension )
- [browser - Should I write an extension or a tampermonkey script? - Stack Overflow](https://stackoverflow.com/questions/61420545/should-i-write-an-extension-or-a-tampermonkey-script )
- [javascript - Can Tampermonkey Userscript access Chrome API? - Stack Overflow](https://stackoverflow.com/questions/52497039/can-tampermonkey-userscript-access-chrome-api )
- icon via: https://www.iconfont.cn/collections/detail?cid=29558