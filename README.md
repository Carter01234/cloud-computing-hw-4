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
    --service-account=homework4-service-account@project-8aeecca0-4f70-4c6b-8e3.iam.gserviceaccount.com \
    --scopes=cloud-platform
```

