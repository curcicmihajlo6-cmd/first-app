# ...existing code...
"""
Simple local "AI" chatbot (terminal).
- Rule-based + small knowledge store (knowledge.json optional).
- Safe arithmetic evaluation.
- Extended with Scrum-focused knowledge and commands:
    /scrum           - list available Scrum topics
    /scrum <topic>   - show detailed info about a topic
    /export_scrum    - write built-in Scrum knowledge to knowledge.json
Run: python AI.py
Commands:
  /exit     - quit
  /help     - show help
  /reload   - reload knowledge.json
"""
import json
import os
import time
import math
import datetime
import ast
import operator as op

KNOWLEDGE_FILE = "knowledge.json"

# Safe eval for arithmetic expressions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

def safe_eval(expr: str):
    """
    Evaluate a simple arithmetic expression safely.
    Supports + - * / ** % // and parentheses.
    """
    try:
        node = ast.parse(expr, mode="eval").body
        return _eval_node(node)
    except Exception as e:
        raise ValueError("invalid expression") from e

def _eval_node(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
    raise ValueError("unsupported expression")

# Load simple Q/A knowledge file if present
def load_knowledge(path=KNOWLEDGE_FILE):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return {k.lower(): v for k, v in data.items()}
        except Exception:
            pass
    return {}

KNOW = load_knowledge()

# Built-in Scrum knowledge base (concise but comprehensive)
SCRUM_KB = {
    "overview": (
        "Scrum is an empirical, iterative framework to deliver products in timeboxed Sprints. "
        "It emphasizes inspection, adaptation, and transparency. Each Sprint produces a potentially "
        "shippable Increment that meets the Definition of Done."
    ),
    "roles": (
        "Three core roles: Product Owner (prioritizes backlog, defines product vision), "
        "Scrum Master (facilitates Scrum, removes impediments), and Developers (cross-functional team "
        "that builds the Increment)."
    ),
    "artifacts": (
        "Product Backlog: ordered list of requirements. "
        "Sprint Backlog: selected items + plan for the Sprint. "
        "Increment: the working product at Sprint end. "
        "Definition of Done: criteria an Increment must meet."
    ),
    "events": (
        "Sprint: fixed-length iteration (1-4 weeks). "
        "Sprint Planning: set Sprint Goal and select backlog items. "
        "Daily Scrum: 15-min daily inspection and plan. "
        "Sprint Review: inspect Increment with stakeholders and adapt Product Backlog. "
        "Sprint Retrospective: inspect and improve process."
    ),
    "sprint planning": (
        "During Sprint Planning the Scrum Team defines a Sprint Goal, selects Product Backlog Items "
        "to deliver, and creates a plan (Sprint Backlog). Timebox ~2 hours per week of Sprint length."
    ),
    "daily scrum": (
        "A 15-minute timeboxed event for Developers to inspect progress toward the Sprint Goal and "
        "plan the next 24 hours. Focus on status, impediments, and adjustments to the plan."
    ),
    "sprint review": (
        "At Sprint end the team presents the Increment to stakeholders for feedback. The Product Backlog "
        "is revised based on feedback; decisions about release or next priorities are made."
    ),
    "retrospective": (
        "Inspect the team's process and collaboration; identify concrete improvements and create a plan "
        "to implement them in the next Sprint."
    ),
    "definition of done": (
        "A shared checklist describing quality criteria an Increment must meet to be releasable. "
        "Used to ensure transparency and consistent quality."
    ),
    "backlog refinement": (
        "Ongoing activity to clarify, decompose, and estimate Product Backlog items so they are ready "
        "for future Sprint Planning. Not a mandatory formal event but timeboxed as needed."
    ),
    "estimation": (
        "Common techniques: story points, t-shirt sizing, planning poker. Estimation captures relative "
        "size/effort, not time. Used for forecasting, not commitment."
    ),
    "velocity": (
        "Velocity is the average number of story points a team completes per Sprint. Useful for forecasting "
        "but should not be used as a performance target."
    ),
    "burndown": (
        "A burndown chart shows remaining work in the Sprint (or release). It helps visualize progress "
        "toward the Sprint Goal."
    ),
    "acceptance criteria": (
        "Conditions that a Product Backlog Item must satisfy to be accepted. They guide development and testing."
    ),
    "scaling scrum": (
        "For large products, multiple Scrum Teams coordinate via approaches like Nexus, LeSS, or the Scaled Agile Framework. "
        "Maintain clear Product Backlog, cross-team integration, and shared Definition of Done."
    ),
    "common anti-patterns": (
        "Examples: treating Scrum as a process contract, skipping retrospectives, unclear Definition of Done, "
        "over-committing, or using velocity as a performance metric."
    ),
    "checklist": (
        "Sprint checklist: 1) Sprint Goal defined, 2) Backlog items selected and understood, 3) Tasks identified, "
        "4) Definition of Done applied, 5) QA & integration planned, 6) Daily Scrum scheduled, 7) Stakeholders invited to Review."
    )
}

def scrum_topics_list() -> str:
    keys = sorted(SCRUM_KB.keys())
    return "Available Scrum topics:\n" + ", ".join(keys)

def scrum_answer(topic: str) -> str:
    t = topic.strip().lower()
    if not t:
        return SCRUM_KB["overview"]
    if t in SCRUM_KB:
        return SCRUM_KB[t]
    # try fuzzy match by keyword
    for k in SCRUM_KB:
        if t in k or k in t:
            return SCRUM_KB[k]
    return f"No detailed info for '{topic}'. Use /scrum to list topics."

# Simple responder extended for Scrum
def respond(prompt: str) -> str:
    q = prompt.strip()
    if not q:
        return "Please type a question or /help for commands."
    low = q.lower()
    # Built-in command: /scrum
    if low.startswith("/scrum"):
        parts = q.split(" ", 1)
        if len(parts) == 1:
            return scrum_topics_list()
        else:
            return scrum_answer(parts[1])
    # allow user to ask general Scrum questions
    if "scrum" in low or any(w in low for w in ("sprint", "product backlog", "definition of done", "scrum master", "product owner")):
        # try to find a relevant topic word
        for key in SCRUM_KB:
            if key in low:
                return SCRUM_KB[key]
        # fallback to overview
        return SCRUM_KB["overview"]
    # direct knowledge match from external knowledge.json
    if low in KNOW:
        return KNOW[low]
    # greetings
    if any(g in low for g in ("hello", "hi", "hey", "good morning", "good afternoon")):
        return "Hello. How can I help you today?"
    if "time" in low and ("what" in low or "current" in low):
        return "Current time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # date
    if "date" in low and ("what" in low or "today" in low):
        return "Today's date: " + datetime.date.today().isoformat()
    # simple math: detect arithmetic characters and try to eval
    if any(ch in q for ch in "+-*/%()") and any(ch.isdigit() for ch in q):
        try:
            result = safe_eval(q)
            return f"Result: {result}"
        except Exception:
            pass
    # definitions from knowledge keys like "define X" or "what is X"
    if low.startswith("define ") or low.startswith("what is "):
        key = low.split(" ", 1)[1].strip()
        if key in KNOW:
            return KNOW[key]
        else:
            return f"I don't have a definition for '{key}'. You can add it to {KNOWLEDGE_FILE}."
    # fallback
    return ("I don't know the exact answer. Try rephrasing, ask a specific Scrum question, "
            "or use /scrum to list topics. You can also add Q/A via /add or /export_scrum to save the built-in Scrum KB.")

def export_scrum(path=KNOWLEDGE_FILE) -> str:
    try:
        # merge existing knowledge with scrum kb (lowercased keys)
        existing = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f) or {}
        merged = existing.copy()
        for k, v in SCRUM_KB.items():
            merged[k] = v
        with open(path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        return f"Exported Scrum knowledge to {path} ({len(SCRUM_KB)} topics)."
    except Exception as e:
        return f"Failed to export: {e}"

def repl():
    print("Simple local AI — type questions. /help for commands. Use /scrum to access Scrum topics.")
    while True:
        try:
            inp = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not inp:
            continue
        if inp.startswith("/"):
            cmd = inp.lower()
            if cmd == "/exit":
                print("Goodbye.")
                break
            if cmd == "/help":
                print("/help    show this help\n/exit    quit\n/reload  reload knowledge.json\n/add     add Q/A to knowledge file\n/scrum   list Scrum topics or /scrum <topic>\n/export_scrum   save built-in Scrum KB to knowledge.json")
                continue
            if cmd == "/reload":
                global KNOW
                KNOW = load_knowledge()
                print(f"Reloaded knowledge ({len(KNOW)} entries).")
                continue
            if cmd == "/export_scrum":
                print(export_scrum())
                continue
            if cmd == "/add":
                q = input("Question (exact): ").strip().lower()
                a = input("Answer: ").strip()
                if q:
                    KNOW[q] = a
                    try:
                        # merge with file if exists
                        existing = {}
                        if os.path.exists(KNOWLEDGE_FILE):
                            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                                existing = json.load(f) or {}
                        existing.update({q: a})
                        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
                            json.dump(existing, f, indent=2, ensure_ascii=False)
                        print("Saved to knowledge.json")
                    except Exception as e:
                        print("Failed to save:", e)
                else:
                    print("Empty question, aborted.")
                continue
            print("Unknown command. /help for commands.")
            continue
        # normal question
        ans = respond(inp)
        print(ans)

if __name__ == "__main__":
    repl()
# ...existing code...