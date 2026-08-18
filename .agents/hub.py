#!/usr/bin/env python3
"""
Lightweight shortcut for .agents/agent_hub.py
Usage: python .agents/hub.py [command] [options]
"""
import os
import sys

hub_path = os.path.join(os.path.dirname(__file__), "agent_hub.py")
if os.path.exists(hub_path):
    import agent_hub
    agent_hub.main()
else:
    print(f"Error: Could not locate {hub_path}")
    sys.exit(1)
