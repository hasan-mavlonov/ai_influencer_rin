# main.py
# -*- coding: utf-8 -*-
from rin.agent import RinAgent

import sys
sys.stdout.reconfigure(encoding='utf-8')

if __name__ == "__main__":
    print("🧠 Generating Rin’s post...")
    rin = RinAgent()
    caption = rin.generate_caption("weekend brunch at an aesthetic café")
    print("\n💬 Rin’s caption:\n", caption)
