# 🌐 WEB DEPLOYMENT GUIDE
## Making Universal Agent a True Web Application

## YES! This Already IS a Web Application! 🎉

Streamlit creates a **real web app** that agents can access through their browsers. Here's how to deploy it:

---

## 🚀 Quick Deploy Options

### Option 1: Company Server (Recommended)

Deploy to your internal server where agents can access it via URL:

```bash
# On your server (Windows/Linux):
streamlit run universal_agent_app.py --server.address 0.0.0.0 --server.port 8501

# Agents access via:
http://your-server-ip:8501
```

**Configuration file** (`~/.streamlit/config.toml`):
```toml
[server]
address = "0.0.0.0"
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
base = "dark"
primaryColor = "#3498db"
```

---

### Option 2: Streamlit Cloud (FREE!)

Deploy for free on Streamlit's cloud:

1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Deploy!

**Agents access via**: `https://your-app.streamlit.app`

**Example `secrets.toml` for Streamlit Cloud:**
```toml
GOOG_API_KEY = "your_gemini_key_here"
```

---

### Option 3: Azure Web App

Deploy to your Microsoft infrastructure:

**Using Azure App Service:**

```bash
# Install Azure CLI
az login

# Create resource group
az group create --name universal-agent-rg --location eastus

# Create App Service plan
az appservice plan create --name universal-agent-plan --resource-group universal-agent-rg --sku B1 --is-linux

# Create web app
az webapp create --name universal-agent-app --resource-group universal-agent-rg --plan universal-agent-plan --runtime "PYTHON:3.11"

# Deploy
az webapp up --name universal-agent-app --resource-group universal-agent-rg
```

**Agents access via**: `https://universal-agent-app.azurewebsites.net`

---

### Option 4: Docker Container

Make it portable and deployable anywhere:

**Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY universal_agent_app.py .
COPY Knowledge_Base/ Knowledge_Base/

# Expose ports
EXPOSE 8501 8765

# Set environment
ENV GOOG_API_KEY=""

# Run app
CMD ["streamlit", "run", "universal_agent_app.py", "--server.address", "0.0.0.0"]
```

**Build and run:**
```bash
# Build
docker build -t universal-agent .

# Run
docker run -p 8501:8501 -p 8765:8765 -e GOOG_API_KEY="your_key" universal-agent

# Agents access via:
http://server-ip:8501
```

---

## 🔐 Adding Authentication

Streamlit doesn't have built-in auth, but you have options:

### Option A: Simple Password Protection

Add to top of `universal_agent_app.py`:

```python
import streamlit as st
import hmac

def check_password():
    """Returns True if the user has correct password."""
    
    def password_entered():
        """Checks whether a password entered by user is correct."""
        if hmac.compare_digest(st.session_state["password"], "your_secure_password"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Show input for password
    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

# Add this at the start of your app
if not check_password():
    st.stop()

# Rest of your app code...
```

### Option B: Azure AD Integration

Use `streamlit-azure-ad` package:

```bash
pip install streamlit-azure-ad
```

```python
from streamlit_azure_ad import get_user_info

user_info = get_user_info()
if user_info:
    st.write(f"Welcome, {user_info['name']}!")
    # Rest of app...
else:
    st.error("Please log in with your Microsoft account")
    st.stop()
```

### Option C: Reverse Proxy with Auth

Use nginx with Azure AD or OAuth:

**nginx config example:**
```nginx
location / {
    auth_request /auth;
    proxy_pass http://localhost:8501;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $host;
}

location /auth {
    proxy_pass http://auth-service:8000;
}
```

---

## 📊 Multi-User Considerations

### Session Isolation (✅ Built-in!)
Streamlit automatically isolates each user's session. Each agent gets their own:
- Session state
- Chat history
- Knowledge stream
- Selected client/agent profile

### Concurrent Users
- **Small team (1-10 agents)**: Single instance works fine
- **Medium team (10-50 agents)**: Use load balancer + multiple instances
- **Large call center (50+ agents)**: Kubernetes deployment

**Load balancing example:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app1:
    image: universal-agent
    environment:
      - GOOG_API_KEY=${GOOG_API_KEY}
  app2:
    image: universal-agent
    environment:
      - GOOG_API_KEY=${GOOG_API_KEY}
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

---

## 🗄️ Shared Knowledge Base

For multiple instances, mount Knowledge_Base from shared storage:

### OneDrive/SharePoint
```python
# In universal_agent_app.py, change:
KB_DIR = "C:/Users/Shared/OneDrive/Universal_Agent_KB"
```

### Network Drive
```python
KB_DIR = "//server/share/Knowledge_Base"
```

### Azure Blob Storage
```python
from azure.storage.blob import BlobServiceClient

def download_kb_from_azure():
    """Download KB from Azure Blob Storage"""
    # Implementation here
```

---

## 📈 Monitoring & Analytics

### Built-in Streamlit Metrics
Streamlit Cloud includes analytics for:
- Active users
- Page views
- Session duration

### Custom Analytics
Add to your app:

```python
import streamlit as st
from datetime import datetime

# Log usage
def log_usage(event_type, details):
    with open("usage_log.csv", "a") as f:
        f.write(f"{datetime.now()},{st.session_state.current_agent},{event_type},{details}\n")

# Call when actions happen:
log_usage("search", query)
log_usage("ai_query", prompt)
log_usage("article_click", article_name)
```

---

## 🔧 Performance Optimization

### For Production Deployment:

1. **Enable Caching:**
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def search_kb(client, query):
    # Your search logic
```

2. **Lazy Load Knowledge Base:**
```python
@st.cache_resource
def load_client_kb(client_name):
    # Load KB files on first access
```

3. **Use Connection Pooling:**
```python
@st.cache_resource
def get_gemini_model():
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash-latest')
```

---

## 🚨 Production Checklist

Before deploying to production:

- [ ] Set strong authentication (Azure AD recommended)
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure backup for Knowledge_Base
- [ ] Test with multiple concurrent users
- [ ] Set up monitoring/alerting
- [ ] Document agent onboarding process
- [ ] Create runbook for common issues
- [ ] Set up automatic restarts (systemd/supervisord)
- [ ] Configure environment variables properly
- [ ] Test KB file serving under load
- [ ] Set rate limits on API calls

---

## 🎯 Recommended Architecture for 50+ Agents

```
Internet
    ↓
Azure Front Door (SSL termination, DDoS protection)
    ↓
Azure Application Gateway (Load balancer, WAF)
    ↓
    ├─→ App Instance 1 (East US)
    ├─→ App Instance 2 (East US)
    └─→ App Instance 3 (West US)
         ↓
    Azure Storage (Knowledge Base files)
         ↓
    Azure Monitor (Logging & Analytics)
```

**Cost estimate**: ~$200-500/month for 50 agents

---

## 💡 Quick Win: Deploy to Streamlit Cloud NOW

Fastest way to make it accessible:

1. **Create GitHub repo:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/universal-agent.git
git push -u origin main
```

2. **Add secrets file** (`.streamlit/secrets.toml`):
```toml
GOOG_API_KEY = "your_key_here"
```

3. **Deploy:**
- Go to https://share.streamlit.io
- Click "New app"
- Connect GitHub repo
- Done! Live in 2 minutes.

4. **Share URL with agents:**
`https://universal-agent-[your-name].streamlit.app`

---

## 🎓 Agent Access Instructions

Once deployed, agents simply:

1. Open browser
2. Navigate to: `http://your-url:8501`
3. (If auth enabled) Log in with credentials
4. Select their profile from sidebar
5. Start working!

**No installation needed. No downloads. Just a URL.** 🎉

---

## 📞 Support & Scaling

Need help deploying? The community can help:
- Streamlit Forums: https://discuss.streamlit.io
- Azure Support: Enterprise support available
- Streamlit Enterprise: White-glove deployment service

**Bottom line**: This is already a web app. You just need to point it at a server instead of localhost!

---

*Next step: Try the Streamlit Cloud deployment - it's free and takes 5 minutes!*
