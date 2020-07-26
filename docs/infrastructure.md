# Infrastructure


Reference: [GCP developer pro-tips: How to schedule a recurring Python script on GCP](https://cloud.google.com/blog/products/application-development/how-to-schedule-a-recurring-python-script-on-gcp)



## Workflow

```bash
# Setup project on gcloud.
gcloud config set project 'cauvery-calling-284508'
```


### Pub/Sub

> PubSub topic exists purely to connect the two ends of our pipeline: It is an intermediary mechanism for connecting the Cloud Scheduler job and the Cloud Function, which holds the actual Python script that we will run. Essentially, the PubSub topic acts like a telephone line, providing the connection that allows the Cloud Scheduler job to talk, and the Cloud Function to listen.

```bash
# Create a new Pub/Sub topic.
gcloud pubsub topics create 'download-rl-from-ksndmc'

# TEST: Publish a message to the topic.
gcloud pubsub topics publish 'download-rl-from-ksndmc' \
    --message 'Hello, world!' \
    --attribute 'action=download'
```


### Cloud Function

> The Cloud Function subscribes to this topic. This means that it is alerted whenever a new message is published. When it is alerted, it then executes the Python script.

```bash
# Connect function with Pub/Sub topic.
gcloud functions deploy 'download-rl-from-ksndmc' \
    --entry-point 'download_rl_from_ksndmc' \
    --runtime 'python37' \
    --trigger-resource 'download-rl-from-ksndmc' \
    --trigger-event 'google.pubsub.topic.publish'

# TEST: Call function with test data.
gcloud functions call 'download-rl-from-ksndmc' --data='{"message": "Hello, world!"}'
```


### Scheduler

> Cloud Scheduler is a managed Google Cloud Platform (GCP) product that lets you specify a frequency in order to schedule a recurring job. In a nutshell, it is a lightweight managed task scheduler.

```bash
# Schedule message to Pub/Sub.
gcloud scheduler jobs create pubsub 'download-rl-from-ksndmc' \
    --schedule '0 */6 * * *' \
    --topic 'download-rl-from-ksndmc' \
    --message-body 'This is a job that runs every 6 hours.'

# TEST: Trigger the job.
gcloud scheduler jobs run 'download-rl-from-ksndmc'
```
