



function createCheckbox(value)
{
   var $input =$('<input class="text-nicelabel"  type="checkbox" value="'+value+'"  data-nicelabel=\'{"checked_text": "'+value+'", "unchecked_text": "'+value+'"}\'/>')  ;

   return $input;
}
function createExpTags(){
    var arrayExp=[
    "javascript","java","c#","php","android","python","jquery","html","c++","ios","css","mysql","sql","asp.net","ruby-on-rails","c","objective-c","arrays",".net","r","node.js","angularjs"
    ];

    for(var i in arrayExp){
        $('#expertise-checkbox-container').append(createCheckbox(arrayExp[i]))
    }
}
function createInterestTags(){
    var arrayInterests=[
        "javascript","java","c#","php","android","python","jquery","html","c++","ios","css","mysql","sql","asp.net","ruby-on-rails","c","objective-c","arrays",".net","r","node.js","angularjs"
    ];

    for(var i in arrayInterests){
        $('#interest-checkbox-container').append(createCheckbox(arrayInterests[i]))
    }
}
createExpTags();
createInterestTags();
$('input.text-nicelabel').nicelabel({uselabel: true});


function getUser(userId){
    var settings = {
    "dataType": "json",
      "async": true,
      "crossDomain": true,
      "url": "/profile_json/"+userId,
      "method": "GET"
    };
    $.ajax(settings).done(function (response) {
      console.log(response);
    });
}
getUsername("i867355");

