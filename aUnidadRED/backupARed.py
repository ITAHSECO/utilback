import os
import shutil
import datetime
from pathlib import Path
from dotenv import load_dotenv
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Cargar configuraciones desde .env
load_dotenv()

# Configuraciones desde .env
LOG_FILE = os.getenv("LOG_FILE", r"C:\scripts\output.log")
SCRIPT_LOG = os.getenv("SCRIPT_LOG", r"C:\scripts\script.log")
BACKUP_SOURCE = os.getenv("BACKUP_SOURCE", r"N:\SQL_BACKUP")
BACKUP_DEST = os.getenv("BACKUP_DEST", r"G:\.shortcut-targets-by-id\11mzlg_qx4dn5U4WMK5N9Gq_WxIbx42SU\BACKS")
LOCAL_BACKUP = os.getenv("LOCAL_BACKUP", r"C:\BACK\ulQG.bak")
INTERVAL_HOURS = int(os.getenv("INTERVAL_HOURS", 6))
MAX_EXECUTIONS = int(os.getenv("MAX_EXECUTIONS", 10))
START_TIME = os.getenv("START_TIME", "08:00")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

# Validaciones
try:
    assert all([GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_TO]), "Faltan credenciales de Gmail en .env"
    assert os.path.exists(BACKUP_SOURCE)
    assert os.path.exists(BACKUP_DEST)
except AssertionError as e:
    print(f"❌ Error: {str(e)}")
    exit(1)

execution_count = 0

def log_message(message, log_file=LOG_FILE):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    print(message)

def send_completion_email():
    """Envía correo con logs al completar el ciclo"""
    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = f"✅ Backup Softcon COMPLETADO - {datetime.datetime.now().strftime('%Y-%m-%d')}"

        # Cuerpo del correo
        body = f"""
🚀 BACKUP SOFTCON FINALIZADO CORRECTAMENTE

📅 Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔄 Configuración: {MAX_EXECUTIONS} ejecuciones cada {INTERVAL_HOURS} horas
✅ Total exitosas: {execution_count}

📎 Adjunto: output.log completo del ciclo

¡El próximo ciclo inicia mañana a las {START_TIME}!
        """
        msg.attach(MIMEText(body, 'plain'))

        # Adjuntar output.log
        with open(LOG_FILE, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= output.log'
        )
        msg.attach(part)

        # Enviar correo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        log_message("📧 CORREO ENVIADO CORRECTAMENTE")
        print("✅ Email enviado!")
        
    except Exception as e:
        error_msg = f"❌ ERROR ENVIANDO CORREO: {str(e)}"
        log_message(error_msg)
        print(error_msg)

def copy_files(source_pattern, dest_folder, description):
    global execution_count
    log_message(f"......=ACCEDIENDO A {description}=......")
    try:
        if '*' in source_pattern:
            files = Path(source_pattern).parent.glob(Path(source_pattern).name)
            for file_path in files:
                dest_path = Path(dest_folder) / file_path.name
                shutil.copy2(str(file_path), str(dest_path))
                log_message(f"Copiado: {file_path.name}")
        else:
            shutil.copy2(source_pattern, dest_folder)
            log_message(f"Copiado: {os.path.basename(source_pattern)}")
        log_message(".....................................................")
    except Exception as e:
        log_message(f"ERROR: {str(e)}")

def backup_task():
    global execution_count
    execution_count += 1
    log_message(f"🔄 Ejecución #{execution_count}/{MAX_EXECUTIONS}")
    log_message("=========== SOFTCON - INICIANDO PROCESO DE COPIADO=============")
    
    copy_files(f"{BACKUP_SOURCE}\\*.bak", BACKUP_DEST, "SQL_BACKUP *.bak")
    copy_files(f"{BACKUP_SOURCE}\\ulSERVTEC.sql", BACKUP_DEST, "ulSERVTEC.sql")
    copy_files(LOCAL_BACKUP, BACKUP_DEST, "ulQG.bak")
    
    log_message("✅ COPIA TERMINADA")
    
    final_log = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Ejecutado"
    with open(SCRIPT_LOG, 'a', encoding='utf-8') as f:
        f.write(final_log + "\n")

def wait_until_start_time():
    now = datetime.datetime.now()
    start_hour, start_minute = map(int, START_TIME.split(":"))
    target = now.replace(hour=start_hour, minute=start_minute, second=0)
    if target < now:
        target += datetime.timedelta(days=1)
    seconds_to_wait = (target - now).total_seconds()
    log_message(f"⏰ Esperando {seconds_to_wait/3600:.1f}h hasta {target.strftime('%H:%M')}")
    time.sleep(seconds_to_wait)

def run_daily_cycle():
    global execution_count
    execution_count = 0
    log_message("🌅 INICIANDO CICLO DIARIO")
    
    while execution_count < MAX_EXECUTIONS:
        wait_until_start_time()
        backup_task()
        if execution_count < MAX_EXECUTIONS:
            log_message(f"💤 Durmiendo {INTERVAL_HOURS}h hasta próxima...")
            time.sleep(INTERVAL_HOURS * 3600)
    
    # 🚀 ÚLTIMA EJECUCIÓN: ENVIAR CORREO
    log_message("🎉 ÚLTIMA EJECUCIÓN COMPLETADA - ENVIANDO CORREO...")
    send_completion_email()
    log_message("✅ Ciclo completado. Reiniciando en 24h...")

# 🚀 INICIO - MODO CONTINUO
log_message("🎯 MODO CONTINUO ACTIVADO con NOTIFICACIÓN GMAIL")
log_message(f"Config: Cada {INTERVAL_HOURS}h, {MAX_EXECUTIONS}x/día desde {START_TIME}")

try:
    while True:
        run_daily_cycle()
        time.sleep(60)
except KeyboardInterrupt:
    log_message("🛑 Detenido manualmente")