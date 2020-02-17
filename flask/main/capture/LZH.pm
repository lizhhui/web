package LZH;

sub dp{
    print "@_";
    print "\n";
}

sub p_log{
    ($file,$txt)=@_;
    if( -e $file) { 
	open(FILE,">>$file") or print "Waring,add $file failed \n"; 
    }else{
	open(FILE,">$file") or print "Waring,create $file failed \n"; 
    }
    print FILE "$txt\n";
    close(FILE);
}

1;
