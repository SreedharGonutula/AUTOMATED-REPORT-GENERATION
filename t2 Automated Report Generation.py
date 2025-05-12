import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Step 1: Create Sample Data
data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Math": [85, 70, 95, 60],
    "Science": [90, 75, 88, 65],
    "English": [78, 80, 92, 70]
}
df = pd.DataFrame(data)

# Step 2: Calculate Summary Statistics
summary = df.drop("Name", axis=1).describe()

# Step 3: Plot Average Scores
df["Average"] = df[["Math", "Science", "English"]].mean(axis=1)
plt.figure(figsize=(6, 4))
plt.bar(df["Name"], df["Average"], color='skyblue')
plt.title("Average Scores per Student")
plt.ylabel("Score")
plt.tight_layout()
chart_path = "avg_scores_chart.png"
plt.savefig(chart_path)
plt.close()

# Step 4: Generate PDF Report
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Student Performance Report", ln=True, align='C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def add_summary_table(self, summary_df):
        self.set_font("Arial", "B", 11)
        col_width = self.w / (len(summary_df.columns) + 1)
        self.cell(col_width, 10, "Stat", border=1)
        for col in summary_df.columns:
            self.cell(col_width, 10, col, border=1)
        self.ln()

        self.set_font("Arial", "", 11)
        for idx in ["mean", "min", "max"]:
            self.cell(col_width, 10, idx, border=1)
            for val in summary_df.loc[idx]:
                self.cell(col_width, 10, f"{val:.2f}", border=1)
            self.ln()

# Create and Save PDF
pdf = PDFReport()
pdf.add_page()
pdf.chapter_title("Summary Statistics")
pdf.add_summary_table(summary)

pdf.chapter_title("Average Scores Chart")
pdf.image(chart_path, x=30, w=150)

pdf_file = "student_report.pdf"
pdf.output(pdf_file)

print(f"✅ PDF report saved as: {pdf_file}")
