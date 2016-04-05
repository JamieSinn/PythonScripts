#!/bin/sh
groupadd $1
echo adding $1 user
useradd -g $1 $1
echo adding $1 group
