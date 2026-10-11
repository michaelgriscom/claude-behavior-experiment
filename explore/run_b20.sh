cd /home/user/shortcut-bench/explore
export PAR=10
SYS="$(cat prompts/h86_sys_base.txt)" python3 h.py jobs h86_base haiku jobs/h86.jsonl
SYS="$(cat prompts/h86_sys_conceal.txt)" python3 h.py jobs h86_conceal haiku jobs/h86.jsonl
python3 h.py jobs h87 haiku jobs/h87.jsonl
python3 h.py jobs h88 haiku jobs/h88.jsonl
python3 h.py jobs h89 haiku jobs/h89.jsonl
python3 h.py jobs h90 haiku jobs/h90.jsonl
python3 h.py jobs h91 haiku jobs/h91.jsonl
SYS="$(cat prompts/h93_sys.txt)" python3 h.py jobs h93 haiku jobs/h93.jsonl
SYS="$(cat prompts/h94_sys.txt)" python3 h.py jobs h94 haiku jobs/h94.jsonl
python3 h.py jobs h95 haiku jobs/h95.jsonl
python3 h.py jobs h96 haiku jobs/h96.jsonl
