//----------------------------------
// edit article function
//----------------------------------
var t;
function edit_text(){
    var cform=document.getElementsByTagName("form");
    if(!t){
	var org_text = document.getElementById('well_text').innerText;
	document.getElementById('well_text').innerText='';
	var ctext= document.createElement("textarea");
	ctext.name ="text_body";
	ctext.value =org_text;
	ctext.rows="9";
	cform[0].appendChild(ctext);
    }else {
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

function remove_item(title,addr){
    var temp = document.createElement("form");
    temp.action = addr;
    temp.method = "post";
    temp.style.display = "none";
    var opt = document.createElement("textarea");
    opt.name = "remove";
    opt.value = title;
    temp.appendChild(opt);
    document.body.appendChild(temp);
    temp.submit();
}


