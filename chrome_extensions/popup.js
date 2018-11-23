var chromeUrls = ["chrome://about","chrome://accessibility","chrome://appcache-internals","chrome://apps","chrome://blob-internals","chrome://bluetooth-internals","chrome://bookmarks","chrome://chrome","chrome://chrome-urls","chrome://components","chrome://conflicts","chrome://crashes","chrome://credits","chrome://device-log","chrome://devices","chrome://dino","chrome://discards","chrome://download-internals","chrome://downloads","chrome://extensions","chrome://flags","chrome://flash","chrome://gcm-internals","chrome://gpu","chrome://help","chrome://histograms","chrome://history","chrome://indexeddb-internals","chrome://inspect","chrome://interstitials","chrome://interventions-internals","chrome://invalidations","chrome://local-state","chrome://media-engagement","chrome://media-internals","chrome://nacl","chrome://net-export","chrome://net-internals","chrome://network-error","chrome://network-errors","chrome://newtab","chrome://ntp-tiles-internals","chrome://omnibox","chrome://password-manager-internals","chrome://policy","chrome://predictors","chrome://print","chrome://quota-internals","chrome://safe-browsing","chrome://serviceworker-internals","chrome://settings","chrome://signin-internals","chrome://site-engagement","chrome://suggestions","chrome://supervised-user-internals","chrome://sync-internals","chrome://system","chrome://taskscheduler-internals","chrome://terms","chrome://thumbnails","chrome://tracing","chrome://translate-internals","chrome://usb-internals","chrome://user-actions","chrome://version","chrome://webrtc-internals","chrome://webrtc-logs","chrome://badcastcrash/","chrome://inducebrowsercrashforrealz/","chrome://crash/","chrome://crashdump/","chrome://kill/","chrome://hang/","chrome://shorthang/","chrome://gpuclean/","chrome://gpucrash/","chrome://gpuhang/","chrome://memory-exhaust/","chrome://ppapiflashcrash/","chrome://ppapiflashhang/","chrome://inducebrowserheapcorruption/","chrome://heapcorruptioncrash/","chrome://quit/","chrome://restart/"]

function renderExceptions(){
    chrome.storage.local.get({exceptionWebsites: []}, function (result) { 
     for(site in result.exceptionWebsites)
        $("#ExceptionContainer").append(renderException(result.exceptionWebsites[site]));
    });
}
function renderException(exceptionSite){
    var $exceptionEntry=$('<div class="exception-entry"><span class="link-for-exception">'+exceptionSite+'</span><span class="delete-exception"><svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 17 17"><g fill="none" fill-rule="evenodd" stroke="#EC747E" transform="translate(1 1)"><circle cx="7.5" cy="7.5" r="7.5" fill="none"/><path stroke-linecap="square" d="M4.5 4.44l6 6.06M10.5 4.44l-6 6.06"/></g></svg></span></div>')
    $exceptionEntry.find('.delete-exception').click(function(e){

        chrome.storage.local.get({exceptionWebsites: []}, function (result) { 
            var exceptionWebsites = result.exceptionWebsites;
            var index =exceptionWebsites.indexOf(exceptionSite);
            if(index>-1){   
                exceptionWebsites.splice(index, 1); 
                chrome.storage.local.set({exceptionWebsites: exceptionWebsites}, function () { });
            }
            $exceptionEntry.hide();  
        });
    });
    return $exceptionEntry;
}

renderExceptions(); 


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
$('#settings-icon').click(function(e){
    var oldId;
    chrome.storage.local.get('UserId', function (result) { 
        oldId = result.UserId;
        
        var UserId;

        if(oldId)
            UserId = prompt("Enter your SAP UserId",oldId);
        else
            UserId = prompt("Enter your SAP UserId");
        chrome.storage.local.set({UserId: UserId}, function () {  
        });
    });
    
});

$('#AddExceptionButton').click(function(){  
    chrome.tabs.getSelected(null, function(tab) { 
        tabUrl = tab.url; 
        
        if(chromeUrls.indexOf("chrome://"+extractHostname(tabUrl))==-1){ 

            chrome.storage.local.get({exceptionWebsites: []}, function (result) { 
                var exceptionWebsites = result.exceptionWebsites;
                if(exceptionWebsites.indexOf(extractHostname(tabUrl))==-1){ 
                    exceptionWebsites.push(extractHostname(tabUrl)); 
                    chrome.storage.local.set({exceptionWebsites: exceptionWebsites}, function () { 
                        $("#ExceptionContainer").append(renderException(exceptionWebsites[exceptionWebsites.length-1]));
                    });
                }        
                else{
                    $("#error-container").html("Exception Already Exists!"); 
                    $("#error-container").show();
                    setTimeout(function() { $("#error-container").hide(); }, 5000);
                    return;
                }
                    
                
            });
        }
        else {
            $("#error-container").html("You cannot add this URL to exception List as chrome:// urls are already ignored."); 
                    $("#error-container").show();
                    setTimeout(function() { $("#error-container").hide(); }, 5000);
                }
    });

});

chrome.storage.sync.get('IsSAPConnectActive', function(data) { 
    var lc_switch = $('#switch').lc_switch('switch'); 
    lc_switch.hide(); 
    $('#switch').prop('checked', data.IsSAPConnectActive);  
    if(data.IsSAPConnectActive){ 
        $('#switch').lcs_on();  
    }
    else{ 
        $('#switch').lcs_off();  
    }
    lc_switch.show();
  });


  $('body').delegate('', 'lcs-statuschange', function(e) {  

    if(e.target.matches("#switch")){ 
        $("#switch").attr("checked", !$("#switch").attr("checked")); 
    }

    chrome.storage.sync.set({IsSAPConnectActive: ($("#switch").attr("checked")!=undefined)}, function() {  
    }) 
});
 