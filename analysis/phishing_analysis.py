"""
================================================================================
WHY HUMANS CLICK - Phishing Awareness Behavioural Study

An Ethical Simulated Phishing Study: Assessing Behavioral Susceptibility in an SME Context and the Implementation of a Targeted phishing Awareness

Data Analysis Script
Author: Jesufemi Dada | May 2026
================================================================================
INSTRUCTIONS:
  1. Place both files in the same folder as this script:
        behavioural-survey-responses.csv
        gophish-campaign-results.xlsx
  2. Run: python phishing_analysis.py
  3. Charts saved to /figures subfolder
================================================================================
"""

import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import plotly.graph_objects as go
import json, os

os.makedirs("figures", exist_ok=True)

# LOAD DATA
form = pd.read_csv("behavioural-survey-responses.csv")
form.columns = ["Timestamp","Q1_Busyness","Q2_Stress","Q3_Tasks","Q4_ClickReason","Q5_Confidence"]

gophish = pd.read_excel("gophish-campaign-results.xlsx")
gophish["send_date"]     = pd.to_datetime(gophish["send_date"])
gophish["modified_date"] = pd.to_datetime(gophish["modified_date"])
gophish["mins_to_click"] = (gophish["modified_date"] - gophish["send_date"]).dt.total_seconds() / 60

# CAMPAIGN PERFORMANCE
print("\n=== CAMPAIGN PERFORMANCE ===")
total   = len(gophish)
clicked = gophish[gophish["status"] == "Clicked Link"].copy()
opened  = gophish[gophish["status"] == "Email Opened"]
sent    = gophish[gophish["status"] == "Email Sent"]
print(f"Total participants : {total}")
print(f"Clicked Link       : {len(clicked)} ({len(clicked)/total*100:.1f}%)")
print(f"Opened no click    : {len(opened)}  ({len(opened)/total*100:.1f}%)")
print(f"Sent no open       : {len(sent)}   ({len(sent)/total*100:.1f}%)")
print(f"KnowBe4 SME baseline (1-250 staff): 24.6%")
print(f"This study is {len(clicked)/total*100 / 24.6:.1f}x the industry baseline")

# TIME TO CLICK
print("\n=== TIME-TO-CLICK ===")
def cat(m):
    if m < 5:     return "Impulsive (under 5 mins)"
    elif m < 30:  return "Fast (5 to 30 mins)"
    elif m < 120: return "Delayed (30 mins to 2 hrs)"
    else:         return "Late (over 2 hrs)"

clicked["category"] = clicked["mins_to_click"].apply(cat)
print(f"Mean : {clicked['mins_to_click'].mean():.1f} mins")
print(f"SD   : {clicked['mins_to_click'].std():.1f} mins")
print(f"Min  : {clicked['mins_to_click'].min():.2f} mins")
print(f"Max  : {clicked['mins_to_click'].max():.1f} mins")
print(clicked["category"].value_counts().to_string())

# ORDINAL ENCODING
form["B"] = form["Q1_Busyness"].map({
    "Completely free, nothing else on my mind":1, "Slightly busy":2,
    "Moderately busy":3, "Very busy, juggling multiple things":4,
    "Extremely busy/Overwhelmed":5})
form["S"] = form["Q2_Stress"].map({
    "Very calm and relaxed":1, "Slightly stressed":2, "Moderately stressed":3,
    "Quite stressed":4, "Very stressed":5})
form["T"] = form["Q3_Tasks"].map({
    "Nothing else on my mind":1, "1-2 other tasks":2,
    "3-5 other tasks":3, "More than 5 tasks":4})
form["C"] = form["Q5_Confidence"].map({
    "Not Confident at all":1, "Slightly confident":2, "Moderately confident":3,
    "Quite confident":4, "Extremely confident - I thought i'd never fall for one":5})
form["CogLoad"] = form["B"] + form["S"] + form["T"]

# COGNITIVE LOAD
print("\n=== COGNITIVE LOAD (max=14) ===")
print(f"Mean   : {form['CogLoad'].mean():.2f}")
print(f"Median : {form['CogLoad'].median():.1f}")
print(f"SD     : {form['CogLoad'].std():.2f}")
print(f"Range  : {form['CogLoad'].min()} to {form['CogLoad'].max()}")

# SPEARMAN CORRELATIONS
print("\n=== SPEARMAN CORRELATIONS ===")
rho1,p1 = spearmanr(form["C"], form["CogLoad"])
rho2,p2 = spearmanr(form["C"], form["S"])
rho3,p3 = spearmanr(form["B"], form["T"])
print(f"Confidence vs CogLoad : rho={rho1:.3f}, p={p1:.3f}")
print(f"Confidence vs Stress  : rho={rho2:.3f}, p={p2:.3f}")
print(f"Busyness vs Tasks     : rho={rho3:.3f}, p={p3:.3f}")

# Q4 CLICK REASONS
print("\n=== Q4 CLICK REASONS ===")
reasons = []
for v in form["Q4_ClickReason"]:
    for r in str(v).split(";"):
        reasons.append(r.strip())
for r,c in pd.Series(reasons).value_counts().items():
    print(f"  {c}/11 ({c/11*100:.1f}%)  {r}")

# Q5 OVERCONFIDENCE
print("\n=== Q5 OVERCONFIDENCE PARADOX ===")
print(form["Q5_Confidence"].value_counts().to_string())
oc = form[form["C"] >= 4]
print(f"\nHighly confident yet clicked: {len(oc)}/11 ({len(oc)/11*100:.1f}%)")

# FIGURES
print("\n=== GENERATING FIGURES ===")
BG="white"; GRD="rgba(170,170,170,0.25)"
FNT=dict(family="Arial, sans-serif",size=14,color="#111")
TTF=dict(size=18,color="#111"); AF=dict(size=14,color="#111"); TKF=dict(size=13,color="#111")

def L(title,xt,yt,yr=None):
    d=dict(title=dict(text=title,font=TTF,x=0.5,xanchor="center"),
           plot_bgcolor=BG,paper_bgcolor=BG,font=FNT,
           xaxis=dict(title=dict(text=xt,font=AF),tickfont=TKF,showgrid=False,
                      linecolor="#555",linewidth=1,automargin=True),
           yaxis=dict(title=dict(text=yt,font=AF),tickfont=TKF,
                      gridcolor=GRD,linecolor="#555",linewidth=1),
           margin=dict(l=75,r=55,t=110,b=85))
    if yr: d["yaxis"]["range"]=yr
    return d

def S(fig,name,cap):
    fig.write_image(f"figures/{name}")
    json.dump({"caption":cap},open(f"figures/{name}.meta.json","w"))
    print(f"  Saved: figures/{name}")

# Fig 1: Funnel
fig1=go.Figure(go.Funnel(
    y=["Emails Sent (17)","Opened (16)","Clicked (12)","Form Done (11)","Training Done (9)"],
    x=[17,16,12,11,9],textinfo="value+percent initial",
    textfont=dict(size=14,color="white"),
    marker=dict(color=["#1A5276","#1F618D","#C0392B","#E67E22","#27AE60"])))
fig1.update_layout(title=dict(text="Figure 1: Campaign Engagement Funnel",
    font=TTF,x=0.5,xanchor="center"),plot_bgcolor=BG,paper_bgcolor=BG,font=FNT,
    margin=dict(l=75,r=55,t=100,b=55))
S(fig1,"fig1_funnel.png","Figure 1: Campaign Funnel (n=17)")

# Fig 2: Benchmark
fig2=go.Figure(go.Bar(
    x=["This Study\n(n=17)","KnowBe4 SME\n1-250 Staff","KnowBe4\nAll Orgs"],
    y=[70.6,24.6,33.1],marker_color=["#C0392B","#7F8C8D","#BDC3C7"],
    text=["70.6%","24.6%","33.1%"],textposition="outside",textfont=dict(size=14,color="#111")))
fig2.update_layout(**L("Figure 2: Click Rate vs Industry Benchmarks","Group","Click Rate (%)",[0,85]))
fig2.update_traces(cliponaxis=False)
S(fig2,"fig2_benchmark.png","Figure 2: Click Rate vs KnowBe4 2025 Benchmarks")

# Fig 3: Click Reasons
fig3=go.Figure(go.Bar(x=[6,5,4,2,1],
    y=["Curiosity","Thought Genuine","In a Rush","Official Appearance","Auto-click"],
    orientation="h",marker_color=["#C0392B","#E67E22","#F39C12","#2980B9","#95A5A6"],
    text=["6/11","5/11","4/11","2/11","1/11"],textposition="outside",
    textfont=dict(size=13,color="#111")))
fig3.update_layout(**L("Figure 3: Q4 Click Reasons (Multi-Select, n=11)",
    "Respondents","Click Reason",[0,9]))
fig3.update_layout(yaxis=dict(tickfont=TKF,automargin=True,
    linecolor="#555",linewidth=1,showgrid=False))
fig3.update_traces(cliponaxis=False)
S(fig3,"fig3_reasons.png","Figure 3: Q4 Click Reasons (n=11)")

# Fig 4: Confidence
fig4=go.Figure(go.Bar(
    x=["Slightly\nConfident","Moderately\nConfident","Quite\nConfident","Extremely\nConfident"],
    y=[2,3,5,1],marker_color=["#2ECC71","#F39C12","#E67E22","#C0392B"],
    text=["2/11","3/11","5/11","1/11"],textposition="outside",
    textfont=dict(size=13,color="#111")))
fig4.update_layout(**L("Figure 4: Prior Phishing Detection Confidence (n=11)",
    "Confidence Level","Respondents",[0,7.5]))
fig4.update_traces(cliponaxis=False)
S(fig4,"fig4_confidence.png","Figure 4: Q5 Prior Confidence (n=11)")

# Fig 5: Busyness and Stress
fig5=go.Figure()
fig5.add_trace(go.Bar(name="Busyness (Q1)",
    x=["Slightly Busy","Moderately Busy","Very Busy","Overwhelmed"],y=[3,4,2,2],
    text=["3","4","2","2"],textposition="outside",textfont=dict(size=13,color="#111")))
fig5.add_trace(go.Bar(name="Stress (Q2)",
    x=["Very Calm","Slightly Stressed","Moderately Stressed","Quite Stressed","Very Stressed"],
    y=[3,2,1,3,2],text=["3","2","1","3","2"],textposition="outside",
    textfont=dict(size=13,color="#111")))
fig5.update_layout(barmode="group",
    title=dict(text="Figure 5: Busyness and Stress at Time of Click (n=11)",
    font=TTF,x=0.5,xanchor="center"),
    legend=dict(orientation="h",yanchor="bottom",y=1.05,xanchor="center",x=0.5),
    plot_bgcolor=BG,paper_bgcolor=BG,font=FNT,
    xaxis=dict(title=dict(text="Level",font=AF),tickfont=TKF,
               showgrid=False,linecolor="#555",automargin=True),
    yaxis=dict(title=dict(text="Respondents",font=AF),tickfont=TKF,
               gridcolor=GRD,linecolor="#555",range=[0,6]),
    margin=dict(l=75,r=55,t=130,b=90))
fig5.update_traces(cliponaxis=False)
S(fig5,"fig5_cogload.png","Figure 5: Busyness and Stress at Click (n=11)")

# Fig 6: Time to Click
fig6=go.Figure(go.Bar(
    x=["Under 5 mins\n(Impulsive)","5-30 mins\n(Fast)",
       "30 mins-2 hrs\n(Delayed)","Over 2 hrs\n(Late)"],
    y=[3,1,5,3],marker_color=["#C0392B","#E67E22","#2980B9","#7F8C8D"],
    text=["3","1","5","3"],textposition="outside",textfont=dict(size=14,color="#111")))
fig6.update_layout(**L("Figure 6: Time-to-Click Distribution (n=12)",
    "Time After Email Delivery","Clickers",[0,7]))
fig6.update_traces(cliponaxis=False)
S(fig6,"fig6_timetoclk.png","Figure 6: Time-to-Click Distribution (n=12)")

# Fig 7: Overconfidence Paradox
fig7=go.Figure(go.Bar(
    x=["Slightly\nConfident","Moderately\nConfident","Quite\nConfident","Extremely\nConfident"],
    y=[2,3,5,1],marker_color=["#2ECC71","#F39C12","#E67E22","#C0392B"],
    text=["2/11","3/11","5/11","1/11"],textposition="outside",
    textfont=dict(size=13,color="#111")))
fig7.add_annotation(x=2,y=6.6,
    text="<b>6 of 11 (54.5%) were highly confident yet all clicked</b>",
    showarrow=False,font=dict(size=12,color="#C0392B"),
    bgcolor="white",bordercolor="#C0392B",borderwidth=1,xanchor="center")
fig7.update_layout(**L("Figure 7: The Overconfidence Paradox (n=11)",
    "Pre-Study Confidence","Respondents",[0,8]))
fig7.update_traces(cliponaxis=False)
S(fig7,"fig7_overconfidence.png","Figure 7: Overconfidence Paradox (n=11)")

print("\nDone. All 7 figures saved to /figures folder.")