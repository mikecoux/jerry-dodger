#!/bin/bash
echo "Welcome to Jerry Dodger!"
read -n1 -p "Would you like to start? (y/n) : " user_input

case $user_input in  
  y|Y)
    cd lib
    pipenv install
    pipenv run python3 main.py
    ;; 
  n|N)
    echo no
    ;; 
  *)
    echo dont know ;; 
esac