//----------------------------------
// edit article function
//----------------------------------
var t;
function edit_text(){
    if(!t){
	var org_text = document.getElementById('well_text').innerText;
	document.getElementById('well_text').innerText='';
	var ctext= document.getElementsByName("text_body");
	ctext[0].innerText =org_text;
    }else {
	var cform=document.getElementsByTagName("form");
	cform[0].submit();
	
    }

    //alert(t);
    t = !t;
    if(t){
	document.getElementById('edit_button').innerText='提交';
    }else {
	document.getElementById('edit_button').innerText='编辑';
    }

}

