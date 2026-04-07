from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Flowable
import os
from datetime import date

# ── ASSETS ───────────────────────────────────────────────────────────────────
ASSETS = "/home/claude/ux-report/assets"
LOGO   = os.path.join(ASSETS, "logo.png")

# ── REGISTER FONTS ───────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("Outfit-Light",    os.path.join(ASSETS, "Outfit_300Light.ttf")))
pdfmetrics.registerFont(TTFont("Outfit",          os.path.join(ASSETS, "Outfit_400Regular.ttf")))
pdfmetrics.registerFont(TTFont("Outfit-Medium",   os.path.join(ASSETS, "Outfit_500Medium.ttf")))
pdfmetrics.registerFont(TTFont("Outfit-SemiBold", os.path.join(ASSETS, "Outfit_600SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("Outfit-Bold",     os.path.join(ASSETS, "Outfit_700Bold.ttf")))

# ── BRAND TOKENS ─────────────────────────────────────────────────────────────
C_NAVY    = HexColor("#1E1B3A")
C_RED     = HexColor("#F4450C")
C_MAGENTA = HexColor("#D4006A")
C_LIGHT   = HexColor("#F5F7FA")
C_TEXT    = HexColor("#1E1B3A")
C_MUTED   = HexColor("#6B7280")

C_CRITICAL = HexColor("#EF4444")
C_MAJOR    = HexColor("#F97316")
C_MODERATE = HexColor("#EAB308")
C_GOOD     = HexColor("#22C55E")

W, H   = A4
MARGIN = 2 * cm

# ── COMPANY (fisso) ───────────────────────────────────────────────────────────
COMPANY = {
    "name":      "Metodo di Marri Michele",
    "website":   "https://metodo.dev",
    "piva":      "P.IVA 02784750396",
    "rea":       "REA: 257079",
    "evaluator": "Michele Marri",
}

# ── STYLES ───────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "cover_title": ParagraphStyle("cover_title",
            fontName="Outfit-Bold", fontSize=36, textColor=white,
            leading=44, spaceAfter=10),
        "cover_sub": ParagraphStyle("cover_sub",
            fontName="Outfit-Light", fontSize=16, textColor=HexColor("#E0E0F0"),
            leading=22, spaceAfter=8),
        "cover_meta": ParagraphStyle("cover_meta",
            fontName="Outfit", fontSize=11, textColor=HexColor("#B0AEC8"),
            leading=17),
        "body": ParagraphStyle("body",
            fontName="Outfit", fontSize=10, textColor=C_TEXT,
            leading=17, spaceAfter=8, alignment=TA_JUSTIFY),
        "body_intro": ParagraphStyle("body_intro",
            fontName="Outfit-Light", fontSize=11, textColor=C_TEXT,
            leading=18, spaceAfter=10, alignment=TA_JUSTIFY),
        "subsection": ParagraphStyle("subsection",
            fontName="Outfit-SemiBold", fontSize=11, textColor=C_NAVY,
            spaceBefore=14, spaceAfter=4),
        "issue_title": ParagraphStyle("issue_title",
            fontName="Outfit-SemiBold", fontSize=11, textColor=C_NAVY,
            spaceAfter=3),
        "issue_body": ParagraphStyle("issue_body",
            fontName="Outfit", fontSize=9.5, textColor=C_TEXT,
            leading=15, spaceAfter=4),
        "rec": ParagraphStyle("rec",
            fontName="Outfit-Medium", fontSize=9.5, textColor=C_RED,
            leading=14),
        "body_muted": ParagraphStyle("body_muted",
            fontName="Outfit-Light", fontSize=9, textColor=C_MUTED, leading=14),
        "h2": ParagraphStyle("h2",
            fontName="Outfit-SemiBold", fontSize=12, textColor=C_NAVY,
            spaceBefore=10, spaceAfter=4),
    }

S = make_styles()

# ── CUSTOM FLOWABLES ──────────────────────────────────────────────────────────
class SectionHeader(Flowable):
    def __init__(self, text, width=W - 2 * MARGIN):
        Flowable.__init__(self)
        self.text  = text
        self._width = width
        self.height = 32

    def draw(self):
        c = self.canv
        c.setFillColor(C_RED)
        c.rect(0, 4, 4, 22, fill=1, stroke=0)
        c.setFillColor(C_NAVY)
        c.setFont("Outfit-Bold", 14)
        c.drawString(12, 8, self.text)

class HeuristicScoreRow(Flowable):
    SCORE_BG  = {(1,2): HexColor("#FEF2F2"), (3,4): HexColor("#FFF7ED"),
                 (5,6): HexColor("#FEFCE8"), (7,8): HexColor("#F0FDF4"),
                 (9,10): HexColor("#F0FDF4")}
    SCORE_DOT = {(1,2): C_CRITICAL, (3,4): C_MAJOR,
                 (5,6): HexColor("#EAB308"), (7,8): C_GOOD,
                 (9,10): C_GOOD}

    def __init__(self, code, name, score, note, row_width):
        Flowable.__init__(self)
        self.code = code; self.name = name
        self.score = score; self.note = note
        self.width = row_width; self.height = 44

    def _bg(self):
        for rng, c in self.SCORE_BG.items():
            if rng[0] <= self.score <= rng[1]: return c
        return C_LIGHT

    def _dot(self):
        for rng, c in self.SCORE_DOT.items():
            if rng[0] <= self.score <= rng[1]: return c
        return C_MUTED

    def draw(self):
        c = self.canv
        # background
        c.setFillColor(self._bg())
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # colored dot — vertically centered
        c.setFillColor(self._dot())
        c.circle(14, 22, 6, fill=1, stroke=0)
        # H code
        c.setFillColor(C_MUTED); c.setFont("Outfit-Bold", 8)
        c.drawString(28, 28, self.code)
        # heuristic name
        c.setFillColor(C_NAVY); c.setFont("Outfit-SemiBold", 10)
        c.drawString(28, 14, self.name)
        # score block — colored rounded rect, fully centered
        BOX_W, BOX_H = 44, 30
        BOX_X = self.width - BOX_W - 8          # 8pt right padding
        BOX_Y = (self.height - BOX_H) / 2       # vertically centered
        # light tinted background
        import re
        from reportlab.lib.colors import HexColor as HC
        dot_color = self._dot()
        # draw rounded rect with dot color at low opacity via light bg
        c.setFillColor(self._bg())
        c.roundRect(BOX_X, BOX_Y, BOX_W, BOX_H, 6, fill=1, stroke=0)
        # colored left accent bar on the box
        c.setFillColor(dot_color)
        c.roundRect(BOX_X, BOX_Y, 4, BOX_H, 2, fill=1, stroke=0)
        # score number — centered in box
        c.setFillColor(dot_color); c.setFont("Outfit-Bold", 15)
        c.drawCentredString(BOX_X + BOX_W / 2 + 2, BOX_Y + BOX_H / 2 + 1, str(self.score))
        # "/ 10" — small, below number, centered
        c.setFillColor(C_MUTED); c.setFont("Outfit-Light", 7)
        c.drawCentredString(BOX_X + BOX_W / 2 + 2, BOX_Y + 4, "/ 10")
        # note — right-aligned, ends before score box
        NOTE_MAX_RIGHT = BOX_X - 10
        c.setFillColor(C_MUTED); c.setFont("Outfit-Light", 9)
        c.drawRightString(NOTE_MAX_RIGHT, self.height / 2 - 4, self.note[:50])


class HeuristicLegend(Flowable):
    """Legenda colori a fondo pagina euristici."""
    ITEMS = [
        (HexColor("#EF4444"), "1–2  Critico"),
        (HexColor("#F97316"), "3–4  Importante"),
        (HexColor("#EAB308"), "5–6  Moderato"),
        (HexColor("#22C55E"), "7–10  Soddisfacente"),
    ]
    def __init__(self, width):
        Flowable.__init__(self)
        self.width  = width
        self.height = 28

    def draw(self):
        c = self.canv
        # background strip
        c.setFillColor(HexColor("#F5F7FA"))
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        # label
        c.setFillColor(HexColor("#6B7280")); c.setFont("Outfit-SemiBold", 8)
        c.drawString(12, 10, "LEGENDA:")
        # items evenly spaced
        item_w = (self.width - 90) / len(self.ITEMS)
        x = 90
        for color, label in self.ITEMS:
            # dot
            c.setFillColor(color)
            c.circle(x + 6, 14, 5, fill=1, stroke=0)
            # label
            c.setFillColor(HexColor("#1E1B3A")); c.setFont("Outfit", 8)
            c.drawString(x + 15, 10, label)
            x += item_w

# ── PAGE TEMPLATES ────────────────────────────────────────────────────────────
def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(C_RED)
    canvas.rect(0, 0, W, 6, fill=1, stroke=0)
    canvas.setFillColor(C_MAGENTA)
    canvas.rect(W * 0.4, 0, W * 0.6, 6, fill=1, stroke=0)
    canvas.drawImage(LOGO, MARGIN, H - MARGIN - 1.4*cm,
                     width=5.5*cm, height=1.4*cm,
                     preserveAspectRatio=True, mask='auto')
    line_h = 0.42*cm
    y = H - MARGIN - 0.1*cm
    for font, size, text in [
        ("Outfit-SemiBold", 9,  COMPANY["name"]),
        ("Outfit-Light",    8,  COMPANY["website"]),
        ("Outfit-Light",    8,  COMPANY["piva"]),
        ("Outfit-Light",    8,  COMPANY["rea"]),
    ]:
        canvas.setFont(font, size)
        canvas.setFillColor(HexColor("#B0AEC8"))
        canvas.drawRightString(W - MARGIN, y, text)
        y -= line_h
    canvas.restoreState()

def inner_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, H - 1.2*cm, W, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(C_RED)
    canvas.rect(0, H - 1.2*cm, 4, 1.2*cm, fill=1, stroke=0)
    canvas.drawImage(LOGO, MARGIN, H - 1.1*cm,
                     width=3.5*cm, height=0.85*cm,
                     preserveAspectRatio=True, mask='auto')
    canvas.setFont("Outfit-Light", 8)
    canvas.setFillColor(HexColor("#B0AEC8"))
    canvas.drawRightString(W - MARGIN, H - 0.85*cm, doc.report_title)
    canvas.setStrokeColor(C_LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.4*cm, W - MARGIN, 1.4*cm)
    canvas.setFont("Outfit-Light", 8)
    canvas.setFillColor(C_MUTED)
    canvas.drawString(MARGIN, 0.9*cm,
                      f"{COMPANY['name']} — {COMPANY['website']}")
    canvas.drawRightString(W - MARGIN, 0.9*cm, f"Pagina {doc.page}")
    canvas.restoreState()

# ── DOCUMENT BUILDER ─────────────────────────────────────────────────────────
class UXReportDoc(BaseDocTemplate):
    def __init__(self, filename, report_title, **kwargs):
        self.report_title = report_title
        BaseDocTemplate.__init__(self, filename, **kwargs)
        cover_frame = Frame(MARGIN, MARGIN, W - 2*MARGIN, H - 2*MARGIN, id='cover')
        inner_frame = Frame(MARGIN, 1.8*cm, W - 2*MARGIN,
                            H - 1.2*cm - 1.8*cm - 0.8*cm, id='inner')
        self.addPageTemplates([
            PageTemplate(id='Cover', frames=cover_frame, onPage=cover_page),
            PageTemplate(id='Inner', frames=inner_frame, onPage=inner_page),
        ])

# ── BUILD ─────────────────────────────────────────────────────────────────────
def build_sample_report(output_path):
    from reportlab.platypus import NextPageTemplate, PageBreak
    today = date.today().strftime("%d %B %Y")

    doc = UXReportDoc(output_path,
                      report_title="Analisi UX — App di esempio",
                      pagesize=A4,
                      leftMargin=MARGIN, rightMargin=MARGIN,
                      topMargin=MARGIN, bottomMargin=MARGIN)
    story = []

    # ════════════════════════════════════════════════════════════════
    # COPERTINA
    # ════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 3.5*cm))
    story.append(Paragraph("Analisi UX", S["cover_title"]))
    story.append(Paragraph("App di esempio — Flusso di pagamento", S["cover_sub"]))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(f"Preparato da {COMPANY['name']} · {today}", S["cover_meta"]))
    story.append(Paragraph(f"Valutatore: {COMPANY['evaluator']}", S["cover_meta"]))
    story.append(NextPageTemplate("Inner"))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGINA 1 — SINTESI ESECUTIVA
    # ════════════════════════════════════════════════════════════════
    story.append(SectionHeader("Sintesi Esecutiva"))
    story.append(Spacer(1, 0.35*cm))

    # Paragrafo introduttivo
    story.append(Paragraph(
        "L'analisi ha preso in esame il flusso di pagamento dell'applicazione, valutando "
        "l'esperienza utente dall'aggiunta al carrello fino alla conferma dell'ordine. "
        "Nel complesso, l'interfaccia presenta una base visiva solida e un linguaggio "
        "accessibile, ma emergono alcune aree di miglioramento significative che, se affrontate, "
        "possono ridurre l'abbandono e aumentare la fiducia dell'utente nelle fasi critiche "
        "dell'acquisto. Sono state identificate 7 opportunita' di miglioramento su 10 euristiche "
        "di usabilita', di cui 2 richiedono intervento prioritario prima del lancio.",
        S["body_intro"]))

    # Box statistiche
    col_w = (W - 2*MARGIN) / 4
    stats = [
        [Paragraph("7",  ParagraphStyle("sn", fontName="Outfit-Bold", fontSize=28,
                   textColor=C_RED, alignment=TA_CENTER)),
         Paragraph("2",  ParagraphStyle("sn", fontName="Outfit-Bold", fontSize=28,
                   textColor=C_CRITICAL, alignment=TA_CENTER)),
         Paragraph("3",  ParagraphStyle("sn", fontName="Outfit-Bold", fontSize=28,
                   textColor=C_MAJOR, alignment=TA_CENTER)),
         Paragraph("2",  ParagraphStyle("sn", fontName="Outfit-Bold", fontSize=28,
                   textColor=HexColor("#EAB308"), alignment=TA_CENTER))],
        [Paragraph("Opportunita' totali", ParagraphStyle("sl", fontName="Outfit-Light",
                   fontSize=9, textColor=C_MUTED, alignment=TA_CENTER)),
         Paragraph("Critiche",            ParagraphStyle("sl", fontName="Outfit-Light",
                   fontSize=9, textColor=C_MUTED, alignment=TA_CENTER)),
         Paragraph("Importanti",          ParagraphStyle("sl", fontName="Outfit-Light",
                   fontSize=9, textColor=C_MUTED, alignment=TA_CENTER)),
         Paragraph("Moderate",            ParagraphStyle("sl", fontName="Outfit-Light",
                   fontSize=9, textColor=C_MUTED, alignment=TA_CENTER))],
    ]
    t = Table(stats, colWidths=[col_w]*4)
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), C_LIGHT),
        ('BOX',          (0,0), (-1,-1), 0.5, HexColor("#E5E7EB")),
        ('LINEAFTER',    (0,0), (2,-1),  0.5, HexColor("#E5E7EB")),  # vertical dividers only
        ('TOPPADDING',   (0,0), (-1,-1), 10),
        ('BOTTOMPADDING',(0,0), (-1,-1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    # Sottosezioni della sintesi
    story.append(Paragraph("Punti di forza", S["subsection"]))
    story.append(Paragraph(
        "Il design visivo e' pulito e coerente nelle schermate principali. "
        "Il linguaggio adottato e' comprensibile e vicino al mondo dell'utente, "
        "con etichette chiare e un layout che riduce al minimo le distrazioni. "
        "Le opzioni disponibili sono sempre visibili senza richiedere di memorizzare "
        "percorsi o comandi, il che abbassa significativamente il carico cognitivo "
        "nelle fasi di navigazione ordinaria.",
        S["body"]))

    story.append(Paragraph("Feedback e stati di sistema", S["subsection"]))
    story.append(Paragraph(
        "L'area piu' critica riguarda la mancanza di feedback visivo durante le operazioni "
        "asincrone, in particolare nel momento del pagamento. L'assenza di uno stato di "
        "caricamento lascia l'utente in una condizione di incertezza che puo' portare a "
        "interazioni ripetute e, nei casi piu' gravi, a transazioni duplicate. "
        "Analogamente, i messaggi di errore attualmente presenti non forniscono indicazioni "
        "sufficienti per comprendere la causa del fallimento ne' per procedere autonomamente "
        "alla risoluzione.",
        S["body"]))

    story.append(Paragraph("Controllo e reversibilita'", S["subsection"]))
    story.append(Paragraph(
        "Una volta avviato il flusso di checkout, l'utente non ha la possibilita' di "
        "modificare il contenuto del carrello senza abbandonare la pagina e perdere i dati "
        "gia' inseriti. Manca inoltre una schermata di riepilogo prima della conferma "
        "definitiva, il che priva l'utente dell'opportunita' di verificare i propri dati "
        "prima di completare un'azione irreversibile come il pagamento.",
        S["body"]))

    story.append(Paragraph("Accessibilita' e inclusivita'", S["subsection"]))
    story.append(Paragraph(
        "Non sono stati rilevati problemi gravi di accessibilita'. Il contrasto cromatico "
        "e' adeguato nella maggior parte delle schermate, e le dimensioni dei target di "
        "tocco risultano conformi alle linee guida WCAG 2.1. Si segnala tuttavia l'assenza "
        "di un'opzione di checkout come ospite, che costituisce una barriera rilevante per "
        "gli utenti che accedono per la prima volta e non desiderano registrarsi.",
        S["body"]))

    # Forza pagina 2
    story.append(NextPageTemplate("Inner"))
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════════
    # PAGINA 2 — PUNTEGGI EURISTICI + OPPORTUNITA'
    # ════════════════════════════════════════════════════════════════
    story.append(SectionHeader("Punteggi Euristici"))
    story.append(Spacer(1, 0.3*cm))

    heuristics = [
        ("H1",  "Visibilita' dello stato del sistema",   4,  "Nessun indicatore durante il pagamento"),
        ("H2",  "Corrispondenza col mondo reale",        8,  "Linguaggio chiaro e comprensibile"),
        ("H3",  "Controllo e liberta' dell'utente",      3,  "Impossibile modificare il carrello"),
        ("H4",  "Coerenza e standard",                   7,  "Lievi incoerenze nei pulsanti"),
        ("H5",  "Prevenzione degli errori",              2,  "Nessuna schermata di conferma acquisto"),
        ("H6",  "Riconoscimento anziche' ricordo",       8,  "Opzioni visibili e ben etichettate"),
        ("H7",  "Flessibilita' ed efficienza d'uso",     6,  "Nessun checkout come ospite"),
        ("H8",  "Design estetico e minimalista",         9,  "Layout pulito, poche distrazioni"),
        ("H9",  "Gestione e recupero degli errori",      3,  "Messaggi di errore vaghi e inutili"),
        ("H10", "Guida e documentazione",                7,  "FAQ accessibile ma non contestuale"),
    ]
    aw = W - 2*MARGIN
    for code_h, name, score, note in heuristics:
        story.append(HeuristicScoreRow(code_h, name, score, note, aw))
        story.append(Spacer(1, 4))

    # Legenda a fondo pagina
    story.append(Spacer(1, 0.5*cm))
    story.append(HeuristicLegend(aw))

    # Pagina dedicata per le opportunità
    story.append(NextPageTemplate("Inner"))
    story.append(PageBreak())
    story.append(SectionHeader("Opportunita' Prioritarie"))
    story.append(Spacer(1, 0.3*cm))

    opps = [
        ("CRITICA",    "H5", "Aggiungere una schermata di conferma acquisto",
         "L'utente puo' completare un acquisto accidentalmente senza poter rivedere i dettagli. "
         "Un tap errato su 'Paga ora' avvia una transazione irreversibile.",
         "Inserire una schermata di riepilogo ordine prima della conferma definitiva del pagamento."),
        ("CRITICA",    "H1", "Introdurre feedback visivo durante l'elaborazione del pagamento",
         "Dopo aver tappato 'Paga ora' lo schermo si blocca senza alcun indicatore di caricamento. "
         "L'utente non sa se l'azione e' stata registrata e rischia di premere piu' volte.",
         "Aggiungere uno spinner di caricamento e disabilitare il pulsante durante l'elaborazione."),
        ("IMPORTANTE", "H3", "Consentire la modifica del carrello dal checkout",
         "Una volta nel checkout, l'utente deve tornare indietro perdendo tutti i dati inseriti.",
         "Integrare un riepilogo carrello modificabile direttamente all'interno del flusso di checkout."),
        ("IMPORTANTE", "H9", "Rendere i messaggi di errore specifici e azionabili",
         "Il messaggio attuale recita solo 'Pagamento fallito. Riprova.' senza indicazioni utili.",
         "Mostrare la causa specifica (CVV errato, carta scaduta) con i passi concreti per risolvere."),
    ]

    sev_colors = {"CRITICA": C_CRITICAL, "IMPORTANTE": C_MAJOR, "MODERATA": C_MODERATE}
    sev_bg     = {"CRITICA": HexColor("#FEF2F2"), "IMPORTANTE": HexColor("#FFF7ED"),
                  "MODERATA": HexColor("#FEFCE8")}

    for sev, hcode, title, desc, rec in opps:
        b_col = sev_colors.get(sev, C_MUTED)
        BORDER = HexColor("#E5E7EB")
        WHITE  = HexColor("#FFFFFF")

        # ── Header: badge | hcode | title ──────────────────────────────
        header_row = Table(
            [[Paragraph(sev, ParagraphStyle("bt",
                  fontName="Outfit-Bold", fontSize=7, textColor=white,
                  alignment=TA_CENTER, leading=9)),
              Paragraph(hcode, ParagraphStyle("hc",
                  fontName="Outfit-Bold", fontSize=10, textColor=b_col)),
              Paragraph(title, ParagraphStyle("it",
                  fontName="Outfit-Bold", fontSize=11, textColor=C_NAVY))]],
            colWidths=[80, 36, aw - 116]
        )
        header_row.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (0,0),   b_col),
            ('BACKGROUND',    (1,0), (-1,0),  WHITE),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN',         (0,0), (0,0),   'CENTER'),
            ('TOPPADDING',    (0,0), (0,0),   12),
            ('BOTTOMPADDING', (0,0), (0,0),   12),
            ('TOPPADDING',    (1,0), (-1,0),  12),
            ('BOTTOMPADDING', (1,0), (-1,0),  12),
            ('LEFTPADDING',   (0,0), (0,0),   8),
            ('RIGHTPADDING',  (0,0), (0,0),   8),
            ('LEFTPADDING',   (1,0), (1,0),   14),
            ('LEFTPADDING',   (2,0), (2,0),   4),
            ('RIGHTPADDING',  (2,0), (2,0),   14),
            ('LINEBELOW',     (0,0), (-1,-1), 0.5, BORDER),
            ('BOX',           (0,0), (-1,-1), 0.5, BORDER),
        ]))

        # ── Description ────────────────────────────────────────────────
        desc_row = Table(
            [[Paragraph(desc, ParagraphStyle("ib",
                fontName="Outfit", fontSize=9.5, textColor=C_TEXT,
                leading=16, alignment=TA_JUSTIFY))]],
            colWidths=[aw]
        )
        desc_row.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), WHITE),
            ('TOPPADDING',    (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING',   (0,0), (-1,-1), 16),
            ('RIGHTPADDING',  (0,0), (-1,-1), 16),
            ('BOX',           (0,0), (-1,-1), 0.5, BORDER),
        ]))

        # ── Recommendation ──────────────────────────────────────────────
        rec_row = Table(
            [[Paragraph(f"→  {rec}", ParagraphStyle("ir",
                fontName="Outfit-SemiBold", fontSize=9.5, textColor=b_col,
                leading=15))]],
            colWidths=[aw]
        )
        rec_row.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), WHITE),
            ('TOPPADDING',    (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING',   (0,0), (-1,-1), 16),
            ('RIGHTPADDING',  (0,0), (-1,-1), 16),
            ('BOX',           (0,0), (-1,-1), 0.5, BORDER),
            ('LINEABOVE',     (0,0), (-1,0),  0.5, BORDER),
        ]))

        story.append(KeepTogether([header_row, desc_row, rec_row]))
        story.append(Spacer(1, 16))

    # ════════════════════════════════════════════════════════════════
    # PAGINA 3 — PROSSIMI PASSI (pagina dedicata)
    # ════════════════════════════════════════════════════════════════
    story.append(NextPageTemplate("Inner"))
    story.append(PageBreak())

    story.append(SectionHeader("Prossimi Passi Raccomandati"))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Le seguenti azioni sono ordinate per impatto atteso sull'esperienza utente. "
        "Si consiglia di affrontare le prime due prima del lancio, "
        "e le restanti nella prima iterazione successiva al rilascio.",
        S["body"]))
    story.append(Spacer(1, 0.4*cm))

    next_steps = [
        ("1", "Aggiungere una schermata di conferma acquisto",
               "Previene transazioni accidentali — intervento con il massimo impatto."),
        ("2", "Implementare stati di caricamento per tutte le azioni asincrone",
               "Elimina l'incertezza dell'utente nei momenti piu' critici del flusso."),
        ("3", "Riscrivere i messaggi di errore con indicazioni specifiche e azionabili",
               "Riduce le richieste di supporto e migliora il tasso di recupero autonomo."),
        ("4", "Consentire la modifica del carrello all'interno del checkout",
               "Riduce l'abbandono da parte degli utenti che devono cambiare articoli."),
        ("5", "Aggiungere l'opzione di checkout come ospite",
               "Rimuove il freno per i nuovi acquirenti che non vogliono registrarsi."),
    ]

    for num, action, benefit in next_steps:
        row = Table(
            [[Paragraph(num, ParagraphStyle("step_num",
                fontName="Outfit-Bold", fontSize=13, textColor=white,
                alignment=TA_CENTER)),
              Paragraph(f"<b>{action}</b><br/><font color='#6B7280'>{benefit}</font>",
                ParagraphStyle("step_text", fontName="Outfit", fontSize=10,
                    textColor=C_NAVY, leading=15))]],
            colWidths=[30, aw - 30]
        )
        row.setStyle(TableStyle([
            ('BACKGROUND',   (0,0), (0,0), C_RED),
            ('BACKGROUND',   (1,0), (1,0), C_LIGHT),
            ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING',   (0,0), (-1,-1), 10),
            ('BOTTOMPADDING',(0,0), (-1,-1), 10),
            ('LEFTPADDING',  (1,0), (1,0), 12),
            ('LINEBELOW',    (0,0), (-1,-1), 0.5, white),
        ]))
        story.append(row)


    # ════════════════════════════════════════════════════════════════
    # PAGINA FINALE — LE 10 EURISTICHE DI NIELSEN
    # ════════════════════════════════════════════════════════════════
    story.append(NextPageTemplate("Inner"))
    story.append(PageBreak())

    story.append(SectionHeader("Le 10 Euristiche di Nielsen"))
    story.append(Spacer(1, 0.15*cm))
    story.append(Paragraph(
        "Principi fondamentali dell'usabilita' sviluppati da Jakob Nielsen (1994), "
        "riferimento standard per la valutazione dell'esperienza utente.",
        ParagraphStyle("nielsen_intro", fontName="Outfit-Light", fontSize=8.5,
            textColor=C_MUTED, leading=13, spaceAfter=8)))

    nielsen = [
        ("H1",  "Visibilita' dello stato del sistema",
         "Il sistema deve sempre informare gli utenti su cosa sta accadendo, "
         "con feedback appropriato in tempi ragionevoli."),
        ("H2",  "Corrispondenza tra sistema e mondo reale",
         "Parlare il linguaggio dell'utente, con parole e concetti familiari, "
         "seguendo le convenzioni del mondo reale."),
        ("H3",  "Controllo e liberta' dell'utente",
         "Offrire sempre una via di uscita chiara per abbandonare uno stato "
         "indesiderato senza dover percorrere strade lunghe."),
        ("H4",  "Coerenza e standard",
         "Gli utenti non devono chiedersi se parole o azioni diverse significhino "
         "la stessa cosa. Seguire le convenzioni di piattaforma."),
        ("H5",  "Prevenzione degli errori",
         "Un design attento che previene il problema a monte vale piu' di qualsiasi "
         "messaggio di errore. Eliminare condizioni di errore o chiedere conferma."),
        ("H6",  "Riconoscimento anziche' ricordo",
         "Ridurre il carico cognitivo rendendo visibili oggetti e opzioni. "
         "L'utente non deve ricordare informazioni da uno step all'altro."),
        ("H7",  "Flessibilita' ed efficienza d'uso",
         "Acceleratori per gli utenti esperti che velocizzano l'interazione, "
         "mantenendo il sistema accessibile anche ai nuovi utenti."),
        ("H8",  "Design estetico e minimalista",
         "Le interfacce non devono contenere elementi irrilevanti: ogni componente "
         "in piu' riduce la visibilita' delle informazioni importanti."),
        ("H9",  "Supporto nel riconoscere e correggere gli errori",
         "I messaggi di errore devono usare linguaggio semplice, indicare il problema "
         "con precisione e suggerire una soluzione concreta."),
        ("H10", "Guida e documentazione",
         "Anche se il sistema ideale non richiede spiegazioni, e' necessario fornire "
         "documentazione facile da trovare, concisa e orientata all'azione."),
    ]

    BORDER = HexColor("#E5E7EB")
    for i, (code_n, name, desc) in enumerate(nielsen):
        bg_row = HexColor("#FAFAFA") if i % 2 == 0 else HexColor("#FFFFFF")
        row = Table(
            [[Paragraph(code_n, ParagraphStyle("nc",
                  fontName="Outfit-Bold", fontSize=9, textColor=C_RED,
                  alignment=TA_CENTER, leading=11)),
              Paragraph(f"<b>{name}</b><br/>"
                        f"<font name='Outfit' size='8' color='#6B7280'>{desc}</font>",
                  ParagraphStyle("nd", fontName="Outfit", fontSize=8,
                      textColor=C_NAVY, leading=12))]],
            colWidths=[36, aw - 36]
        )
        row.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), bg_row),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING',    (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING',   (0,0), (0,0),   8),
            ('RIGHTPADDING',  (0,0), (0,0),   8),
            ('LEFTPADDING',   (1,0), (1,0),   12),
            ('RIGHTPADDING',  (1,0), (1,0),   12),
            ('LINEBELOW',     (0,0), (-1,-1), 0.5, BORDER),
            ('LINEBEFORE',    (0,0), (0,-1),  0.5, BORDER),
            ('LINEAFTER',     (-1,0), (-1,-1), 0.5, BORDER),
            ('LINEABOVE',     (0,0), (-1,0),  0.5, BORDER) if i == 0 else ('TOPPADDING', (0,0), (-1,-1), 7),
        ]))
        story.append(row)

    # Fonte
    story.append(Spacer(1, 0.25*cm))
    story.append(Paragraph(
        "Fonte: Jakob Nielsen, '10 Usability Heuristics for User Interface Design' (1994) — nngroup.com",
        ParagraphStyle("source", fontName="Outfit-Light", fontSize=7.5,
            textColor=C_MUTED, leading=11)))

    doc.build(story)
    print(f"Report generato: {output_path}")

if __name__ == "__main__":
    build_sample_report("/mnt/user-data/outputs/ux-report-sample.pdf")
