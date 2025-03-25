# port forwards:
ssh -fN -J granat  quad-6 -L 8000:localhost:8000
ssh -fN -J granat  quad-6 -L 8001:localhost:8001
ssh -fN -J granat  quad-6 -L 9090:localhost:9090

