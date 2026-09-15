# -*- coding: utf-8 -*-
import os, psutil

# Check if WINWORD is running and terminate if so
word_procs = [p for p in psutil.process_iter(['pid', 'name']) if 'winword' in p.info['name'].lower()]
for p in word_procs:
    try:
        p.terminate()
        print(f"Terminated WINWORD PID {p.info['pid']}")
    except:
        pass

with open(r'E:\VanDe_AI\build_full_report.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code)
print("Finished building full report!")
