# Longhorn PV Backup

## 1. Generate the backup folder in S3

Run the following command to generate a backup folder in S3:

```
aws --endpoint-url=https://s3.<url>:443 s3api put-object --bucket <bucket-name> --key <folder-name>/
```

**Note:** If you have more than one S3 configured in your credentials (`./aws/credentials`), specify the profile like this:

```
aws --profile <profile-name> --endpoint-url=https://s3.<url>:443 s3api put-object --bucket <bucket-name> --key <folder-name>/
```

## 2. Generate a Longhorn-System AWS Secret

Create the Longhorn AWS secret using this command:

```
kubectl create secret generic aws-secret \
  --from-literal=AWS_ACCESS_KEY_ID=<value> \
  --from-literal=AWS_SECRET_ACCESS_KEY=<value> \
  --from-literal=AWS_ENDPOINTS=<url-for-s3:443> \
  -n longhorn-system
```

## 3. Configure Longhorn UI for Backups

In the Longhorn UI:

1. Go to `Settings -> General`.
2. Scroll down to the **Backups** section.
3. In the **Backup Target** field, enter:

   ```
   s3://<url-for-s3>@us-east-1/<backup-folder-in-s3>/
   ```

4. In the **Backup Target Credential Secret** field, enter the name of the secret you generated (`aws-secret`).

### Generate manual backup
To manually backup, look for the volume you need under the `Volumes` section in Longhorn UI, tick the box and choose `backup` hich will run the process.


### Confirm the backup  

```
aws --endpoint-url=https://<s3-url>:443 s3 ls s3://<bucket>/<folder> --recursive
```
NOTE! When you have more then one S3 configured add `--profile <profile-name>`

```
aws --profile <profile-name> --endpoint-url=https://<s3-url>:443 s3 ls s3://<bucket>/<folder> --recursive
```
