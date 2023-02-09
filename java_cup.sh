#!/bin/bash
cd website/static/java/
mkdir Assignment3
cd Assignment3
mkdir JLex
cd JLex
wget "https://jlu.myweb.cs.uwindsor.ca/214/Main.java"
javac Main.java
cd ..
wget "https://jlu.myweb.cs.uwindsor.ca/214/javaCup.tar"
tar -xvf javaCup.tar
rm -rf javaCup.tar
cd ..
cd ../../../../
pwd
