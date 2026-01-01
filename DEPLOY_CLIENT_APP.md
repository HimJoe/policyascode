# Deploy Policy-to-Code Converter (Client-Facing Web App)

This guide shows you how to deploy the Policy-to-Code Converter so clients can access it via a web link.

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (FREE & EASIEST) ⭐ Recommended

**Pros:** Free, automatic HTTPS, no server management, auto-updates from GitHub
**Perfect for:** Sharing with clients via a simple web link

#### Steps:

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Click "Sign in" and use your GitHub account

2. **Deploy New App**
   - Click "New app" button
   - Repository: `HimJoe/policyascode`
   - Branch: `main`
   - Main file path: `policy_to_code_converter.py`
   - App URL: Choose a custom name (e.g., `policy-converter`)

3. **Click "Deploy!"**
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://[your-name]-policy-converter.streamlit.app`

4. **Share with Clients**
   - Share the URL with your clients
   - They can use it immediately (no installation needed)
   - Works on any device with a browser

**Your Client-Facing URL will be:**
```
https://[your-custom-name].streamlit.app
```

Example:
```
https://himjoe-policy-converter.streamlit.app
```

---

### Option 2: Heroku (Free Tier Available)

**Pros:** Full control, custom domain support
**Requires:** Heroku account

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   cd "/Users/himanshujoshi/Downloads/Policiy as a code"
   heroku create policy-converter
   ```

4. **Create Required Files**

   Create `Procfile`:
   ```
   web: streamlit run policy_to_code_converter.py --server.port=$PORT --server.address=0.0.0.0
   ```

   Create `runtime.txt`:
   ```
   python-3.10.12
   ```

5. **Deploy**
   ```bash
   git add Procfile runtime.txt
   git commit -m "Add Heroku configuration"
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

**Your URL:** `https://policy-converter.herokuapp.com`

---

### Option 3: Google Cloud Run

**Pros:** Scalable, pay-per-use, automatic HTTPS
**Requires:** Google Cloud account

#### Steps:

1. **Build Docker Image**
   ```bash
   cd "/Users/himanshujoshi/Downloads/Policiy as a code"
   docker build -t policy-converter .
   ```

2. **Tag for Google Container Registry**
   ```bash
   docker tag policy-converter gcr.io/YOUR_PROJECT_ID/policy-converter
   ```

3. **Push to GCR**
   ```bash
   docker push gcr.io/YOUR_PROJECT_ID/policy-converter
   ```

4. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy policy-converter \
     --image gcr.io/YOUR_PROJECT_ID/policy-converter \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8501
   ```

**Your URL:** Provided after deployment

---

### Option 4: AWS EC2 (Full Control)

**Pros:** Complete control, custom configurations
**Requires:** AWS account

#### Steps:

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.micro (free tier)
   - Allow port 8501 in security group

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Setup Application**
   ```bash
   # Install dependencies
   sudo apt update
   sudo apt install python3-pip git -y

   # Clone repository
   git clone https://github.com/HimJoe/policyascode.git
   cd policyascode

   # Install requirements
   pip3 install -r requirements.txt

   # Run converter
   nohup streamlit run policy_to_code_converter.py --server.port=8501 --server.address=0.0.0.0 &
   ```

4. **Access**
   ```
   http://your-ec2-ip:8501
   ```

5. **Setup Domain (Optional)**
   - Point your domain to EC2 IP
   - Setup SSL with Let's Encrypt

---

### Option 5: Local Network (Internal Use)

**Pros:** Complete data privacy, no internet required
**Perfect for:** Internal company use, sensitive policies

#### Steps:

1. **Run on Your Machine**
   ```bash
   cd "/Users/himanshujoshi/Downloads/Policiy as a code"
   streamlit run policy_to_code_converter.py --server.address=0.0.0.0
   ```

2. **Get Your IP**
   ```bash
   # macOS/Linux
   ifconfig | grep "inet "

   # Windows
   ipconfig
   ```

3. **Share with Team**
   ```
   http://YOUR_LOCAL_IP:8501
   ```

   Example: `http://192.168.1.100:8501`

---

## 🚀 Quick Deployment (3 Minutes)

### For Immediate Client Access:

1. **Go to:** https://share.streamlit.io
2. **Sign in** with GitHub
3. **New app:**
   - Repo: `HimJoe/policyascode`
   - File: `policy_to_code_converter.py`
4. **Deploy** - Wait 2 minutes
5. **Share** the URL with clients

**Done!** Clients can now access via web browser.

---

## 📋 What Clients Can Do

Once deployed, clients can:

1. ✅ **Upload** their policy documents (PDF, Text, Excel)
2. ✅ **View** extracted rules with filters and search
3. ✅ **Download** Python code for validation
4. ✅ **Download** JSON rules for any system
5. ✅ **Download** complete package with examples
6. ✅ **Integrate** code into their applications

---

## 🔒 Security Considerations

### For Public Deployment (Streamlit Cloud, Heroku, etc.):

**⚠️ Important Notes:**

1. **Data Privacy:**
   - Uploaded policies are processed in-memory
   - No permanent storage by default
   - Data is cleared after session ends

2. **For Sensitive Policies:**
   - Use local deployment (Option 5)
   - Or deploy on private cloud (AWS VPC, etc.)
   - Enable authentication (see below)

3. **Add Authentication** (Optional):

   Add to `policy_to_code_converter.py`:
   ```python
   import streamlit as st

   def check_password():
       def password_entered():
           if st.session_state["password"] == "YOUR_SECRET_PASSWORD":
               st.session_state["password_correct"] = True
               del st.session_state["password"]
           else:
               st.session_state["password_correct"] = False

       if "password_correct" not in st.session_state:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           return False
       elif not st.session_state["password_correct"]:
           st.text_input("Password", type="password", on_change=password_entered, key="password")
           st.error("😕 Password incorrect")
           return False
       else:
           return True

   if not check_password():
       st.stop()
   ```

---

## 🎯 Recommended Setup for Clients

### For External Clients (Easy Access):
```
✅ Deploy to Streamlit Cloud
✅ Share web link
✅ No installation needed
✅ Works on any device
```

### For Enterprise Clients (Security):
```
✅ Deploy on private cloud (AWS/GCP/Azure)
✅ Enable authentication
✅ Custom domain with SSL
✅ Data stays in their infrastructure
```

### For Internal Use (Full Control):
```
✅ Run locally or on company server
✅ No internet required
✅ Complete data privacy
✅ Custom configurations
```

---

## 📊 Usage Tracking (Optional)

To track client usage, add analytics:

```python
# Add to policy_to_code_converter.py
import streamlit as st

# Google Analytics
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
""", unsafe_allow_html=True)
```

---

## 🔧 Customization for Clients

### White-Label the App:

1. **Change Title and Branding**

   In `policy_to_code_converter.py`:
   ```python
   st.set_page_config(
       page_title="Your Company - Policy Converter",
       page_icon="🏢",  # Your logo
   )
   ```

2. **Add Company Logo**
   ```python
   st.image("your_logo.png", width=200)
   ```

3. **Custom Colors**

   Create `.streamlit/config.toml`:
   ```toml
   [theme]
   primaryColor="#your_color"
   backgroundColor="#your_color"
   secondaryBackgroundColor="#your_color"
   textColor="#your_color"
   font="sans serif"
   ```

---

## 📞 Support URLs to Share with Clients

After deployment, share these resources:

1. **App URL:** `https://your-app.streamlit.app`
2. **User Guide:** Link to `CLIENT_GUIDE.md` on GitHub
3. **Example Policies:** Link to `sample_banking_policy.txt`
4. **Support Email:** your-support@email.com
5. **GitHub Repo:** https://github.com/HimJoe/policyascode

---

## ✅ Deployment Checklist

Before sharing with clients:

- [ ] App deployed and accessible
- [ ] Test file upload (PDF, TXT, Excel)
- [ ] Test code download (Python, JSON, ZIP)
- [ ] Review UI and branding
- [ ] Test on different browsers
- [ ] Test on mobile devices
- [ ] Add authentication (if needed)
- [ ] Setup custom domain (if needed)
- [ ] Create user documentation
- [ ] Setup support channel
- [ ] Monitor usage and errors

---

## 🎉 Next Steps

1. **Deploy Now:** Choose Option 1 (Streamlit Cloud) for quickest setup
2. **Test:** Upload a sample policy
3. **Share:** Send URL to clients with `CLIENT_GUIDE.md`
4. **Support:** Monitor usage and provide support
5. **Iterate:** Gather feedback and improve

---

## 🌟 Your Client-Facing App is Ready!

**Recommended Quick Start:**

```bash
# 1. Go to Streamlit Cloud
open https://share.streamlit.io

# 2. Deploy in 3 clicks:
#    - New App
#    - Select: HimJoe/policyascode
#    - File: policy_to_code_converter.py
#    - Deploy!

# 3. Share URL with clients
#    https://[your-name]-policy-converter.streamlit.app
```

**That's it!** Clients can now convert their policies to code via web browser! 🚀
