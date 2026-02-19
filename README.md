# Strengthlytics

**Strengthlytics** is a feedback analysis tool inspired by Peter Drucker’s concept of *feedback analysis* from *Managing Oneself*.

Instead of guessing what you’re good at, Strengthlytics helps you identify recurring strengths and friction patterns by analyzing feedback over time.

Self-knowledge shouldn’t rely on memory or mood. It should rely on patterns.

---

## 🧠 Why?

Peter Drucker argued that most people think they know their strengths — and are usually wrong.

His method was simple:
- Collect feedback.
- Compare expectations with outcomes.
- Look for recurring patterns.
- Build from strengths.

In practice, however, feedback is scattered:
- A comment from a teacher.
- A remark from a colleague.
- A note from a manager.
- Something said in passing.

Strengthlytics structures that data and extracts patterns over time.

---

## 🚀 What It Does (MVP)

- Store feedback entries (who, context, when, what was said)
- Analyze recurring themes in the text
- Identify likely strengths
- Identify recurring friction areas
- Highlight patterns over time

The goal is not to let AI decide who you are.

The goal is to detect patterns in what others repeatedly observe.

---

## 🏗 Architecture (v1)

Phase 1:
- Python core logic
- SQLite database
- CLI interface

Phase 2:
- Thematic analysis using OpenAI API
- Pattern clustering
- Structured output

Phase 3:
- FastAPI backend
- Optional web interface

---

## 📦 Example Input

My teacher said I am calm during presentations.  
A colleague told me I’m good at structuring complex problems.  
I was told I avoid confrontation.  
My manager said I communicate clearly.

---

## 📊 Example Output

**Recurring Strengths**
- Clear communication (2 mentions)
- Structured thinking (1 mention)
- Emotional stability under stress (1 mention)

**Recurring Friction Patterns**
- Avoids confrontation (1 mention)

---

## 🎯 Philosophy

Strengthlytics does not generate personality insights.

It extracts signal from accumulated feedback.

Patterns over time > single comments.  
Evidence over intuition.  
Structure over self-doubt.

---

## 🛠 Tech Stack (current)

- Python
- SQLite
- OpenAI API (planned)
- FastAPI (planned)

---

## 📌 Status

Early-stage development.  
Core feedback storage and analysis engine in progress.