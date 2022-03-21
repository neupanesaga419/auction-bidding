
function checkValue()
{
    let min_amount = document.getElementById('min_bid_amount').innerHTML;
    let given_amount = document.forms["my_form"]["inputValue"].value;
    min_amount= parseFloat(min_amount)
    if(min_amount >= given_amount)
    {
        alert("Your Bidding Amount must be greater than product min amount amount");
        return false;
    }
    
    return console.log(min_amount);

}