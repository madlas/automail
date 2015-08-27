#!/bin/bash
## 获取当前的进程号
pid=$$
 
## 获取当前的脚本文件名
name=`basename $0`
 
## 检测进程内是否有此进程号，并且此进程号的运行程序为当前脚本名，如果有则kill此进程
ps -ef|awk -v p=$pid -v n=$name '$2!=p && $NF~n{system("kill "p)}'

python ./main_imap.py >> /mnt/ramdisk/automail.log
#sleep 10
