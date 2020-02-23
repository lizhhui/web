var loop_time=0;


var sv = document.getElementById('sv_p');
var ws = document.getElementById('ws_p');

var xmlhttp = new XMLHttpRequest();
xmlhttp.timeout = 4000;


//xmlhttp.onreadystatechange=state_Change;
//xmlhttp.open("GET","/req_data/sv",true);
//xmlhttp.send(null);
//sv.innerText="changed manually"


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

sv.innerText="sv execute fail ...";

//==================================
// memory system function
//----------------------------------
// memory curve lin 1-1-1-1-1-1-1-2-2-2-2-3-3-3-10-10-20-30-100-200-300


//----------------------------------
// element
var pare = document.getElementById('memo_div');
var submit_area = document.getElementById('memo_chk_sta');
var memo_form = document.getElementById('form_memo');

var all_childs = pare.childNodes;
var heads = pare.getElementsByTagName('h4');
var contents = pare.getElementsByTagName('p');
var up_h = document.createElement('h4');
var up_c = document.createElement('p');

//----------------------------------
// process item below
var heads_text = [];
var contents_text = [];
var tag_text = [];
//----------------------------------

var ctime=new Date();
var my_time = ctime.toLocaleDateString();
//alert(my_time);
var cur_stage=1;
var memory_curve=[1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 10, 10, 20, 30, 100, 200, 300];


var last_time = "";
var last_stage = "";
for(var i =0 ; i<contents.length ; i++) {
    var q= contents[i].innerText.match(/\*\*\*\*last_time\*\*\*\*.*\*\*\*\*/);
    last_time= q[0].replace(/\*\*\*\*stage\*\*\*\*.*/,"");
    last_time= last_time.replace(/.*\*\*\*\*last_time\*\*\*\*/,"");
    q= contents[i].innerText.match(/\*\*\*\*stage\*\*\*\*.*\*\*\*\*/);
    last_stage= q[0].replace(/.*stage\*\*\*\*\.*/,"");
    last_stage= last_stage.replace(/\*\*\*\*\.*/,"");
    var tag_date = new Date(last_time);
    // caculate dates after
    var during = parseInt((ctime.getTime() - tag_date.getTime())/(1000*24*60*60));
    if((during >= memory_curve[Number(last_stage)])&&  (Number(last_stage)< memory_curve.length) ) {
	//cur_stage = Number(last_stage) + 1;
	//alert(memory_curve[Number(last_stage)]);
	heads_text.push(heads[i].innerText);
	contents_text.push(contents[i].innerText);
	tag_text.push(last_stage);
    }
    //last_time= "--"+last_time +"--";
    //alert(last_stage);
    //break;

}
    
//----------------------------------
// flow
remove_all_child();

var cur_i =0;
up_h.innerText = heads_text[cur_i];
up_c.innerText = '';

pare.appendChild(up_h);
pare.appendChild(up_c);

//alert(heads[0].innerText);


//----------------------------------
// memo botton function
//----------------------------------

function submit_memo() {
    if(cur_i== heads_text.length-1) {
	memo_form_submit();
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

function show_item(kk) {
    up_c.innerText = contents_text[kk];
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
	memo_form_submit();
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
function memo_form_submit(){
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
	    submit_area.append("   FORGET ****last_time****"+my_time+"****stage****"+eval(Number(tag_text[i])-1)+"****\n");
	}else {
	    submit_area.append("   CHECKED ****last_time****"+my_time+"****stage****"+eval(Number(tag_text[i])+1)+"****\n");
	}
    }
    //memo_form.submit();
    var formData = new FormData(memo_form);
    xmlhttp.open("POST","/memo/",true);
    xmlhttp.send(formData);
}

//----------------------------------
// todo botton function
//----------------------------------


function finish_item(title,addr){
    //=======================
    // 同步提交方式,刷新页面
    var temp = document.createElement("form");
    temp.action = addr;
    temp.method = "post";
    temp.style.display = "none";
    var opt = document.createElement("textarea");
    opt.name = "finish";
    opt.value = title;
    temp.appendChild(opt);
    document.body.appendChild(temp);
    temp.submit();
    //=======================
    // 异步提交方式,不刷新页面
    //alert(title);
    //var formData = new FormData();
    //formData.append("finish",title);
    //xmlhttp.open("POST",addr ,true);
    //xmlhttp.send(formData);
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

function pullback_item(title,addr){
    var temp = document.createElement("form");
    temp.action = addr;
    temp.method = "post";
    temp.style.display = "none";
    var opt = document.createElement("textarea");
    opt.name = "pullback";
    opt.value = title;
    temp.appendChild(opt);
    document.body.appendChild(temp);
    temp.submit();
}


