
$('#switch').toggleSwitch(); 
$('.onoffswitch-label[for="switch"]').hide();
chrome.storage.sync.get('IsSAPConnectActive', function(data) {  
    $('#switch').prop('checked', data.IsSAPConnectActive);  
    $('.onoffswitch-label[for="switch"]').show();  
  });


 

$("#switch").change(function() { 
    chrome.storage.sync.set({IsSAPConnectActive: this.checked}, function() { 
        console.log(this.checked);
    }) 
});