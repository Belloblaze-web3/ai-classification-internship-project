"""Generate an editable internship-submission PowerPoint deck.

Run from the project root:
    python create_presentation.py
"""
from pathlib import Path
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
OUT = ROOT / "Iris_AI_Classification_Internship_Submission.pptx"

NAVY = RGBColor(10, 29, 52)
BLUE = RGBColor(24, 91, 147)
TEAL = RGBColor(35, 157, 150)
ORANGE = RGBColor(231, 108, 47)
INK = RGBColor(24, 38, 56)
MUTED = RGBColor(91, 108, 125)
PALE = RGBColor(244, 247, 250)
WHITE = RGBColor(255, 255, 255)
LIGHT_TEAL = RGBColor(225, 244, 241)
LIGHT_ORANGE = RGBColor(252, 235, 224)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def box(slide, x, y, w, h, fill, line=None, radius=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.color.rgb = line or fill
    if radius:
        s.adjustments[0] = 0.08
    return s


def text(slide, x, y, w, h, value, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
         font="Aptos", valign=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.clear(); tf.word_wrap = True; tf.vertical_anchor = valign
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = value
    r.font.name = font; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
    return tb


def rich_text(slide, x, y, w, h, runs, size=18, color=INK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.clear(); tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    for value, clr, bold in runs:
        r = p.add_run(); r.text = value; r.font.name = "Aptos"; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = clr
    return tb


def title(slide, kicker, heading, page):
    text(slide, 0.65, 0.35, 8.8, 0.25, kicker.upper(), 10, TEAL, True)
    text(slide, 0.65, 0.65, 11.7, 0.55, heading, 28, NAVY, True)
    box(slide, 0.65, 1.28, 12.03, 0.02, TEAL)
    text(slide, 12.05, 7.12, 0.65, 0.2, f"{page:02d} / 08", 9, MUTED, True, PP_ALIGN.RIGHT)


def bullet_list(slide, x, y, w, items, size=17, color=INK, gap=0.48):
    for i, item in enumerate(items):
        yy = y + i * gap
        box(slide, x, yy + 0.08, 0.10, 0.10, ORANGE)
        text(slide, x + 0.22, yy, w - 0.22, 0.34, item, size, color)


def metric(slide, x, y, w, label, value, accent):
    box(slide, x, y, w, 1.18, WHITE, RGBColor(220, 228, 235), True)
    box(slide, x, y, 0.08, 1.18, accent, accent, True)
    text(slide, x + 0.22, y + 0.18, w - 0.35, 0.32, value, 28, accent, True)
    text(slide, x + 0.22, y + 0.64, w - 0.35, 0.28, label, 11, MUTED, True)

# Slide 1: cover
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, NAVY)
box(s, 8.85, 0, 4.483, 7.5, BLUE)
box(s, 9.55, 0.7, 2.55, 2.55, TEAL, TEAL, True)
box(s, 10.2, 1.35, 1.25, 1.25, ORANGE, ORANGE, True)
text(s, 0.75, 0.75, 7.3, 0.3, "DECODELABS · INTERNSHIP SUBMISSION", 12, TEAL, True)
text(s, 0.75, 1.55, 7.3, 1.35, "Iris Flower\nClassification Using AI", 35, WHITE, True)
text(s, 0.78, 3.35, 6.6, 0.7, "An end-to-end supervised learning pipeline built as an AI Engineer / Data Scientist project.", 18, RGBColor(218, 229, 239))
text(s, 0.78, 5.8, 5.5, 0.25, "K-Nearest Neighbors · StandardScaler · Python", 12, RGBColor(218, 229, 239), True)
text(s, 0.78, 6.25, 5.5, 0.25, "Verified test accuracy: 93.33%", 15, ORANGE, True)
text(s, 9.25, 4.55, 3.4, 0.3, "PROJECT 02", 12, WHITE, True)
text(s, 9.25, 5.05, 3.0, 0.75, "Data\nClassification", 26, WHITE, True)
text(s, 9.25, 6.55, 3.2, 0.25, "2026 · Portfolio presentation", 11, RGBColor(220, 230, 240))

# Slide 2: problem
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, PALE); title(s, "01 · Framing the task", "Problem & Objective", 2)
box(s, 0.65, 1.7, 5.1, 4.75, NAVY, NAVY, True)
text(s, 1.05, 2.1, 4.3, 0.35, "THE QUESTION", 11, TEAL, True)
text(s, 1.05, 2.6, 4.1, 1.25, "Can a machine learn to identify an Iris species from flower measurements?", 25, WHITE, True)
text(s, 1.05, 4.25, 4.1, 1.2, "Input: 4 numerical measurements\nOutput: 1 of 3 species classes", 18, RGBColor(220, 230, 240))
box(s, 6.25, 1.7, 6.4, 4.75, WHITE, RGBColor(220, 228, 235), True)
text(s, 6.7, 2.1, 5.3, 0.35, "PROJECT OBJECTIVE", 11, ORANGE, True)
bullet_list(s, 6.7, 2.75, 5.4, [
    "Load and understand a labeled dataset",
    "Split data into training and testing sets",
    "Apply a simple supervised algorithm",
    "Validate the model with multiple metrics",
], 18, INK, 0.72)
text(s, 6.7, 5.95, 5.1, 0.3, "Outcome: a reproducible, reviewable ML pipeline.", 15, BLUE, True)

# Slide 3: dataset
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, WHITE); title(s, "02 · Data understanding", "Dataset: Iris Benchmark", 3)
metric(s, 0.65, 1.7, 2.75, "SAMPLES", "150", BLUE)
metric(s, 3.65, 1.7, 2.75, "FEATURES", "4", TEAL)
metric(s, 6.65, 1.7, 2.75, "CLASSES", "3", ORANGE)
metric(s, 9.65, 1.7, 3.0, "MISSING VALUES", "0", BLUE)
text(s, 0.7, 3.35, 5.9, 0.35, "FEATURES USED", 11, TEAL, True)
# table-like feature list
features = [("Sepal length", "cm"), ("Sepal width", "cm"), ("Petal length", "cm"), ("Petal width", "cm")]
for i, (name, unit) in enumerate(features):
    yy = 3.8 + i * 0.52
    box(s, 0.7, yy, 5.2, 0.38, PALE, PALE, True)
    text(s, 0.95, yy + 0.08, 3.6, 0.2, name, 14, INK, True)
    text(s, 5.2, yy + 0.08, 0.45, 0.2, unit, 12, MUTED, False, PP_ALIGN.RIGHT)
text(s, 7.1, 3.35, 5.55, 0.35, "CLASS BALANCE", 11, ORANGE, True)
for i, (label, count, color) in enumerate([("Setosa", "50", TEAL), ("Versicolor", "50", BLUE), ("Virginica", "50", ORANGE)]):
    yy = 3.82 + i * 0.7
    text(s, 7.15, yy, 1.65, 0.28, label, 16, INK, True)
    box(s, 8.95, yy + 0.05, 2.8, 0.22, RGBColor(232, 237, 242), RGBColor(232, 237, 242), True)
    box(s, 8.95, yy + 0.05, 2.8, 0.22, color, color, True)
    text(s, 11.95, yy - 0.02, 0.55, 0.28, count, 16, color, True, PP_ALIGN.RIGHT)
text(s, 7.15, 6.05, 5.2, 0.3, "Balanced classes support fairer evaluation.", 14, MUTED)

# Slide 4: workflow
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, PALE); title(s, "03 · Engineering workflow", "From Raw Data to Predictions", 4)
steps = [("01", "Load", "Iris dataset", TEAL), ("02", "Split", "80 / 20 stratified", BLUE), ("03", "Scale", "StandardScaler", ORANGE), ("04", "Train", "KNN, k=5", TEAL), ("05", "Evaluate", "Metrics + matrix", BLUE)]
for i, (num, head, sub, color) in enumerate(steps):
    x = 0.65 + i * 2.48
    box(s, x, 2.15, 2.05, 2.35, WHITE, RGBColor(220, 228, 235), True)
    text(s, x + 0.22, 2.42, 0.5, 0.25, num, 12, color, True)
    box(s, x + 0.22, 2.95, 0.55, 0.07, color)
    text(s, x + 0.22, 3.28, 1.55, 0.35, head, 20, NAVY, True)
    text(s, x + 0.22, 3.85, 1.55, 0.4, sub, 13, MUTED)
    if i < 4:
        text(s, x + 2.12, 3.18, 0.3, 0.3, "→", 22, ORANGE, True, PP_ALIGN.CENTER)
text(s, 0.75, 5.45, 11.8, 0.5, "Design principle: keep preprocessing inside the model pipeline so the same transformation is applied consistently at training and inference time.", 17, NAVY, True, PP_ALIGN.CENTER)

# Slide 5: model
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, WHITE); title(s, "04 · Model design", "Scaled K-Nearest Neighbors", 5)
box(s, 0.65, 1.7, 5.5, 4.95, NAVY, NAVY, True)
text(s, 1.0, 2.05, 4.8, 0.3, "WHY KNN?", 11, TEAL, True)
text(s, 1.0, 2.55, 4.55, 0.9, "Similar flowers tend to occupy nearby points in feature space.", 23, WHITE, True)
bullet_list(s, 1.0, 3.85, 4.55, [
    "Simple and interpretable",
    "Strong fit for a small numerical dataset",
    "Scaling prevents large-unit features from dominating",
], 16, RGBColor(220, 230, 240), 0.62)
box(s, 6.65, 1.7, 6.0, 4.95, PALE, PALE, True)
text(s, 7.05, 2.05, 5.2, 0.3, "TUNING K", 11, ORANGE, True)
text(s, 7.05, 2.5, 5.0, 0.65, "The project tests odd k values from 1 to 15.", 20, NAVY, True)
# simple bar-like tuning summary from actual results
vals = [("k=1", "3.3%", TEAL), ("k=3", "6.7%", ORANGE), ("k=5", "6.7%", ORANGE), ("k=7–15", "3.3%", TEAL)]
for i, (lab, val, color) in enumerate(vals):
    yy = 3.55 + i * 0.58
    text(s, 7.05, yy, 1.1, 0.25, lab, 14, INK, True)
    box(s, 8.25, yy + 0.03, 2.9, 0.2, RGBColor(226, 232, 238), RGBColor(226, 232, 238), True)
    width = 0.55 if val == "6.7%" else 0.3
    box(s, 8.25, yy + 0.03, width, 0.2, color, color, True)
    text(s, 11.35, yy - 0.01, 0.8, 0.25, val, 14, color, True, PP_ALIGN.RIGHT)
text(s, 7.05, 6.05, 5.0, 0.3, "Final configuration: StandardScaler → KNN(k=5)", 14, BLUE, True)

# Slide 6: evaluation
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, PALE); title(s, "05 · Error analysis", "Evaluation: What Did the Model Miss?", 6)
cm = str(ART / "confusion_matrix.png")
s.shapes.add_picture(cm, Inches(0.7), Inches(1.65), width=Inches(5.7), height=Inches(4.9))
box(s, 6.8, 1.75, 5.8, 4.7, WHITE, RGBColor(220, 228, 235), True)
text(s, 7.2, 2.1, 4.9, 0.3, "READING THE MATRIX", 11, ORANGE, True)
text(s, 7.2, 2.6, 4.7, 0.72, "Setosa was classified perfectly.", 22, NAVY, True)
text(s, 7.2, 3.55, 4.75, 1.25, "The only errors were two Virginica flowers predicted as Versicolor. This is the expected harder boundary between these visually similar classes.", 17, INK)
box(s, 7.2, 5.35, 4.6, 0.68, LIGHT_ORANGE, LIGHT_ORANGE, True)
text(s, 7.45, 5.56, 4.1, 0.25, "28 / 30 test samples correct", 16, ORANGE, True)
text(s, 0.75, 6.78, 5.8, 0.25, "Source: executed project artifact · confusion_matrix.png", 9, MUTED)

# Slide 7: results
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, WHITE); title(s, "06 · Verified outcome", "Results & Evidence", 7)
metric(s, 0.65, 1.7, 2.75, "ACCURACY", "93.33%", TEAL)
metric(s, 3.65, 1.7, 2.75, "PRECISION", "94.44%", BLUE)
metric(s, 6.65, 1.7, 2.75, "RECALL", "93.33%", ORANGE)
metric(s, 9.65, 1.7, 3.0, "WEIGHTED F1", "93.27%", TEAL)
scatter = str(ART / "prediction_scatter.png")
s.shapes.add_picture(scatter, Inches(0.65), Inches(3.25), width=Inches(6.2), height=Inches(3.75))
box(s, 7.2, 3.35, 5.45, 3.45, PALE, PALE, True)
text(s, 7.6, 3.75, 4.5, 0.3, "WHAT THIS DEMONSTRATES", 11, TEAL, True)
bullet_list(s, 7.6, 4.35, 4.5, [
    "Reproducible data preparation",
    "Distance-aware model selection",
    "Multi-metric model validation",
    "Clear error interpretation",
], 17, INK, 0.54)
text(s, 0.75, 7.05, 6.0, 0.2, "Source: executed project artifacts · metrics.json and prediction_scatter.png", 9, MUTED)

# Slide 8: conclusion
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, NAVY)
text(s, 0.75, 0.7, 6.5, 0.3, "07 · CLOSE", 12, TEAL, True)
text(s, 0.75, 1.35, 8.6, 0.8, "A small model, built like a professional system.", 30, WHITE, True)
text(s, 0.78, 2.5, 7.2, 0.75, "This project bridges theory and practice: data understanding, supervised learning, reproducible evaluation, and communication of results.", 18, RGBColor(220, 230, 240))
box(s, 0.78, 4.05, 5.6, 1.55, RGBColor(21, 51, 82), RGBColor(21, 51, 82), True)
text(s, 1.1, 4.35, 4.7, 0.25, "NEXT PRODUCTION STEPS", 11, ORANGE, True)
bullet_list(s, 1.1, 4.8, 4.7, ["Cross-validation and experiment tracking", "API deployment and monitoring", "Data drift and model governance"], 14, RGBColor(220, 230, 240), 0.38)
text(s, 8.2, 4.25, 3.7, 0.4, "Thank you", 29, WHITE, True, PP_ALIGN.CENTER)
text(s, 8.15, 4.95, 3.8, 0.5, "AI Engineer · Data Scientist\nMachine Learning Professional", 16, TEAL, True, PP_ALIGN.CENTER)
text(s, 12.05, 7.12, 0.65, 0.2, "08 / 08", 9, RGBColor(170, 195, 215), True, PP_ALIGN.RIGHT)

prs.save(OUT)
print(f"Saved {OUT}")
