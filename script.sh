#!/bin/bash

# Loop to create folders and .gitignore files
for i in {1..8}
do
    folder="TPC$i"
    mkdir "$folder"
    touch "$folder/.gitignore"
done



#terminal script
#for i in {1..8}; do mkdir "TPC$i" && touch "TPC$i/.gitkeep"; done