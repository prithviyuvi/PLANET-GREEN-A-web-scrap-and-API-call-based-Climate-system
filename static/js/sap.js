
function Validate(txt)
{

        if(txt !="SAPLING")
    {
    document.getElementById("status").innerHTML    = "<span class='warning'>Email address is not valid yet.</span>";
    }
    else
    {
    document.getElementById("status").innerHTML	= "<span class='valid'></span>";
    }
}
