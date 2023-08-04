import os
from tqdm import tqdm

dir = "screenplays"

files = os.listdir(dir)

ultimate = open("ultimate", "a")

toremove = [
    "<b>",
    "</b>",
    "<pre>",
    "</pre>",
    "<html>",
    "</html>",
    "<title>",
    "</title>",
    '<body bgcolor="#ffffff">',
    "<body>",
    "</body>",
    "<script>",
    "</script>",
    "if (window!= top)",
    "top.location.href=location.href",
    "// -->"
]

for file in tqdm(files):
    with open(dir+"/"+file, "r") as movie:
        for line in movie.read().splitlines():
            l = line
            for pattern in toremove:
                l = l.replace(pattern, " ")
            ultimate.write(l+"\n")