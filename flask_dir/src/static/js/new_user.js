
var arrayExp=[
    "javascript","java","c#","php","android","python","jquery","html","c++","ios","css","mysql","sql","asp.net","ruby-on-rails","c","objective-c","arrays",".net","r","node.js","angularjs"
];
var arrayInterests=[
    "javascript","java","c#","php","android","python","jquery","html","c++","ios","css","mysql","sql","asp.net","ruby-on-rails","c","objective-c","arrays",".net","r","node.js","angularjs"
];

function createCheckbox(value)
{
   var $input =$('<input class="text-nicelabel"  type="checkbox" value="'+value+'"  data-nicelabel=\'{"checked_text": "'+value+'", "unchecked_text": "'+value+'"}\'/>')  ;

   return $input;
}
for(var i in arrayExp){
    $('#expertise-checkbox-container').append(createCheckbox(arrayExp[i]))
}
for(var i in arrayInterests){
    $('#interest-checkbox-container').append(createCheckbox(arrayInterests[i]))
}
$('input.text-nicelabel').nicelabel({uselabel: true});