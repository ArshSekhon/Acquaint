



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
      $("#onboardin-card-4 .onboardin-heading").html("Thanks "+response["first_name"]+"!");
    });
}

function transitionFrom1To2(){
    $('#onboardin-card-1').fadeOut(500, function () {
       setTimeout( function () {
            $('#onboardin-card-2').fadeIn(500, function () {
                     $('#onboardin-card-1').hide()
            });
            },200);

    });

    getUser($("#onboardin-card-1 .onboarding-answer-text").val());
}
function transitionFrom2To3(){
    $('#onboardin-card-2').fadeOut(500, function () {
       setTimeout( function () {
            $('#onboardin-card-3').fadeIn(500, function () {
                     $('#onboardin-card-2').hide()
            });
        },200);
    });
}
function transitionFrom3To4(){
    $('#onboardin-card-3').fadeOut(500, function () {
       setTimeout( function () {
            $('#onboardin-card-4').fadeIn(500, function () {
                 $('#onboardin-card-3').hide()
        });
       },200);
    });

    var userInfo={
        username:"",
        expertise:[],
        interests:[]
    };

    userInfo.username = $("#onboardin-card-1 .onboarding-answer-text").val();

    var checkedValuesExpertise = $('#onboardin-card-2 input:checkbox:checked').map(function() {
        return this.value;
    }).get();
    var interests = $('#onboardin-card-3 input:checkbox:checked').map(function() {
        return this.value;
    }).get();
    userInfo.expertise=checkedValuesExpertise.concat($('#onboardin-card-2 .onboarding-answer-text').val().split(','))
    userInfo.interests=interests.concat($('#onboardin-card-3 .onboarding-answer-text').val().split(','))

    //add API call here


}
 $('#onboardin-card-1 .next-btn').click(()=>{transitionFrom1To2()});
 $('#onboardin-card-2 .next-btn').click(()=>{transitionFrom2To3()});
 $('#onboardin-card-3 .next-btn').click(()=>{transitionFrom3To4()});