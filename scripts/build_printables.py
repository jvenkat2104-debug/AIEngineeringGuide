"""Generate three one-page sheets and web versions from one maintained JSON source."""
from pathlib import Path
from xml.sax.saxutils import escape
import json, shutil
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
EDITION="12 November 2026"
WEBSITE="https://jvenkat2104-debug.github.io/"
OUT=ROOT/"output"/"pdf"
OUT.mkdir(parents=True,exist_ok=True)
(ROOT/"content"/"printables").mkdir(exist_ok=True)
styles={
 "title":ParagraphStyle("title",fontName="Helvetica-Bold",fontSize=23,leading=27,textColor=colors.HexColor("#123d4d"),spaceAfter=8),
 "sub":ParagraphStyle("sub",fontSize=10.5,leading=15,textColor=colors.HexColor("#52646b"),spaceAfter=10),
 "head":ParagraphStyle("head",fontName="Helvetica-Bold",fontSize=11,leading=14,textColor=colors.HexColor("#087f74"),spaceBefore=10,spaceAfter=5),
 "body":ParagraphStyle("body",fontSize=10,leading=14,spaceAfter=5),
 "small":ParagraphStyle("small",fontSize=8,leading=11),
}
def footer(canvas,doc):
 canvas.saveState();width,height=A4
 canvas.setStrokeColor(colors.HexColor("#b8d5d1"));canvas.line(38,57,width-38,57)
 canvas.setFont("Helvetica",8);canvas.setFillColor(colors.HexColor("#123d4d"))
 canvas.drawString(38,43,"Engineering Guide for Indian Students | "+WEBSITE.removeprefix("https://"))
 canvas.linkURL(WEBSITE,(38,38,width-38,52),relative=0)
 canvas.setFont("Helvetica",7);canvas.drawString(38,29,"Community draft - Independent review pending | "+EDITION+" | CC BY 4.0 | 1 / 1")
 canvas.restoreState()
for item in json.loads((ROOT/"publishing/printables.json").read_text(encoding="utf-8")):
 story=[Paragraph(escape(item["title"]),styles["title"]),Paragraph(escape(item["subtitle"]),styles["sub"])]
 md=["# "+item["title"],"", "**Level: Beginner**", "", "Status: Draft | Independent review pending | Edition: "+EDITION,"",item["subtitle"],""]
 for heading,bullets in item["sections"]:
  story.append(Paragraph(escape(heading),styles["head"]));md+=['## '+heading,'']
  for bullet in bullets:
   story.append(Paragraph(escape(bullet),styles["body"],bulletText="-"));md+=['- '+bullet]
  md+=['']
 if "table" in item:
  table=item["table"];rows=[[Paragraph(escape(v),styles["small"]) for v in table["headers"]]]
  rows += [[Paragraph(escape(v),styles["small"]),"","",""] for v in table["rows"]]
  t=Table(rows,colWidths=[175,103,103,103],rowHeights=[27]+[31]*len(table["rows"]))
  t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.5,colors.HexColor("#b8c9cd")),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e9f4f2")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),7)]));story += [Spacer(1,10),t]
  md+=['| '+' | '.join(table['headers'])+' |','| --- | --- | --- | --- |']+['| '+v+' | | | |' for v in table['rows']]+['']
 for field in item["fields"]:
  story+=[Spacer(1,9),Paragraph(escape(field)+" ___________________________________________________",styles["body"])]
  md+=[field+' __________________________________________','']
 story += [Spacer(1,12),Paragraph('Use the current guide and official notices before acting. No admission, placement or salary guarantee.',styles["small"])]
 pdf=OUT/(item["slug"]+".pdf")
 doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=38,leftMargin=38,topMargin=36,bottomMargin=73,title=item["title"],author="Engineering Guide for Indian Students contributors")
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 shutil.copy2(pdf,ROOT/"downloads"/pdf.name)
 md+=['[Download the one-page PDF](../../downloads/'+pdf.name+') · [Read the full guide]('+WEBSITE+item['route']+')','', 'Maintained source: publishing/printables.json; web and PDF versions are generated together.']
 (ROOT/"content"/"printables"/(item["slug"]+".md")).write_text('\n'.join(md)+'\n',encoding="utf-8")
 print(pdf)
