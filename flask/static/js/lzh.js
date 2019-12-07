var loop_time=0;


var sv = document.getElementById('sv_p');
var ws = document.getElementById('ws_p');

var xmlhttp = new XMLHttpRequest();
xmlhttp.timeout = 4000;


xmlhttp.onreadystatechange=state_Change;
xmlhttp.open("GET","/req_data/sv",true);
xmlhttp.send(null);
sv.innerText="changed manually"


function state_Change()
{
    if (xmlhttp.readyState==4)
    {// 4 = "loaded"
	if (xmlhttp.status==200)
	{// 200 = OK
	    if(loop_time==0){ 
		sv.innerText=xmlhttp.responseText;
		xmlhttp.open("GET","/req_data/ws",true);
		xmlhttp.send(null);
		loop_time=1;
	    }else if(loop_time == 1) {
		ws.innerText=xmlhttp.responseText;
		loop_time=2;
	    }else {
		sv.innerText=xmlhttp.responseText;
		//up_h.innerText =xmlhttp.responseText;
	    }
	}
	else
	{
	    if(loop_time==0){ 
		sv.innerText="sv execute fail ...";
	    }else if(loop_time==1) {
		ws.innerText="ws connection down ...";
	    }else {
		sv.innerText="server can not receive memo";
		//up_h.innerText = "server can not receive~";
	    }
	    //alert("Problem retrieving XML data");
	}
    }
}


var pare = document.getElementById('memo_div');
var submit_area = document.getElementById('memo_chk_sta');
var memo_form = document.getElementById('form_memo');

var all_childs = pare.childNodes;
var heads = pare.getElementsByTagName('h4');
var contents = pare.getElementsByTagName('p');
var up_h = document.createElement('h4');
var up_c = document.createElement('p');
var heads_text = [];
for(var i =0 ; i<heads.length ; i++) {
    heads_text.push(heads[i].innerText);
}
var contents_text = [];
for(var i =0 ; i<contents.length ; i++) {
    contents_text.push(contents[i].innerText);
}
    
remove_all_child();

var cur_i =0;
up_h.innerText = heads_text[cur_i];
up_c.innerText = '';

pare.appendChild(up_h);
pare.appendChild(up_c);

//alert(heads[0].innerText);


sv.innerText="sv execute fail ...";

function submit_memo() {
    if(cur_i== heads_text.length-1) {
	form_submit();
	cur_i++;
	if(fail_num.length > 0) {
	    fgot=fail_num[0];
	    update_board(fgot);
	    fail_num.shift()
	}else {
	    up_h.innerText = '';
	    up_c.innerText = '';
	}

    }else if(cur_i > heads_text.length-1) {
	if(fail_num.length > 0) {
	    fail_num.splice(loop_in_fail,1);
	    if(loop_in_fail > fail_num.length-1) {
		loop_in_fail = fail_num.length-1;
	    }
	    fgot=fail_num[loop_in_fail];
	    if(fail_num.length >0 ){
		update_board(fgot);
	    }else {
		up_h.innerText = 'memo complete~';
	    }
	}
    }else {
	++cur_i;
	update_board(cur_i);
    }
}

function update_board(xxx) {
    up_h.innerText = heads_text[xxx];
    up_c.innerText = ' ';
    //pare.innerText='';
}

function remove_all_child() {
    for(var i = all_childs.length -1 ; i>=0; i--){
	pare.removeChild(all_childs[i]) ;
    }
}

function show_memo() {
    if(cur_i < heads_text.length) {
	up_c.innerText = contents_text[cur_i];
    }else {
	up_c.innerText = contents_text[fgot];
    }
}

var fail_num =[];
var fgot=0;
var loop_in_fail=0;
function fail_memo() {
    if(cur_i < heads_text.length-1) {
	fail_num.push(cur_i);
	//alert(cur_i);
	++cur_i;
	update_board(cur_i);
    }else if(cur_i == heads_text.length-1) {
	fail_num.push(cur_i);
	form_submit();
	//alert(cur_i);
	++cur_i;
	fgot = fail_num[0];
	update_board(fgot);
    }else {
	if(fail_num.length > 0) {
	    loop_in_fail=(loop_in_fail+1)%fail_num.length;
	    fgot = fail_num[loop_in_fail];
	    update_board(fgot);
	}
    }
}
	
var exist_fail = false;
function form_submit(){
    submit_area.innerText="";
    for(var i= 0 ;i <heads_text.length; i++){
	exist_fail = false;
	for(var j=0; j < fail_num.length; j++) {
	    if(fail_num[j]==i) {
		exist_fail = true;
	    }
	}
	submit_area.append(heads_text[i]);
	submit_area.rows++;
	if(exist_fail) {
	    submit_area.append("   FORGET\n");
	}else {
	    submit_area.append("   CHECKED\n");
	}
    }
    //memo_form.submit();
    var formData = new FormData(memo_form);
    xmlhttp.open("POST","/",true);
    xmlhttp.send(formData);
}
