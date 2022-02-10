```text
ssh -i ~/.ssh/lms ubuntu@3.20.44.23
```

```text
sudo systemctl restart lms_gunicorn.service
```

```text
sudo systemctl status lms_gunicorn.service -n 150
```