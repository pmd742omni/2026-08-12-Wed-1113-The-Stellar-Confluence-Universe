#!/usr/bin/env python3
"""
Prompt-Response Flow Logging Utility for The Stellar Confluence Universe
Maintains the pair-programming interaction journal with standardized YAML frontmatter,
authoritative local timestamps, and clean markdown entry blocks.
"""

import os
import sys
import json
import re
import datetime
import argparse
import glob

def find_project_root():
    cwd = os.getcwd()
    curr = cwd
    while True:
        if glob.glob(os.path.join(curr, "*Prompt-Response Flow*")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return cwd

PROJECT_ROOT = find_project_root()

def get_active_flow_file():
    """Finds or creates the active Prompt-Response Flow file."""
    flow_dirs = glob.glob(os.path.join(PROJECT_ROOT, "*Prompt-Response Flow*"))
    if flow_dirs:
        target_dir = flow_dirs[0]
    else:
        now = datetime.datetime.now().astimezone()
        dir_name = now.strftime("%Y-%m-%d %a %H%M Prompt-Response Flow")
        target_dir = os.path.join(PROJECT_ROOT, dir_name)
        os.makedirs(target_dir, exist_ok=True)

    files = glob.glob(os.path.join(target_dir, "*.md"))
    if files:
        return files[0]
    
    # Create default file
    now = datetime.datetime.now().astimezone()
    file_title = now.strftime("%Y-%m-%d %a %H%M Prompt-Response Flow")
    file_path = os.path.join(target_dir, f"{file_title}.md")
    
    initial_content = f"""---
Name: "{file_title}"
Version: "1.0"
Date: "{now.strftime('%Y-%m-%d %a %H%M')}"
---
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(initial_content)
    
    return file_path

def format_entry(prompt_text, response_text, timestamp=None):
    now = timestamp or datetime.datetime.now().astimezone()
    day_header = now.strftime("# %Y-%m-%d %a")
    time_header = now.strftime("## %H%M")
    
    entry = f"""
{day_header}

{time_header}

### Prompt

{prompt_text.strip()}

### Response

{response_text.strip()}
"""
    return entry

def append_flow_entry(prompt_text, response_text, file_path=None):
    target = file_path or get_active_flow_file()
    entry_text = format_entry(prompt_text, response_text)
    
    with open(target, "a", encoding="utf-8") as f:
        f.write(entry_text)
        
    return {
        "status": "appended",
        "file": target,
        "entry_length": len(entry_text)
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append entry to Prompt-Response Flow journal")
    parser.add_argument("--prompt", type=str, help="User prompt text")
    parser.add_argument("--response", type=str, help="Assistant response text")
    parser.add_argument("--file", type=str, help="Specific flow markdown file path")
    
    args = parser.parse_args()
    if args.prompt and args.response:
        res = append_flow_entry(args.prompt, args.response, args.file)
        print(json.dumps(res, indent=2))
    else:
        active = get_active_flow_file()
        print(json.dumps({"active_flow_file": active}, indent=2))
