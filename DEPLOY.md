# Deploying the Learn-RAG wiki UI to Google Cloud Run

The `site/` folder is a static, generated website (nginx + Dockerfile included).
It's rebuilt from `wiki/*.md` automatically by the GitHub Actions workflow at
`.github/workflows/deploy.yml`, then built into a container image from
`site/Dockerfile` and deployed to Cloud Run on every push to `main`.

## One-time setup (do this once, from Google Cloud Shell — no local install needed)

Open https://console.cloud.google.com, click the Cloud Shell icon (`>_`) top right, and run:

```bash
# 1. Set your project (replace with your actual project ID)
export PROJECT_ID=YOUR_PROJECT_ID
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com containerregistry.googleapis.com \
  iam.googleapis.com

# 3. Create a service account for GitHub Actions to deploy with
gcloud iam service-accounts create gh-deployer \
  --display-name="GitHub Actions Cloud Run Deployer"

export SA_EMAIL=gh-deployer@$PROJECT_ID.iam.gserviceaccount.com

# 4. Grant the roles it needs to build + deploy
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" --role="roles/run.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" --role="roles/cloudbuild.builds.editor"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" --role="roles/artifactregistry.writer"

# 5. Create and download a JSON key for that service account
gcloud iam service-accounts keys create gh-deployer-key.json \
  --iam-account=$SA_EMAIL

# 6. Print the key so you can copy it (or use the Cloud Shell file download button)
cat gh-deployer-key.json
```

## Add GitHub repo secrets

Go to `github.com/pkmariya/learn-rag` → **Settings → Secrets and variables → Actions → New repository secret**, and add:

- `GCP_PROJECT_ID` — your GCP project ID (e.g. `my-project-123456`)
- `GCP_SA_KEY` — the full contents of `gh-deployer-key.json` from step 6 above

## Trigger the deploy

Once both secrets are set, the workflow runs automatically on the next push to `main`
(this repo already has one queued). You can also trigger it manually from
**Actions → Deploy to Cloud Run → Run workflow**.

Check progress under the **Actions** tab. The last step of the run prints the
public Cloud Run URL, e.g.:

```
https://learn-rag-wiki-xxxxxxxxxx.us-central1.run.app
```

That's the link to share. Cloud Run scales to zero when idle, so an
occasionally-viewed personal wiki costs effectively nothing.

## Updating the wiki later

Just edit `wiki/*.md` and push to `main` — the workflow rebuilds the site and
redeploys automatically. No manual gcloud commands needed after initial setup.
