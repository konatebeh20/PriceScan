# 🚀 INSTALLATION RAPIDE - PRICESCAN-API

## 📋 Prérequis

- **Python 3.8+** installé et dans le PATH
- **Git** pour cloner le projet
- **Accès Internet** pour télécharger les dépendances

## 🖥️ Installation sur Windows

### **Option 1: Installation automatique (Recommandée)**
```cmd
# Double-cliquez sur install_dependencies.bat
# Ou en ligne de commande :
install_dependencies.bat
```

### **Option 2: Installation manuelle**
```cmd
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement
venv\Scripts\activate.bat

# 3. Installer les dépendances
pip install -r requirements.txt
```

## 🐧 Installation sur Linux/Mac

### **Option 1: Installation automatique (Recommandée)**
```bash
# Rendre le script exécutable
chmod +x install_dependencies.sh

# Lancer l'installation
./install_dependencies.sh
```

### **Option 2: Installation manuelle**
```bash
# 1. Créer l'environnement virtuel
python3 -m venv venv

# 2. Activer l'environnement
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Lancement de l'API

### **Windows**
```cmd
# Activer l'environnement
venv\Scripts\activate.bat

# Lancer l'API
python app.py
```

### **Linux/Mac**
```bash
# Activer l'environnement
source venv/bin/activate

# Lancer l'API
python3 app.py
```

## 🌐 Accès à l'API

- **API Base URL**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/health`
- **Documentation**: `http://localhost:5000/apidocs`

## 🔧 Résolution des problèmes

### **Erreur "No module named 'cv2'"**
```bash
pip install opencv-python
```

### **Erreur "No module named 'pytesseract'"**
```bash
pip install pytesseract
```

### **Erreur de politique d'exécution (Windows PowerShell)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problèmes de dépendances**
```bash
# Nettoyer et réinstaller
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 📚 Dépendances principales installées

- **Flask** - Framework web
- **OpenCV** - Traitement d'images
- **Tesseract** - OCR
- **SQLAlchemy** - ORM base de données
- **JWT** - Authentification
- **BeautifulSoup** - Web scraping
- **Redis** - Cache
- **Celery** - Tâches asynchrones

## 🆘 Support

Si vous rencontrez des problèmes :
1. Vérifiez que Python 3.8+ est installé
2. Vérifiez que vous êtes dans l'environnement virtuel
3. Consultez le fichier `DATABASE_SETUP.md` pour la configuration de la base de données
4. Lancez `python test_database.py` pour tester la configuration

---

**🎯 Objectif :** Avoir l'API PriceScan fonctionnelle en moins de 5 minutes !
