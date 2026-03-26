import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import io
from fpdf import FPDF
from io import BytesIO

from utils.hide_streamlit_default import hide_default_info
from utils.page_config import setup_page_config

setup_page_config()
hide_default_info()
st.title("🗺️ Your Personalized Financial Roadmap")

# Check if roadmap data exists
if "roadmap_data" not in st.session_state:
    st.warning("🚧 Please complete the quiz to generate your roadmap.")
    st.stop()

roadmap = st.session_state.roadmap_data

# Icons for roadmap journey
icons = {
    "Budgeting": "💰",
    "Taxes": "🧾",
    "Investing": "📈",
    "Debt Management": "💳"
}

# Order the roadmap categories
section_order = ["Budgeting", "Taxes", "Investing", "Debt Management"]

st.markdown("### 📍 Your Financial Milestone Journey")

# Display roadmap as a horizontal journey
for section in section_order:
    if section not in roadmap:
        continue

    content = roadmap[section]
    st.markdown(f"#### {icons.get(section, '')} **{section}** — *{content.get('subtitle', '')}*")

    col1, col2 = st.columns(2)
    for idx, step in enumerate(content["topics"], 1):
        with (col1 if idx % 2 else col2):
            st.markdown(f"**Step {idx}: {step['label']}**")
            st.markdown(f"{step['summary']}")
            if step["resources"]:
                st.markdown("🔗 **Resources:**")
                for title, url in step["resources"]:
                    st.markdown(f"- [{title}]({url})")
            st.markdown("")

    st.divider()

def format_roadmap_as_text(roadmap):
    output = "Your Personalized Financial Roadmap\n\n"
    for section in section_order:
        if section not in roadmap:
            continue
        content = roadmap[section]
        output += f"## {section} — {content.get('subtitle', '')}\n\n"
        for idx, step in enumerate(content["topics"], 1):
            output += f"### Step {idx}: {step['label']}\n"
            output += f"{step['summary']}\n\n"
            if step["resources"]:
                output += "Resources:\n"
                for title, url in step["resources"]:
                    output += f"- {title}: {url}\n"
            output += "\n"
        output += "\n" + "-" * 40 + "\n\n"
    return output

def sanitize(text):
    return (
        text.replace("—", "-")
            .replace("–", "-")
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("‘", "'")
    )

class RoadmapPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Personalized Financial Literacy Roadmap", ln=True, align="C")
        self.ln(10)

    def add_section(self, section, content):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, sanitize(f"{section} — {content.get('subtitle', '')}"), ln=True)
        self.ln(4)

        self.set_font("Helvetica", size=12)
        for idx, step in enumerate(content["topics"], 1):
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 8, sanitize(f"Step {idx}: {step['label']}"))
            self.set_text_color(60, 60, 60)
            self.multi_cell(0, 8, sanitize(step['summary']))

            if step["resources"]:
                self.set_text_color(0, 0, 180)
                self.set_font("Helvetica", style="U", size=12)
                for title, url in step["resources"]:
                    self.cell(0, 8, sanitize(title), ln=True, link=url)
            self.ln(6)
        self.ln(4)

# Create the PDF in memory
pdf = RoadmapPDF()
pdf.add_page()

for section in section_order:
    if section in roadmap:
        pdf.add_section(section, roadmap[section])

# Convert to byte stream
pdf_buffer = BytesIO()
pdf_buffer.write(pdf.output(dest="S").encode("latin-1"))
pdf_data = pdf_buffer.getvalue()

# Buttons: Download + Go to Home Page
st.download_button(
    label="📄 Download Roadmap as PDF",
    data=pdf_data,
    file_name="financial_roadmap.pdf",
    mime="application/pdf"
)

st.markdown("### Want to save your roadmap?")
if st.button("✏️ Create Account"):
    st.switch_page("pages/signup.py")
