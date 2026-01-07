# Lab 9: Secure and Monitor Your CI/CD Pipeline with GitHub Actions

## Lab Overview

In this lab, you will secure and monitor CI/CD pipelines using GitHub Actions. You'll learn to manage secrets safely, implement manual approvals, eliminate security risks, and optimize performance with caching and triggers.

## Learning Objectives

In this lab, you will:
- Apply secrets securely using GitHub Secrets
- Use .env files for non-sensitive configuration management
- Set up manual approval workflows for production deployments
- Identify and eliminate hardcoded security risks
- Monitor and interpret GitHub Actions logs
- Implement caching and optimized job triggers

## Estimated Completion Time
50 minutes

## Project Structure

```
lab9/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Main CI pipeline with security scans
│       ├── deploy.yml                # Deployment workflow with manual approval
│       ├── performance.yml           # Performance monitoring
│       └── security-monitoring.yml   # Automated security scanning
├── app.py                            # Flask application
├── test_app.py                       # Pytest tests with security checks
├── Dockerfile                        # Container image definition
├── requirements.txt                  # Python dependencies
├── .env                              # Environment variables (gitignored)
├── .env.example                      # Template for environment variables
├── .gitignore                        # Git ignore patterns
├── SECURITY.md                       # Security policy and best practices
└── README.md                         # This file
```

## Background Knowledge

Before starting the lab, review these concepts used throughout:

### 1. Manual Approval Checkpoints
- GitHub Actions supports environment protection rules
- Production deployments can be paused until authorized reviewer approves
- Prevents accidental or unauthorized pushes to production

### 2. Slack Notifications via Secrets
- Deployment results sent to Slack channels using incoming webhooks
- Webhook URL stored securely in GitHub Secrets
- Referenced inside workflows for notifications

### 3. Semgrep Scans
- Static analysis tool scanning source code for security issues
- Runs alongside Bandit and Safety for broader coverage
- Detects coding style violations and security vulnerabilities

### 4. Docker Multi-Platform Builds
- Docker Buildx allows building images for multiple architectures
- Supports both amd64 and arm64 platforms
- Ensures containers work on cloud servers and devices like Raspberry Pi

### 5. Caching with actions/cache
- GitHub Actions caches dependencies to speed up builds
- Caches restored on future runs if key matches
- Significantly reduces build time for pip packages and Docker layers

## Application Files

### Flask Application (app.py)
Simple Flask web application with:
- `GET /` - Home endpoint returning app info and environment details
- `GET /health` - Health check endpoint for monitoring

### Tests (test_app.py)
Comprehensive test suite including:
- Endpoint functionality tests
- Security header validation
- Sensitive data exposure checks
- Pattern matching for forbidden strings (password, secret, token, key)

### Dockerfile
Production-ready container:
- Python 3.11-slim base image
- Gunicorn WSGI server
- Minimal attack surface
- Optimized for security and performance

## Configuration Files

### .env.example
Template showing required environment variables:
```
ENVIRONMENT=development
APP_VERSION=1.0.0
PORT=5000
LOG_LEVEL=INFO
DEBUG=true
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
API_TIMEOUT=30
CACHE_TTL=300
```

### .env
Actual environment configuration (gitignored):
- Contains development settings
- Never committed to version control
- Use for local testing only

## GitHub Actions Workflows

### 1. CI Pipeline (ci.yml)
**Triggers:**
- Push to main or develop branches
- Pull requests to main

**Features:**
- Python setup with pip caching
- Dependency installation
- Security scanning with Bandit and Safety
- Automated testing with coverage
- Test results artifact upload

**Security Scans:**
- **Bandit**: Python security linter detecting common security issues
- **Safety**: Checks for known vulnerabilities in dependencies
- Reports saved as JSON artifacts

### 2. Deploy Workflow (deploy.yml)
**Triggers:**
- Manual workflow dispatch
- CI pipeline completion

**Features:**
- Manual approval for production (environment protection)
- Multi-stage deployment (staging → production)
- Docker multi-platform builds (amd64, arm64)
- Slack notifications on success/failure
- Deployment verification with health checks

**Environments:**
- **staging**: Automatic deployment after CI passes
- **production**: Requires manual approval from authorized users

### 3. Performance Workflow (performance.yml)
**Features:**
- Scheduled performance monitoring
- Load testing capabilities
- Response time tracking
- Resource usage monitoring
- Performance regression detection

### 4. Security Monitoring (security-monitoring.yml)
**Features:**
- Scheduled security scans (daily)
- Dependency vulnerability checks
- Code security analysis
- Security report generation
- Automated issue creation for vulnerabilities

## Setup Instructions

### Prerequisites
- GitHub account
- Git installed locally
- Python 3.11+
- Docker (optional, for container testing)
- Code editor (VS Code recommended)

### Local Setup

1. **Create GitHub repository:**
   ```bash
   # Repository name: secure-cicd-lab
   # Description: Lab 9: Secure CI/CD Pipeline with GitHub Actions
   # Set to Public
   # Add README file
   ```

2. **Clone and setup local project:**
   ```bash
   mkdir Lab9
   cd Lab9
   git init
   git remote add origin https://github.com/YOUR_USERNAME/secure-cicd-lab.git
   git branch -M main
   git pull origin main
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Run tests locally:**
   ```bash
   pytest -v --cov=. --cov-report=html
   ```

6. **Run the application:**
   ```bash
   python app.py
   # Visit http://localhost:5000
   ```

7. **Test with Docker (optional):**
   ```bash
   docker build -t secure-cicd-lab:local .
   docker run -p 5000:5000 --env-file .env secure-cicd-lab:local
   ```

### GitHub Configuration

#### 1. Setup GitHub Secrets

Go to: Repository → Settings → Secrets and variables → Actions

Add these secrets:

**Required:**
- `DOCKER_USERNAME` - Docker Hub username (for image publishing)
- `DOCKER_PASSWORD` - Docker Hub password or access token

**Optional:**
- `SLACK_WEBHOOK` - Slack webhook URL for notifications
- `DATABASE_URL` - Production database connection string
- `API_KEY` - External API credentials
- `SECRET_KEY` - Flask secret key for production

#### 2. Setup Environment Protection

Go to: Repository → Settings → Environments

**Create Production Environment:**
1. Click "New environment"
2. Name: `production`
3. Add protection rules:
   - ✅ Required reviewers (add your username or team)
   - ✅ Wait timer: 5 minutes (optional)
   - Deployment branches: Only main branch

**Create Staging Environment:**
1. Click "New environment"
2. Name: `staging`
3. No protection rules needed (auto-deploy)

#### 3. Enable GitHub Actions

- Go to Actions tab
- Enable workflows if prompted
- Workflows will run automatically on push

## Security Best Practices

### 1. Secrets Management
✅ **DO:**
- Use GitHub Secrets for sensitive values
- Rotate credentials regularly
- Use `.env.example` for documentation
- Keep `.env` in `.gitignore`

❌ **DON'T:**
- Commit secrets to Git
- Hardcode passwords or API keys
- Share secrets in pull requests
- Log sensitive information

### 2. Dependency Management
✅ **DO:**
- Run `safety check` before releases
- Monitor for vulnerabilities
- Update dependencies promptly
- Pin versions in production

❌ **DON'T:**
- Use unverified packages
- Ignore security warnings
- Use outdated dependencies
- Skip dependency audits

### 3. Code Security
✅ **DO:**
- Run Bandit for Python security
- Use Semgrep for pattern scanning
- Conduct security-focused code reviews
- Implement input validation

❌ **DON'T:**
- Ignore security warnings
- Use eval() or exec() on user input
- Skip security scans
- Trust user input without validation

### 4. Deployment Security
✅ **DO:**
- Require manual approval for production
- Use least-privilege service accounts
- Enable audit logging
- Implement rate limiting

❌ **DON'T:**
- Auto-deploy to production without review
- Use admin credentials for deployments
- Skip approval gates
- Disable security features

## Automated Security Checks

This project implements multiple security layers:

### Static Analysis
- **Bandit**: Scans Python code for security issues
  - SQL injection patterns
  - Hardcoded passwords
  - Unsafe function usage
  - Cryptographic weaknesses

- **Safety**: Checks dependencies for known vulnerabilities
  - CVE database matching
  - Security advisories
  - Outdated package detection

- **Semgrep**: Pattern-based security scanning
  - Custom security rules
  - Best practice enforcement
  - Framework-specific checks

### GitHub Features
- **Secret Scanning**: Detects accidentally committed secrets
- **Dependabot**: Automated dependency updates
- **Code Scanning**: Advanced security analysis

## Monitoring and Logging

### Workflow Monitoring
- View logs in Actions tab
- Check for security scan results
- Review test coverage reports
- Monitor deployment status

### Artifacts
After each workflow run, download:
- `test-results`: Test reports and coverage
- `security-reports`: Bandit and Safety JSON reports
- `build-logs`: Docker build outputs

### Notifications
- Slack messages for deployment status
- GitHub notifications for workflow failures
- Email alerts for security issues (if configured)

## Testing

### Run All Tests
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Run Security Tests Only
```bash
pytest -v -k security
```

### Run Security Scans Locally
```bash
# Install tools
pip install bandit safety

# Run Bandit
bandit -r . -f json -o bandit-report.json

# Run Safety
safety check --json > safety-report.json
```

## Troubleshooting

### Common Issues

**1. Workflow fails with "secrets not found"**
- Solution: Add required secrets in GitHub repository settings
- Check: Settings → Secrets and variables → Actions

**2. Manual approval not triggering**
- Solution: Configure production environment with required reviewers
- Check: Settings → Environments → production

**3. Docker build fails**
- Solution: Check Dockerfile syntax and dependencies
- Verify: requirements.txt includes all needed packages

**4. Tests fail locally but pass in CI**
- Solution: Check Python version compatibility
- Ensure: Using Python 3.11+ consistently

**5. Slack notifications not working**
- Solution: Verify SLACK_WEBHOOK secret is set correctly
- Test: Send test message using curl with webhook URL

### Debug Mode

Enable debug logging in workflows:
```yaml
env:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

## Performance Optimization

### Caching Strategy
- Pip dependencies cached based on requirements.txt hash
- Docker layers cached for faster builds
- Test results cached between runs

### Parallel Execution
- Security scans run in parallel
- Multi-platform Docker builds use parallel workers
- Matrix testing for multiple Python versions (if configured)

## CI/CD Pipeline Flow

```
1. Developer pushes code to branch
   ↓
2. CI workflow triggered
   ↓
3. Security scans run (Bandit, Safety)
   ↓
4. Tests execute with coverage
   ↓
5. If main branch: Deploy workflow triggers
   ↓
6. Staging deployment (automatic)
   ↓
7. Manual approval required for production
   ↓
8. Production deployment with health checks
   ↓
9. Slack notification sent
```

## Lab Completion Checklist

- [ ] Created GitHub repository
- [ ] Added all application files
- [ ] Configured GitHub Secrets
- [ ] Setup environment protection for production
- [ ] Pushed code and verified CI workflow runs
- [ ] Security scans completed successfully
- [ ] Tests passed with adequate coverage
- [ ] Triggered manual deployment to staging
- [ ] Approved and deployed to production
- [ ] Verified Slack notifications (if configured)
- [ ] Reviewed security scan results
- [ ] Downloaded and examined artifacts

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Environment Protection Rules](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Security Policy

See [SECURITY.md](SECURITY.md) for detailed security policies and vulnerability reporting procedures.

## License

This project is for educational purposes as part of the DevOps training course.

## Author

Created for Lab 9: Secure and Monitor Your CI/CD Pipeline with GitHub Actions
