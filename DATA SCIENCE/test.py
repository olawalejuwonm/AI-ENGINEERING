import os
path = os.path.normpath(r"C:\Users\USER\Documents\Github\Coursera\AI ENGINEERING\DATA SCIENCE\Example1.txt")
with open(path, "r") as file1:
  
    FileContent=file1.readline()
    
    print(FileContent)
