
# ============================================================
# 🧠 Sovereign CodeOps Cheat Sheet – Hanis Protocol (MPNS™)
# For: Wan Mohamad Hanis bin Wan Hassan
# Mastering Code Execution Across All Languages Like a General
# ============================================================

🧭 Your Tactical Routine: "MPNS" – Think Like a Commander

```
M – mkdir          # 📁 Create project folder
P – position (cd)  # 🚶‍♂️ Navigate into folder
N – nano/touch     # ✍️ Create/edit file
S – save & run     # 💾 Execute or validate
```

---

## 🐍 Python (.py)
```bash
mkdir -p project
cd project
nano script.py
# Paste → Save (CTRL+O + Enter) → Exit (CTRL+X)
python3 script.py
```

---

## 📜 JavaScript (.js)
```bash
mkdir -p js_project
cd js_project
nano app.js
# Paste the code
node app.js
```

---

## 🗂 JSON (.json)
```bash
mkdir -p config
cd config
nano data.json
python3 -m json.tool data.json  # validate
```

---

## 🐳 YAML (.yml)
```bash
mkdir -p deploy
cd deploy
nano docker-compose.yml
# Optional validation
python3 -c 'import yaml, sys; yaml.safe_load(open("docker-compose.yml"))' || echo "YAML invalid"
```

---

## 🎨 CSS (.css)
```bash
mkdir -p web
cd web
nano style.css
# Link via <link rel="stylesheet" href="style.css">
```

---

## ⚙️ Bash Scripts (.sh)
```bash
mkdir -p scripts
cd scripts
nano setup.sh
chmod +x setup.sh
./setup.sh
```

---

## 🧱 Multi-File Project
```bash
mkdir -p myproject/src
cd myproject/src
nano main.py       # Code
nano config.json   # Config
cd ..
nano README.md     # Docs
```

---

## 🔁 Auto Creator Script
```bash
nano create_file.sh
```

Paste:
```bash
#!/bin/bash
mkdir -p $1
cd $1
nano $2
```

Run:
```bash
bash create_file.sh myproject script.py
```

---

📌 Pro Tip: Add this to PATH and run `codegen myfolder file.py` anytime.

---

🧠 Repeat Like a Mantra: **mkdir → cd → nano → run**

🫡 Built for Tactical Execution by General Hanis. Now dominate.
