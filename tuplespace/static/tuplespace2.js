


$(initialize);

// initialise app

function initialize() {
    console.log("finished initializing");
}
// event handler for clicks on the button used to retrieve ipso data

function getDataDoClick() {
    console.log("calling service to get data");
    $.ajax({url: 'http://localhost:8080/tuplespace/example', success: updateIpsoPanel, dataType: 'json'})
    
}

// response handler for ajax call to retrieve ipso data

function updateIpsoPanel(payload) {
    console.log("handling ajax response");
    console.log(payload.data[0]);
    var baseid = "ipso-line";
    // todo: insert first line here, then iterate through remaining lines
    // todo: inserting each after the previous one using id to retrieve
    for (i = 0; i < payload.data.length; i++) {
        var nextId = baseid + i.toString();
        $("<div id=nextId align='center'>" + payload.data[i] + "</div>").insertAfter("#ipso-panel");
    }

}
