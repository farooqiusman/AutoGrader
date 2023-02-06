#!/bin/bash
cd website/static/java/Assignment3/
wget "https://jlu.myweb.cs.uwindsor.ca/214/javaCup.tar"
tar -xvf javaCup.tar
cd JLex
javac Main.java
cd ..
cd ../../../../
pwd
