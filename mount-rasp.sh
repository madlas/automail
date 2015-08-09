#! /bin/bash  
  
LD_LIBRARY_PATH=/usr/local/lib:/usr/lib  
export LD_LIBRARY_PATH  
  
REMOTE_IP=pi@192.168.200.11
REMOTE_DIR=/home/pi/work  
REMOTE_FS=$REMOTE_IP:$REMOTE_DIR
LOCAL_DIR=./raspberrypi

create() {  
    echo $"Checking mountfs... "      
    mount -l|grep $REMOTE_FS  
        RETVAL=$?  
        echo $RETVAL  
    echo  
    if [ $RETVAL -ne 0 ] ; then  
        echo $"Mounting Remote FS... "  
		#mkdir -p $LOCAL_DIR
		sshfs $REMOTE_FS $LOCAL_DIR 
            RETVAL=$?  
        echo $RETVAL  
        echo  
    fi  
  
    #ulimit -n 102400  
    return $RETVAL  
}  
  
delete() {  
    echo $"Umounting Remote FS... "      
    mount -l|grep $REMOTE_FS  
        RETVAL=$?  
        echo $RETVAL  
    echo  
    if [ $RETVAL -ne 1 ] ; then  
		fusermount -u $LOCAL_DIR
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
