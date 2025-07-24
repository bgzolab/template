#!/bin/bash
# way: use bc. means that the pi's arctan(y); when y=1,
# x=arctan(y)=pi/4. and more bc see(zh): https://wangchujiang.com/linux-command/c/bc.html
echo 'scale=100; 4*a(1)' | bc -l