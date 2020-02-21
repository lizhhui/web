//----------------------------------
// edit article function
//----------------------------------
function edit_text(t){
    if(!t){
	alert(t);
	var org_text = document.getElementById('well_text').innerText;
	document.getElementById('well_text').innerText='';
	var ctext= document.getElementsByName("text_body");
	ctext.innerText =org_text;
    }else {
	var cform=document.getElementsByTagName("form");
	cform.submit;
	
    }

    t = !t;
    if(t){
	document.getElementById('edit_button').innerText='提交';
    }else {
	document.getElementById('edit_button').innerText='编辑';
    }

}

