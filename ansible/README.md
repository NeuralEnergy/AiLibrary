# Neural Energy Infrastructure Deployment

@Author: Neuroplastic Software SRL
@Copyright: Neural Energy SRL


prerequisites:
```bash
pip install ansible kubernetes 
```

If repo issue:

run
```bash
grep -r "download.docker.com" /etc/apt/sources.list.d/
```
get all the files that contain the download.docker.com and remove them
```bash
sudo rm /etc/apt/sources.list.d/docker.list
```