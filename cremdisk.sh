#! /bin/bash  
  
LD_LIBRARY_PATH=/usr/local/lib:/usr/lib  
export LD_LIBRARY_PATH  
  

PRGDIR=/home/pi/work/automail
RAMDIR=/mnt/ramdisk
RECV_BIN=$RAMDIR/recv-bin
SEND_BIN=$RAMDIR/send-bin
RAMDIRNAME=dbf
  
create() {  
    echo $"Checking ramdisk... "      
    mount -l|grep $RAMDIRNAME  
        RETVAL=$?  
        echo $RETVAL  
    echo  
    if [ $RETVAL -ne 0 ] ; then  
        echo $"Mounting ramdisk... "  
        mkdir -p $RAMDIR  
        mount -t tmpfs -o size=100M $RAMDIRNAME $RAMDIR  

	mkdir -p $RECV_BIN $SEND_BIN
	chmod 777 $RECV_BIN $SEND_BIN

	#rm $PRGDIR/recv-bin
	#rm $PRGDIR/send-bin
	#ln -s $RECV_BIN $PRGDIR/recv-bin
	#ln -s $SEND_BIN $PRGDIR/send-bin
	
	
            RETVAL=$?  
        echo $RETVAL  
        echo  
    fi  
  
    ulimit -n 102400  
    return $RETVAL  
}  
  
delete() {  
    echo $"Deleting ramdisk... "      
    mount -l|grep $RAMDIRNAME  
        RETVAL=$?  
        echo $RETVAL  
    echo  
    if [ $RETVAL -ne 1 ] ; then  
        umount -v $RAMDIR  
    fi  
}  
  
case "$1" in  
  mount)  
    create  
    ;;  
  umount)  
    delete  
    ;;  
  
  *)  
    echo $"Usage: $0 {mount|umount}"  
    exit 1  
esac  
