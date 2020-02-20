#!/usr/bin/perl
$OO = 0;
#use LZH ;

#        
#           
# 
#                    +-----------+
#                    |           |
#                    |           |----------> to_rem.html
# capture.org ------>|           |
#                    |           |
#                    |           |----------> cap.html
#                    |           |
#                    |           |<---------> current_status.txt
#                    |           |
#                    |           |
#                    |           |
#                    |           |
#                    +-----------+
#                         ^
#                         |
#                         |
#                         |
#                         |
#                         |
#                   check_status.txt
#   
#   
# Describtion:   
#  1. categoary capture.org and everyday(directory) into 3 group:
#    * TODO task
#    * CAP  cap
#    * MEMO memo
#     store the infomations into a 2 stage hash table.
#  2. read(read,close) current_status.txt to update the hash table.
#  3. clean (write,close)check_status.txt
#  4. output(to_rem.html,task.html,cap.html)
#  5. update 1 ,check check_status.txt(read,close) if it's date is newer 
#     than current_status.txt in every 10s and update current_status.txt(write,close)
#   
#   


my $task_flag = 0;
my $cap_flag = 0;
my $memo_flag =0;

my @item_tags;
my $head;
my $time;

my $must_rem;
my @content;

my @to_rem;
my @cpl_rem;
#-----------------
# main routine
#-----------------
&empty_hash;
&get_current_time;
&update_file;
&update_file_from_web("everyday");
&check_current_status;
#&p_tree( 'task');
&output;
#if(&file_is_newer("check_status.txt","current_status.txt")) {
&check_reach_and_record ;
&update_current_status;
&empty_check_status_txt;

#-----------------
# sub function
#-----------------


sub update_file {
    open(FILE,$ARGV[0]) or die "$! not exist";
    while(<FILE>) {
        if($task_flag) {
            &proc_item($_ , 'TODO', 'task' );
        }

        if($cap_flag) {
            &proc_item($_ , "CAP" , 'cap');
        }

        if($memo_flag) {
            &proc_item($_ , "MEMO" , 'memo');
        }
        &match_item($_);
    }
}
sub update_file_from_web {
    $_ = $_[0];
    $task_flag = 0;
    $cap_flag = 0;
    $memo_flag =0;

    opendir(DIR , $_ ) or die "can not open directory :$_";
    pop(@filelist);
    @filelist = readdir DIR;
    closedir(DIR);
    shift(@filelist);
    shift(@filelist);
    LZH::p_log("log.txt", "@filelist")if($OO);
    foreach $web_file (@filelist) {
        open(FILE,"everyday/$web_file") or die "$! not exist";
	LZH::p_log("log.txt", "$web_file")if($OO);
        while(<FILE>) {
            &match_item($_);
            if($task_flag) {
                &proc_item($_ , 'TODO', 'task' );
            }

            if($cap_flag) {
                &proc_item($_ , "CAP" , 'cap');
            }

            if($memo_flag) {
		LZH::p_log("log.txt", "$_")if($OO);
                &proc_item($_ , "MEMO" , 'memo');
            }
        }
        close(FILE);
    }
}

sub match_item {
    $_ = $_[0];
    if(/^\*\ Tasks/ or /^\*\*\ TODO/) {
        $task_flag = 1;
        $cap_flag = 0;
        $memo_flag =0;
    }elsif(/^\*\ Captures/ or /^\*\*\ CAP/) {
        $task_flag = 0;
        $cap_flag = 1;
        $memo_flag =0;
    }elsif(/^\*\ Memos/ or /^\*\*\ MEMO/) {
        $task_flag = 0;
        $cap_flag = 0;
        $memo_flag =1;
    }
}
sub proc_item {
    ($tmp , $cate , $lable)=@_;
    $_ = $tmp;
    $item_on = 0 if(/^\*\*\ /); 
    if(/^\*\*\ $cate\ +(.*)/) {
	$item_on = 1;
        $tmp = $1;
	$must_rem =1 if($lable =~"memo") or $must_rem = 0; 
        @item_tags=&catch_tag($tmp) if(/:/);
        $_ =$tmp;
        s/\s*:.*//;
        $head = $_;
        ${$lable}{$head}{tag}=[@item_tags] ;
        ${$lable}{$head}{rem}= $must_rem;
        $to_rem{$head}{stage} = 0  if($must_rem and !(grep m/$head/ , (keys %to_rem))) ;
        @content = ();
    } elsif(/([0-9]{4}-\d\d-\d\d)[^\d]/) {
        ${$lable}{$head}{time} = $1 if($item_on);
    } elsif($tmp !~/^\s*$/) {
        push @content , $_ if (($tmp !~/^\*/)&&($item_on));
        ${$lable}{$head}{cont}= [@content] if($item_on);
    }
}

sub catch_tag {
    my @tags;
    $_ = $_[0];
    s/.*?://;
    $must_rem = 0 ;
    while($_) {
        s/([a-zA-Z_]*)://;
        $must_rem = 1 if($1 eq "memo");
        push(@tags,$1);
    }
    return @tags;
}


sub p_tree {
    $_ = $_[0];
    foreach $i (keys %{$_}) {
        print "$i\n";
        print ${$_}{$i}{head};
        print "++ @{${$_}{$i}{tag}} \n";
        print ${$_}{$i}{time};
        print "\n @{${$_}{$i}{cont}} \n";
        print ${$_}{$i}{rem};
        print "\n****-\n";
    }
}

sub p_tree_to_file {
    $_ = $_[0];
    my $file = $_[1];
    open(TREEFILE,">$file") or die "can not open $file for write";

    foreach $i (keys %{$_}) {
        print TREEFILE "****${$_}{$i}{time} $i \n";
        #print TREEFILE "++ @{${$_}{$i}{tag}} \n";
        print TREEFILE "@{${$_}{$i}{cont}} \n";
    }
    close(TREEFILE);
}


sub p_rem {
    foreach $i (keys %to_rem) {
        print "$i \n";
        print "next_day: $to_rem{$i}{next_day} \n" ;
        print "stage: $to_rem{$i}{stage} \n";
        print "toggle: $to_rem{$i}{toggle} \n";
    }
}

sub get_current_time {
   ($sec, $min, $hour, $mday, $mon, $year_off, $wday, $yday)= localtime;
}

sub check_reach_and_record {
    my $tmp = $yday;
    print "***** $tmp ******* \n";
    open(IN_CHK , "input/check_status.txt") or print "$! not exist";
    open(HTML , ">output/to_rem.html") or die "$! can't be created";
    open(ARCH , ">output/arch.org") or die "$! can't be created";
    @chk_sta = <IN_CHK>;
    foreach $i (keys %to_rem) {
        if($to_rem{$i}{stage} == 0 ) {
            if(&not_checked($i)) {
                &write_html($i) ;
            }else {
                $to_rem{$i}{next_day} = $tmp+2;
                $to_rem{$i}{stage}++ ;
            }
        }elsif($to_rem{$i}{stage} == 1 ) {
            &check_stage(2);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 2 ) {
            &check_stage(3);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 3 ) {
            &check_stage(5);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 4 ) {
            &check_stage(10);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 5 ) {
            &check_stage(30);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 6 ) {
            &check_stage(100);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 7 ) {
            &check_stage(300);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 8 ) {
            &check_stage(0);
            &write_html($i) if($to_rem{$i}{toggle});

        }elsif($to_rem{$i}{stage} == 9 ) {
            &archieve($i);

        }else{
            print "$i run into wrong stage\n";
        }
    }
    close(IN_CHK);
    close(HTML);
    close(ARCH);
}

sub check_stage {
    my $num = $_[0];
    my $tmp = $yday;
    $to_rem{$i}{toggle} = 1 if($to_rem{$i}{next_day} <= $tmp );
    if($to_rem{$i}{toggle} ) {
        if(!&not_checked($i) ) {
            $to_rem{$i}{toggle} = 0;
            $to_rem{$i}{next_day} =($tmp+$num)%365;
            $to_rem{$i}{stage}++ if($to_rem{$i}{stage} !=9) ;

        }elsif(&forgot_checked($i) ) {
            $to_rem{$i}{toggle} = 1;
            $to_rem{$i}{next_day} =($to_rem{$i}{next_day}+2)%365;
            $to_rem{$i}{stage}--;
        }
    }
}

sub not_checked {
    $t = $_[0];
    $line = grep m/$t.*CHECKED/ , @chk_sta ;
    return 0 if($line) or return 1;
}

sub forgot_checked {
    $t = $_[0];
    $line = grep m/$t.*FORGOT/ , @chk_sta ;
    return 1 if($line) or return 0;
}


sub write_html {
    my $i = $_[0];
    print HTML  "****$i\n";
    print HTML  "     @{$cap{$i}{cont}}\n" ;
}

sub archieve {
    my $i = $_[0];
    print ARCH  "** $i\n";
}

sub empty_hash{
    %task=();
    %cap=();
    %memo=();
}

sub output{
    &p_rem;
    &p_tree_to_file('cap' ,  'output/cap.html' );
    &p_tree_to_file('task' , 'output/task.html' );
}

sub check_current_status{
    open(CS,"current_status.txt") or print "no such current_status.txt";
    @temp=<CS>;
    close(CS);
    foreach $i (keys %to_rem) {
	foreach $j (@temp) {
	    if($j =~ /$i\s*\*\*\*([0-9]+)\s*\*\*\*([0-9]+)/){
		$to_rem{$i}{stage} = $1;
		$to_rem{$i}{next_day} = $2;
	    }
	}
    }
}


sub file_is_newer{
    ($a,$b)=@_;
    $k = (stat "input/$a")[9];
    $j = (stat "$b")[9];
    if($k > $j){
	print "check from website\n";
	return 1;
    }else{
	print "no check from website\n";
	return 0;
    }
}

sub update_current_status{
    open(CS,">current_status.txt") ;
    foreach $i (keys %to_rem) {
        print CS "$i ***$to_rem{$i}{stage}***$to_rem{$i}{next_day}\n";
    }
    close(CS);
}

sub empty_check_status_txt{
    open(IN_CHK , ">input/check_status.txt");
    print IN_CHK "";
    close(IN_CHK);
}
