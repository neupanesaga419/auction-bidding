

var number = /^[0-9]+$/;
var decimal=  /^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$/;

function floatCheck()
{
    const val = document.getElementById("bidAmount").value;

    var decimal=  /^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$/;
    var number = /^[0-9]+$/;

    if(val.match(number) || val.match(decimal))
    {
        // alert("Correct Input");
    }
    else
    {
        // alert("check value");
        wrong = "Please The value of bid amount must be Number of integer";
        document.getElementById("show").innerHTML = wrong;
        document.getElementById("bidAmount").className = "form-control border-danger";
    }



    console.log(val)
}

function formValidate()
{
    var bid_amount = document.getElementById("bidAmount").value;
    submitOk = "true";
    if(bid_amount.match(number) || bid_amount.match(decimal))
    {

    }
    else
    {

        alert("Please check Bid Amount Field");
        submitOk = "false";
    }
    if(submitOk == "false")
    {

        return false;
    }
    
}
