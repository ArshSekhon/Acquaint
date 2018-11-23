 
function extractHostname(url) {
    var hostname; 
    if (url.indexOf("//") > -1) {
        hostname = url.split('/')[2];
    }
    else {
        hostname = url.split('/')[0];
    } 
    hostname = hostname.split(':')[0]; 
    hostname = hostname.split('?')[0];

    return hostname;
}
chrome.runtime.onInstalled.addListener(function() {
    //clear exceptions
    chrome.storage.local.set({exceptionWebsites: []}, function () {});

    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
        chrome.declarativeContent.onPageChanged.addRules([{
          conditions: [new chrome.declarativeContent.PageStateMatcher({ 
          })
          ],
              actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
      });
  });

 chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    var chromeUrls = ["chrome://about","chrome://accessibility","chrome://appcache-internals","chrome://apps","chrome://blob-internals","chrome://bluetooth-internals","chrome://bookmarks","chrome://chrome","chrome://chrome-urls","chrome://components","chrome://conflicts","chrome://crashes","chrome://credits","chrome://device-log","chrome://devices","chrome://dino","chrome://discards","chrome://download-internals","chrome://downloads","chrome://extensions","chrome://flags","chrome://flash","chrome://gcm-internals","chrome://gpu","chrome://help","chrome://histograms","chrome://history","chrome://indexeddb-internals","chrome://inspect","chrome://interstitials","chrome://interventions-internals","chrome://invalidations","chrome://local-state","chrome://media-engagement","chrome://media-internals","chrome://nacl","chrome://net-export","chrome://net-internals","chrome://network-error","chrome://network-errors","chrome://newtab","chrome://ntp-tiles-internals","chrome://omnibox","chrome://password-manager-internals","chrome://policy","chrome://predictors","chrome://print","chrome://quota-internals","chrome://safe-browsing","chrome://serviceworker-internals","chrome://settings","chrome://signin-internals","chrome://site-engagement","chrome://suggestions","chrome://supervised-user-internals","chrome://sync-internals","chrome://system","chrome://taskscheduler-internals","chrome://terms","chrome://thumbnails","chrome://tracing","chrome://translate-internals","chrome://usb-internals","chrome://user-actions","chrome://version","chrome://webrtc-internals","chrome://webrtc-logs","chrome://badcastcrash/","chrome://inducebrowsercrashforrealz/","chrome://crash/","chrome://crashdump/","chrome://kill/","chrome://hang/","chrome://shorthang/","chrome://gpuclean/","chrome://gpucrash/","chrome://gpuhang/","chrome://memory-exhaust/","chrome://ppapiflashcrash/","chrome://ppapiflashhang/","chrome://inducebrowserheapcorruption/","chrome://heapcorruptioncrash/","chrome://quit/","chrome://restart/"]

    if (changeInfo.status == 'complete') { 
        chrome.storage.sync.get({exceptionWebsites: [], UserId:'',IsSAPConnectActive:true}, function(pluginActive ) {  
            if(pluginActive.IsSAPConnectActive && chromeUrls.indexOf("chrome://"+extractHostname(tab.url))==-1){

                chrome.storage.local.get({exceptionWebsites: [], UserId:''}, function (result) { 
                    var exceptionWebsites = result.exceptionWebsites;
                    if(exceptionWebsites.indexOf(extractHostname(tab.url))==-1){
                        // make the API call here send tab.url
                        var settings = {
                            "async": true, 
                            "url": "http://127.0.0.1:5000/ext/processActivity?url="+tab.url+"&userid="+result.UserId,
                            "method": "GET",
                             
                        }
                        
                        $.ajax(settings).done(function (response) {
                            
                        }).fail((a)=>{console.log(a.statusCode())});;
                       
                    }
                        
                });
                
            }  
        });
        
    }
  });