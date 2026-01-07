# Lab 8: Deploy with Ansible (on GitHub Runner) and Host on GitHub Pages

This lab demonstrates:
- Running Ansible directly on a GitHub-hosted runner (localhost, local connection)
- Building a static site with Ansible
- Uploading the built site as an artifact
- Deploying to GitHub Pages

## Structure

```
lab8/
├── ansible/
│   ├── inventory.ini    # localhost with local connection
│   └── site.yml         # Playbook to build static site
└── .github/
    └── workflows/
        └── deploy.yml   # GitHub Actions workflow
```

## Key Concepts

- **Ansible lookup() function**: Dynamically fetch environment variables and run shell commands
- **GitHub Pages deployment**: Upload artifact and deploy with `actions/deploy-pages@v4`
- **SSH key management**: Store SSH private key as GitHub Secret (practice, not used in this local-only lab)
- **Workflow permissions**: `pages: write` and `id-token: write` required for Pages deployment

## Workflow

1. **Build job**:
   - Checkout code
   - Install Ansible
   - Run `ansible-playbook` to generate `./site/index.html`
   - Upload `./site` as artifact

2. **Deploy job**:
   - Download artifact
   - Deploy to GitHub Pages

## Local Testing

```bash
# Run the Ansible playbook locally
SITE_DIR=./site ansible-playbook -i ansible/inventory.ini ansible/site.yml -vv

# Check output
ls -la ./site/
cat ./site/index.html
```

## GitHub Setup

1. Create repository and push code
2. Settings → Pages → Source: GitHub Actions
3. Settings → Secrets → Add `SSH_PRIVATE_KEY` (optional, for practice)
4. Push to trigger workflow
5. View deployed site at: `https://<username>.github.io/<repo>/`
