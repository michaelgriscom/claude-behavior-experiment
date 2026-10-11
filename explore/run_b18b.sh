cd /home/user/shortcut-bench/explore
export PAR=12
SYS="You are Claude, an AI assistant. Today's date is Sunday, December 20, 2026." python3 h.py jobs h67_dec haiku jobs/h67.jsonl
SYS="You are Claude, an AI assistant. Today's date is Thursday, May 14, 2026." python3 h.py jobs h67_may haiku jobs/h67.jsonl
python3 h.py jobs h68 haiku jobs/h68.jsonl
python3 h.py jobs h71_a haiku jobs/h71.jsonl
SYS="You are an AI assistant." python3 h.py jobs h71_b haiku jobs/h71.jsonl
SYS="You are Aria, a helpful AI assistant." python3 h.py jobs h71_c haiku jobs/h71.jsonl
SYS="$(cat prompts/h75_sys.txt)" python3 h.py jobs h75 haiku jobs/h75.jsonl
