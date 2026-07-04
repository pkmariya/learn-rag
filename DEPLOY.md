# Deploying the Learn-RAG wiki UI to Google Cloud Run

The `site/` folder is a static, generated website (nginx + Dockerfile included).
Regenerate it any time the wiki changes with:

```
python3 build.py .
```

## One-time deploy (run from your own machine, where `gcloud` is installed and authenticated)

```bash
# 1. Authenticate (opens a browser)
gcloud auth login

# 2. Set your project (replace with your actual project ID)
gcloud config set project YOUR_PROJECT_ID

# 3. Enable required APIs (one-time per project)
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 4. Build + deploy straight from the site/ folder (contains its own Dockerfile)
gcloud run deploy learn-rag-wiki \
  --source=./site \
  --region=us-central1 \
  --allow-unauthenticated \
  --platform=managed

# 5. gcloud will print a Service URL like:
#    https://learn-rag-wiki-xxxxxxxxxx.us-central1.run.app
# That's the public link to share.
```

## Redeploying after wiki updates

```bash
python3 build.py .          # regenerate site/ from wiki/*.md
gcloud run deploy learn-rag-wiki --source=./site --region=us-central1 --allow-unauthenticated
```

Cloud Run only bills for actual requests (scales to zero when idle), so an
occasionally-viewed personal wiki costs effectively nothing.
