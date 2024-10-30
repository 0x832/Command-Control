import telegram
from telegram.ext import Application, CommandHandler
import os
from functools import wraps
import pyautogui

TOKEN = ''
AUTHORIZED_USERS = []  

def authorized_only(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in AUTHORIZED_USERS:  
            await update.message.reply_text('❌No tienes permiso para usar este comando❌')
            return 
        return await func(update, context, *args, **kwargs)  
    return wrapped

async def notify_startup(context):
    for chat_id in AUTHORIZED_USERS:
        await context.bot.send_message(chat_id=chat_id, text="👤 Alguien ha iniciado el PC \n\n Si quieres apagarlo ⮕ /shutdown 👤")

@authorized_only
async def lock_screen(update, context):
    os.system('rundll32.exe user32.dll,LockWorkStation')
    await update.message.reply_text('Pantalla bloqueada.')

@authorized_only
async def shutdown(update, context):
    await update.message.reply_text('Apagando el PC...')
    os.system('shutdown /s /t 0')

@authorized_only
async def reboot(update, context):
    await update.message.reply_text('Reiniciando el PC...')
    os.system('shutdown /r /t 0')

@authorized_only
async def info(update, context):
    await update.message.reply_text("""
    📡 Command & Control 📡
                                    
    🖥️ Suspender pantalla: /lock
    📴 Apagar PC: /shutdown
    🔄 Reiniciar PC: /reboot
    ⏭️ info: /start

    Usa estos comandos para 
    controlar tu PC de manera remota.
    """)
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('lock', lock_screen))
    application.add_handler(CommandHandler('shutdown', shutdown))
    application.add_handler(CommandHandler('reboot', reboot))    
    application.add_handler(CommandHandler('start', info))  

    application.run_polling()
if __name__ == '__main__':
    main()
