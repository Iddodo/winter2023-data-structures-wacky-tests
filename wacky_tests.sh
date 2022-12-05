#!/bin/bash

clear

mkdir -p "wacky/in" "wacky/out"

tests_generator_start=1
tests_generator_end=100

for ((i = $tests_generator_start; i <= $tests_generator_end; i++))
do
  python3 wacky_tests.py

  mv wacky.in "wacky/in/input$i.in"
  mv wacky.out "wacky/out/output$i.out"
done
