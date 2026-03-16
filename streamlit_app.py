import streamlit as st

from db.db_bridge import create_workspace, open_workspace, save_feedback, list_feedback
from core.feedback import FeedbackEntry
from ai.ai import analyze_strengths


st.image("web/assets/logo.png",)

# ---------- Create drawer ----------

st.header("Create feedback drawer")

create_token = st.text_input("New token")
create_label = st.text_input("Label (optional)")

if st.button("Create drawer"):
    try:
        workspace_id = create_workspace(create_token, create_label)
        st.success(f"Drawer created. Workspace ID: {workspace_id}")
    except Exception as e:
        st.error(str(e))


# ---------- Open drawer ----------

st.header("Open feedback drawer")

open_token = st.text_input("Open token")

if st.button("Open drawer"):
    try:
        workspace = open_workspace(open_token)
        st.session_state["workspace_id"] = workspace["id"]
        st.session_state["workspace_token"] = workspace["token"]
        st.session_state["workspace_label"] = workspace["label"]

        st.success(f"Opened drawer: {workspace['label'] or workspace['token']}")
    except Exception as e:
        st.error(str(e))


# ---------- Show active drawer ----------

if "workspace_id" in st.session_state:
    st.info(
        f"Active drawer: "
        f"{st.session_state.get('workspace_label') or st.session_state.get('workspace_token')}"
    )


# ---------- Add feedback ----------

st.header("Add feedback")

text = st.text_area("Feedback")
source = st.text_input("Source")
context = st.text_input("Context")
entry_type = st.text_input("Type")

if st.button("Save feedback"):
    if "workspace_id" not in st.session_state:
        st.error("Open a drawer first.")
    else:
        try:
            entry = FeedbackEntry(
                text=text,
                source=source,
                context=context,
                entry_type=entry_type,
            )

            feedback_id = save_feedback(st.session_state["workspace_id"], entry)

            st.success(f"Feedback saved. ID: {feedback_id}")

        except Exception as e:
            st.error(str(e))


# ---------- Analyze ----------

st.header("Analyze strengths")

if st.button("Analyze"):
    if "workspace_id" not in st.session_state:
        st.error("Open a drawer first.")
    else:
        try:
            feedback = list_feedback(st.session_state["workspace_id"])
            result = analyze_strengths(feedback)

            st.subheader("Your strengths")

            for i, s in enumerate(result["strengths"], start=1):
                st.write(f"**{i}. {s['name']}** — {s['reason']}")

        except Exception as e:
            st.error(str(e))