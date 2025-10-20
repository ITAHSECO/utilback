import os
from dotenv import load_dotenv
import datetime

print("🔍 DIAGNÓSTICO INICIADO...")
load_dotenv()

# ===== MOSTRAR TODO el .env (SIN OCULTAR NADA) =====
print("\n📄 === TODO EL .env ===")
try:
    with open('.env', 'r', encoding='utf-8') as f:
        print(f.read())
except:
    print("❌ .env NO ENCONTRADO")
print("======================\n")

# ===== VALIDACIONES DETALLADAS =====
print("✅ VERIFICANDO CONFIGURACIONES...\n")

errors = []

# 1. Gmail
GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")
print(f"GMAIL_USER: {'✅ OK' if GMAIL_USER else '❌ VACÍO'}")
print(f"GMAIL_PASSWORD: {'✅ OK' if GMAIL_APP_PASSWORD else '❌ VACÍO'}")
print(f"EMAIL_TO: {'✅ OK' if EMAIL_TO else '❌ VACÍO'}")
if not all([GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_TO]):
    errors.append("FALTAN credenciales GMAIL")

# 2. Rutas
BACKUP_SOURCE = os.getenv("BACKUP_SOURCE", r"N:\SQL_BACKUP")
BACKUP_DEST = os.getenv("BACKUP_DEST", r"G:\.shortcut-targets-by-id\11mzlg_qx4dn5U4WMK5N9Gq_WxIbx42SU\BACKS")
LOCAL_BACKUP = os.getenv("LOCAL_BACKUP", r"C:\BACK\ulQG.bak")

print(f"\nBACKUP_SOURCE ({BACKUP_SOURCE}): {'✅ EXISTE' if os.path.exists(BACKUP_SOURCE) else '❌ NO EXISTE'}")
print(f"BACKUP_DEST ({BACKUP_DEST}): {'✅ EXISTE' if os.path.exists(BACKUP_DEST) else '❌ NO EXISTE'}")
print(f"LOCAL_BACKUP ({LOCAL_BACKUP}): {'✅ EXISTE' if os.path.exists(LOCAL_BACKUP) else '❌ NO EXISTE'}")

if not os.path.exists(BACKUP_SOURCE):
    errors.append(f"BACKUP_SOURCE NO EXISTE: {BACKUP_SOURCE}")
if not os.path.exists(BACKUP_DEST):
    errors.append(f"BACKUP_DEST NO EXISTE: {BACKUP_DEST}")
if not os.path.exists(LOCAL_BACKUP):
    errors.append(f"LOCAL_BACKUP NO EXISTE: {LOCAL_BACKUP}")

# 3. Horarios
try:
    INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))
    MAX_EXECUTIONS = int(os.getenv("MAX_EXECUTIONS", 10))
    print(f"\nINTERVAL_HOURS: {INTERVAL_HOURS} ✅")
    print(f"MAX_EXECUTIONS: {MAX_EXECUTIONS} ✅")
except:
    errors.append("ERROR en INTERVAL_HOURS o MAX_EXECUTIONS")
    INTERVAL_HOURS = 6
    MAX_EXECUTIONS = 10

# ===== RESULTADO =====
print(f"\n{'='*50}")
print(f"📊 RESUMEN DE ERRORES ({len(errors)}):")
print(f"{'='*50}")

if errors:
    for i, error in enumerate(errors, 1):
        print(f"{i}. ❌ {error}")
    print(f"\n🛠️  SOLUCIÓN: Arregla los {len(errors)} errores arriba")
else:
    print("🎉 ¡TODO CORRECTO! Puedes usar el script completo")

print(f"{'='*50}\n")
input("Presiona ENTER para salir...")