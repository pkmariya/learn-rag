# Deploying "Ask Mariya's Wiki" to Google Cloud Run

This is a small Python (Flask) app: it answers questions by keyword-searching
`wiki/*.md` content — no LLM, no external AI. If nothing scores above a
relevance threshold it says "I don't know" and offers a feedback form; any
submission opens a GitHub Issue on this repo (never auto-written into the
wiki) so you can review it before adding it to `wiki/*.md`.

It's built from the repo root `Dockerfile` and deployed to Cloud Run
automatically by `.github/workflows/deploy.yml` on every push to `main`.

## One-time GCP setup (do this once, from Google Cloud Shell — no local install needed)

Open https://console.cloud.google.com, click the Cloud Shell icon (`>_`) top right, and run:

```bash
# 1. Set your project (replace with your actual project ID, no quotes)
export PROJECT_ID=YOUR_PROJECT_ID
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com iam.googleapis.com

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
  --member="serviceAccount:$SA_EMAIL" --role="roles/artifactregistry.admin"

# 5. Create and download a JSON key for that service account
gcloud iam service-accounts keys create gh-deployer-key.json \
  --iam-account=$SA_EMAIL

# 6. Print the key so you can copy it (or use the Cloud Shell file download button)
cat gh-deployer-key.json
```

(Already done if you set this up previously — skip to the feedback token step below.)

## New: GitHub token for the feedback feature

The app itself (running on Cloud Run) needs a **separate, narrowly-scoped**
token to open GitHub Issues when a visitor submits feedback on an unanswered
question. This is different from the deploy service account above.

1. Go to `github.com/settings/personal-access-tokens/new`.
2. Resource owner: your account. Repository access: only `pkmariya/learn-rag`.
3. Under **Repository permissions**, set **Issues** to **Read and write**. Leave everything else as-is (it does not need Contents access).
4. Generate the token and copy it.

## Add GitHub repo secrets

Go to `github.com/pkmariya/learn-rag` → **Settings → Secrets and variables → Actions → New repository secret**, and add:

- `GCP_PROJECT_ID` — your GCP project ID (e.g. `my-project-123456`)
- `GCP_SA_KEY` — the full contents of `gh-deployer-key.json` from step 6 above
- `WIKI_FEEDBACK_GH_TOKEN` — the new Issues-scoped token from the previous section

## Trigger the deploy

Once secrets are set, the workflow runs automatically on the next push to `main`.
You can also trigger it manually from **Actions → Deploy to Cloud Run → Run workflow**.

Check progress under the **Actions** tab. The last step of the run prints the
public Cloud Run URL, e.g.:

```
https://learn-rag-wiki-xxxxxxxxxx.us-central1.run.app
```

That's the link to share. Cloud Run scales to zero when idle, so an
occasionally-viewed personal wiki costs effectively nothing.

## Reviewing feedback

Visitor-submitted "I don't know" feedback shows up as a GitHub Issue labeled
`wiki-feedback` on `pkmariya/learn-rag`, containing the question asked and
whatever the visitor typed. Nothing is written into `wiki/*.md`
automatically — review the issue, and if it checks out, add it to the
relevant wiki page yourself (or ask Claude to do it) following the normal
ingest workflow in `CLAUDE.md`.

## Updating the wiki later

Just edit `wiki/*.md` and push to `main` — the app re-reads the wiki content
on each new deploy, no separate build step required.

## Running locally

```bash
cd app
pip install -r requirements.txt
PORT=8080 python3 app.py
```
