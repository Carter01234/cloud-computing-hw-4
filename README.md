# Common Commands 


Running the server locally 

```
python3 server.py
```

Creating my VM with my service account. 

```
gcloud compute instances create my-vm \
    --zone=us-central1-a \
    --address=homework4-ip \
    --service-account=web-server-sa@project-8aeecca0-4f70-4c6b-8e3.iam.gserviceaccount.com \
    --scopes=cloud-platform \
    --metadata-from-file=startup-script=startup.sh,file-server-py=file-server/file-server.py
```

Calling my server on the VM.

```
curl http://136.64.134.90:8080
```

SSH into my server in google cloud

```
gcloud compute ssh my-vm --zone=us-central1-a
```

