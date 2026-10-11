cd /home/user/shortcut-bench/explore
export PAR=12
SYS="$(cat prompts/h78_sys_base.txt)" python3 h.py jobs h78_base haiku jobs/h78.jsonl
SYS="$(cat prompts/h78_sys_deny.txt)" python3 h.py jobs h78_deny haiku jobs/h78.jsonl
python3 h.py jobs h83own haiku jobs/h83own.jsonl
python3 h83build.py && python3 h.py jobs h83oth haiku jobs/h83oth.jsonl
python3 h81.py h81e haiku 30
python3 h.py jobs h81d haiku jobs/h81d.jsonl
python3 h.py jobs h80 haiku jobs/h80.jsonl
EFFORT=low python3 h.py jobs h82_low haiku jobs/h82.jsonl
EFFORT=max python3 h.py jobs h82_max haiku jobs/h82.jsonl
SYS="$(cat prompts/h84_sys_base.txt)" python3 h.py jobs h84_base haiku jobs/h84.jsonl
SYS="$(cat prompts/h84_sys_steer.txt)" python3 h.py jobs h84_steer haiku jobs/h84.jsonl
python3 h.py jobs h79 haiku jobs/h79.jsonl
python3 h.py jobs h85 haiku jobs/h85.jsonl
