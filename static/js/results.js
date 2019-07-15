 $('#submit').click( function(e) {
     e.preventDefault();
     console.log("Get JSON");
     $("#loadMe").modal({
         backdrop: "static", //remove ability to close modal with click
         keyboard: false, //remove option to close with keyboard
         show: true //Display loader!
     });
     $.getJSON($SCRIPT_ROOT + '/submit', {
         text: $('textarea[name="text"]').val()
     }, function (data) {  
            $("#loadMe").modal("hide");
         $("#action-td").text(data.result.Action);
         displayBadge(data.result.Action, $("#action-badge"));
         $("#adventure-td").text(data.result.Adventure);
         displayBadge(data.result.Adventure, $("#adventure-badge"));
         $("#comedy-td").text(data.result.Comedy);
         displayBadge(data.result.Comedy, $("#comedy-badge"));
         $("#crime-td").text(data.result.Crime);
         displayBadge(data.result.Crime, $("#crime-badge"));
         $("#family-td").text(data.result.Family);
         displayBadge(data.result.Family, $("#family-badge"));
         $("#mystery-td").text(data.result.Mystery);
         displayBadge(data.result.Mystery, $("#mystery-badge"));
         $("#romance-td").text(data.result.Romance);
         displayBadge(data.result.Romance, $("#romance-badge"));
         $("#thriller-td").text(data.result.Thriller);
         displayBadge(data.result.Thriller, $("#thriller-badge"));
         console.log("Complete");
     });
     return false;
 });

function displayBadge(data, id) {
     if (parseFloat(data) >= 0.5) {
        console.log("display");
         id.css('display', 'inline');
     } else {
         console.log("not display");
        id.css('display', 'none');
     }
}