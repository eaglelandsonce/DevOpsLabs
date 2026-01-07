# Lab 7: Automate Remote Deployment with Ansible Playbooks

## Lab Overview

In this lab, you will explore automating remote deployments using Ansible playbooks. You'll create inventory files, write deployment playbooks, automate service management and file operations, handle errors gracefully, and design modular, reusable automation. By the end of this lab, you'll have a complete Ansible-based deployment system that can manage multiple servers and applications automatically.

## Learning Objectives

In this lab, you will:
- Write basic deployment playbooks with YAML syntax
- Automate service restart and file copying operations
- Handle errors and playbook failures gracefully
- Practice YAML structuring and modular playbook design
- Manage multiple servers with inventory files
- Use Ansible templates for configuration management
- Implement automated monitoring and health checks

## Estimated Completion Time
60 minutes

## Project Structure

```
lab7/
├── inventories/
│   └── development.yml          # Inventory file defining hosts and groups
├── group_vars/
│   └── webservers.yml           # Variables specific to webserver group
├── playbooks/
│   ├── deploy-app.yml           # Main deployment playbook
│   └── templates/
│       ├── app.conf.j2          # Application configuration template
│       └── supervisor-app.conf.j2  # Supervisor process management template
├── Makefile                     # Make commands for easy deployment
├── ansible-deploy.sh            # Deployment wrapper script
└── README.md                    # This file
```

## Prerequisites

- Ubuntu/Debian-based system
- Python 3.x installed
- sudo access
- Basic understanding of YAML syntax
- Familiarity with Linux command line

## Setup Instructions

### 1. Install Ansible and Dependencies

```bash
# Update package list
sudo apt update

# Install Ansible
sudo apt install ansible -y

# Fix Jinja2 compatibility issues
pip3 uninstall jinja2 -y 2>/dev/null || true
pip3 install --user "jinja2==3.0.3"

# Install additional tools for SSH key management
sudo apt install sshpass -y

# Add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Verify installation
ansible --version
```

### 2. Create Project Structure

```bash
cd ~/Desktop
mkdir -p Lab7
cd Lab7
mkdir -p inventories playbooks/templates roles group_vars
```

## Configuration Files

### Inventory File (inventories/development.yml)

Defines the infrastructure with three host groups:

**webservers:**
- `web1`: Primary webserver on port 8080
- `web2`: Secondary webserver on port 8081

**databases:**
- `db1`: PostgreSQL database server

**loadbalancers:**
- `lb1`: Load balancer with round-robin algorithm

**Global Variables:**
- `environment`: development
- `app_directory`: /home/student/deployed-apps
- `app_version`: 1.0.0
- `deploy_user`: student

### Group Variables (group_vars/webservers.yml)

Variables specific to webserver hosts:
- Nginx configuration (port, worker processes)
- Application settings (memory, workers, timeout)
- Monitoring configuration
- Health check endpoints
- Deployment strategy (rolling updates)

### Deployment Playbook (playbooks/deploy-app.yml)

Main playbook that:
1. Updates package cache
2. Creates application directories
3. Installs system packages (Python, Nginx, Supervisor)
4. Creates Flask application
5. Sets up Python virtual environment
6. Installs application dependencies
7. Configures Nginx
8. Configures Supervisor for process management
9. Starts and enables services
10. Performs health checks

### Templates

**app.conf.j2:**
- Application configuration file template
- Uses Jinja2 templating for dynamic values
- Environment-specific settings

**supervisor-app.conf.j2:**
- Supervisor process management configuration
- Auto-restart on failure
- Log file locations
- Environment variables

## Flask Application

The deployment creates a simple Flask application with three endpoints:

### Endpoints

**1. Home Endpoint (`GET /`)**
```
Returns HTML page with:
- Environment name
- Hostname
- Application version
- Port number
```

**2. Health Check (`GET /health`)**
```json
{
  "status": "healthy",
  "environment": "dev",
  "timestamp": "2026-01-07T12:00:00",
  "host": "localhost"
}
```

**3. Version (`GET /version`)**
```json
{
  "app_version": "1.0.0",
  "environment": "dev",
  "port": "8080"
}
```

## Using the Makefile

The Makefile provides convenient commands for deployment and management:

### Deployment Commands

**Check deployment (dry-run):**
```bash
make deploy-check
```

**Deploy to development:**
```bash
make deploy
```

**Deploy to specific environment:**
```bash
make deploy ENV=production
```

### Monitoring Commands

**Check service status:**
```bash
make status
```

**View web1 logs:**
```bash
make logs-web1
```

**View web2 logs:**
```bash
make logs-web2
```

### Cleanup Commands

**Clean up logs and configurations:**
```bash
make clean
```

## Using the Deployment Script

The `ansible-deploy.sh` script provides advanced deployment options:

### Basic Usage

**Deploy to development:**
```bash
./ansible-deploy.sh -e development -p playbooks/deploy-app.yml
```

**Check mode (dry-run):**
```bash
./ansible-deploy.sh -e development -p playbooks/deploy-app.yml -c
```

### Script Options

- `-e <environment>`: Specify environment (default: development)
- `-p <playbook>`: Specify playbook path (default: playbooks/deploy-app.yml)
- `-c`: Check mode only (dry-run, no changes)

### Script Features

1. **Pre-flight checks:**
   - Tests inventory connectivity with ping
   - Validates playbook syntax
   - Reports configuration before execution

2. **Logging:**
   - Timestamps for all operations
   - Clear progress indicators
   - Success/failure notifications

3. **Safety:**
   - Exits on error (set -e)
   - Validates environment before deployment
   - Check mode available for testing

## Running Deployments

### Method 1: Using Make (Recommended)

```bash
# Check deployment (no changes)
make deploy-check

# Deploy application
make deploy

# Check status
make status
```

### Method 2: Using Deployment Script

```bash
# Make script executable
chmod +x ansible-deploy.sh

# Run deployment
./ansible-deploy.sh -e development -p playbooks/deploy-app.yml
```

### Method 3: Direct Ansible Command

```bash
# Run playbook directly
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml

# Check mode
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml --check

# Syntax check
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml --syntax-check
```

## Testing the Deployment

### 1. Verify Services

```bash
# Check Supervisor status
sudo supervisorctl status

# Expected output:
# flask-demo-web1    RUNNING    pid 12345, uptime 0:00:30
# flask-demo-web2    RUNNING    pid 12346, uptime 0:00:30
```

### 2. Test Application Endpoints

**Test web1 (port 8080):**
```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/version
```

**Test web2 (port 8081):**
```bash
curl http://localhost:8081/
curl http://localhost:8081/health
curl http://localhost:8081/version
```

### 3. Check Application Logs

```bash
# View web1 logs
tail -f /home/student/deployed-apps/logs/flask-demo-web1.out.log
tail -f /home/student/deployed-apps/logs/flask-demo-web1.err.log

# View web2 logs
tail -f /home/student/deployed-apps/logs/flask-demo-web2.out.log
tail -f /home/student/deployed-apps/logs/flask-demo-web2.err.log
```

### 4. Check Nginx Status

```bash
# Check Nginx service
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

## Ansible Commands Reference

### Inventory Management

**List all hosts:**
```bash
ansible -i inventories/development.yml all --list-hosts
```

**List specific group:**
```bash
ansible -i inventories/development.yml webservers --list-hosts
```

**Test connectivity:**
```bash
ansible -i inventories/development.yml all -m ping
```

### Ad-hoc Commands

**Check disk space:**
```bash
ansible -i inventories/development.yml all -m shell -a "df -h"
```

**Check memory usage:**
```bash
ansible -i inventories/development.yml all -m shell -a "free -h"
```

**Restart service:**
```bash
ansible -i inventories/development.yml webservers -b -m service -a "name=nginx state=restarted"
```

### Playbook Execution

**Verbose mode (debugging):**
```bash
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml -v
```

**Very verbose:**
```bash
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml -vvv
```

**Step mode (confirm each task):**
```bash
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml --step
```

**Start at specific task:**
```bash
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml --start-at-task="Install Python dependencies"
```

**Tag filtering:**
```bash
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml --tags="deploy,config"
```

## Troubleshooting

### Common Issues

**1. Permission denied errors**
```bash
# Solution: Ensure proper sudo access
sudo visudo
# Add: student ALL=(ALL) NOPASSWD:ALL
```

**2. Port already in use**
```bash
# Check what's using the port
sudo lsof -i :8080

# Kill process if needed
sudo kill -9 <PID>
```

**3. Supervisor fails to start application**
```bash
# Check supervisor logs
sudo tail -f /var/log/supervisor/supervisord.log

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
```

**4. Ansible playbook fails**
```bash
# Run with verbose output
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml -vvv

# Check syntax
ansible-playbook playbooks/deploy-app.yml --syntax-check
```

**5. Python virtual environment issues**
```bash
# Remove and recreate
rm -rf /home/student/deployed-apps/venv
python3 -m venv /home/student/deployed-apps/venv
source /home/student/deployed-apps/venv/bin/activate
pip install -r requirements.txt
```

### Debugging Tips

**1. Check Ansible facts:**
```bash
ansible -i inventories/development.yml all -m setup
```

**2. Test template rendering:**
```bash
ansible -i inventories/development.yml webservers -m template -a "src=playbooks/templates/app.conf.j2 dest=/tmp/test.conf"
cat /tmp/test.conf
```

**3. Validate YAML syntax:**
```bash
python3 -c "import yaml; yaml.safe_load(open('playbooks/deploy-app.yml'))"
```

**4. Check variable precedence:**
```bash
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml -e "debug=true" -v
```

## Best Practices Demonstrated

### 1. **Idempotency**
- Playbook can be run multiple times safely
- Uses `creates` parameter to avoid re-creating resources
- State-based approach (desired state vs current state)

### 2. **Modularity**
- Separate inventory, variables, and playbooks
- Reusable templates with Jinja2
- Group-based variable organization

### 3. **Error Handling**
- Pre-flight checks before deployment
- Syntax validation
- Health checks after deployment
- Graceful failure handling

### 4. **Documentation**
- Clear task names
- Comments in playbooks
- Comprehensive README
- Makefile with helpful targets

### 5. **Automation**
- Shell scripts for common operations
- Makefile for simplified commands
- Automated service management
- Self-healing with Supervisor

### 6. **Security**
- No hardcoded credentials
- Use of become for privilege escalation
- Proper file permissions
- Environment-based configuration

## Advanced Features

### Rolling Deployments

The playbook supports rolling deployments with the `serial` keyword:

```yaml
- name: Deploy Flask Application
  hosts: webservers
  serial: 1  # Deploy to one host at a time
  max_fail_percentage: 20  # Fail if >20% of hosts fail
```

### Health Checks

Automated health checks verify deployment success:

```yaml
- name: Wait for application to be healthy
  uri:
    url: "http://localhost:{{ app_port }}/health"
    status_code: 200
  register: health_check
  retries: 5
  delay: 3
```

### Rollback Strategy

To rollback to previous version:

```bash
# Store current version
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml -e "app_version=1.0.0"

# Deploy new version
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml -e "app_version=2.0.0"

# Rollback if issues
ansible-playbook -i inventories/development.yml playbooks/deploy-app.yml -e "app_version=1.0.0"
```

## Integration with CI/CD

This Ansible setup can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Deploy with Ansible
  run: |
    ansible-playbook -i inventories/production.yml playbooks/deploy-app.yml
```

## Cleanup and Reset

To completely clean up the deployment:

```bash
# Using Makefile
make clean

# Manual cleanup
sudo supervisorctl stop flask-demo-web1 flask-demo-web2
sudo rm -f /etc/supervisor/conf.d/flask-demo*.conf
sudo supervisorctl reread
sudo supervisorctl update
rm -rf /home/student/deployed-apps
```

## Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [Supervisor Documentation](http://supervisord.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## Lab Review Questions

1. What is the purpose of the inventory file in Ansible?
   - Defines hosts, groups, and variables for automation

2. How does Ansible ensure idempotency?
   - Uses state-based approach and checks current state before making changes

3. What is the advantage of using templates with Jinja2?
   - Dynamic configuration based on variables and environment

4. Why use Supervisor for process management?
   - Auto-restart on failure, log management, centralized control

5. What is the purpose of the health check endpoint?
   - Verify application is running and responding correctly

## License

This project is for educational purposes as part of the DevOps training course.

## Author

Created for Lab 7: Automate Remote Deployment with Ansible Playbooks
