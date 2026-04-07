---
name: ux-report
description: >
  Generate a professional branded PDF UX/CX audit report from a heuristic evaluation or UX
  analysis. Use this skill whenever the user asks to export, save, or create a report from a
  UX review, usability audit, heuristic evaluation, or CX analysis. Trigger on phrases like
  "generate report", "crea il report", "esporta l'analisi", "fai il PDF", "manda al cliente",
  "documenta questa valutazione". Always use this skill when the output needs to be a
  shareable, formatted document — not just a chat response.
---

# UX Report — Generatore PDF Brandizzato (Metodo.dev)

## Scopo
Trasformare un'analisi UX/CX in un PDF professionale e brandizzato per Metodo.dev,
pronto per essere condiviso con clienti e stakeholder non tecnici.

Tutti i testi del report sono in **italiano**.

---

## Dati aziendali (fissi, non chiedere mai)

```python
COMPANY = {
    "name":      "Metodo di Marri Michele",
    "website":   "https://metodo.dev",
    "piva":      "P.IVA 02784750396",
    "rea":       "REA: 257079",
    "evaluator": "Michele Marri",
}
```

---

## Brand Assets (pre-configurati)

Tutti i file sono in `assets/` relativo a questa skill:

| Asset | File |
|-------|------|
| Logo | `assets/logo.png` |
| Font Light | `assets/Outfit_300Light.ttf` |
| Font Regular | `assets/Outfit_400Regular.ttf` |
| Font Medium | `assets/Outfit_500Medium.ttf` |
| Font SemiBold | `assets/Outfit_600SemiBold.ttf` |
| Font Bold | `assets/Outfit_700Bold.ttf` |

### Color tokens
```python
C_NAVY    = HexColor("#1E1B3A")   # primario — sfondi, titoli
C_RED     = HexColor("#F4450C")   # accento caldo — badge, CTA, accenti
C_MAGENTA = HexColor("#D4006A")   # accento freddo — striscia copertina
C_LIGHT   = HexColor("#F5F7FA")   # sfondi sezioni
C_TEXT    = HexColor("#1E1B3A")   # corpo testo
C_MUTED   = HexColor("#6B7280")   # didascalie, metadati

# Severità opportunità
C_CRITICAL = HexColor("#EF4444")  # CRITICA
C_MAJOR    = HexColor("#F97316")  # IMPORTANTE
C_MODERATE = HexColor("#EAB308")  # MODERATA
C_GOOD     = HexColor("#22C55E")  # punteggi 7-10
```

---

## Input — Cosa raccogliere prima di generare

### Obbligatorio
- **Nome prodotto / schermata**: cosa è stato valutato
- **Contenuto analisi**: da una valutazione `ux-heuristics` nella conversazione,
  oppure da note/descrizione fornite dall'utente

### Opzionale (chiedere solo se non già in conversazione)
- **Nome cliente**: mostrato in copertina
- **Data**: default = oggi

Non chiedere mai il nome del valutatore (è sempre Michele Marri).
Se la conversazione contiene già una valutazione euristica, estrai tutti i dati
direttamente — non chiedere all'utente di ripeterli.

---

## Struttura del Report

### Pagina 0 — Copertina
- Sfondo navy full-bleed
- Logo in alto a sinistra
- Blocco dati aziendali in alto a destra (4 righe: nome, sito, P.IVA, REA)
- Titolo report grande bianco (Outfit Bold 36pt)
- Sottotitolo: nome prodotto/flusso
- Valutatore + data
- Striscia rossa/magenta in fondo

### Pagina 1 — Sintesi Esecutiva
- Paragrafo introduttivo lungo (Outfit Light 11pt, giustificato)
- Box statistiche: Opportunità totali / Critiche / Importanti / Moderate
  - **IMPORTANTE**: il box usa solo divisori verticali, NO linea orizzontale centrale
  - Stile: `LINEAFTER` sulle colonne 0-2, `BOX` esterno, NO `INNERGRID`
- Sottosezioni narrative con titolo SemiBold (es. Punti di forza, Feedback e stati,
  Controllo e reversibilità, Accessibilità)

### Pagina 2 — Punteggi Euristici
- 10 righe, una per euristica (H1–H10)
- Ogni riga: dot colorato | codice | nome | nota | box punteggio
- Box punteggio: rettangolo arrotondato centrato verticalmente, accent bar sinistra,
  numero grande nel colore della scala, "/ 10" sotto
- Scala colori (4 livelli, no blu):
  - 🔴 1–2 `#EF4444` Critico
  - 🟠 3–4 `#F97316` Importante
  - 🟡 5–6 `#EAB308` Moderato
  - 🟢 7–10 `#22C55E` Soddisfacente
- Legenda a fondo pagina (striscia grigio chiaro con dot + label)

### Pagina 3 — Opportunità Prioritarie
- Termine usato: **"opportunità"**, mai "problemi"
- Badge severità: CRITICA / IMPORTANTE / MODERATA (mai "CRITICAL/MAJOR")
- Ogni card è composta da 3 tabelle separate con bordo `#E5E7EB`:
  1. Header: badge colorato (80pt) | codice H (36pt) | titolo
  2. Descrizione: sfondo bianco, padding 16pt, testo giustificato
  3. Raccomandazione: sfondo bianco, testo nel colore della severità, preceduto da "→"
- Tutto sfondo bianco — niente sfondi colorati (stampa pulita)
- Badge centrato verticalmente con `VALIGN MIDDLE` e `ALIGN CENTER`
- 16pt di spazio tra una card e l'altra

### Pagina 4 — Prossimi Passi Raccomandati
- Paragrafo introduttivo con indicazione temporale (prima del lancio / prima iterazione)
- Max 5 passi numerati
- Ogni passo: numero rosso su sfondo rosso | azione in bold + beneficio in grigio
- Sfondo grigio chiaro per la colonna testo

### Pagina 5 — Le 10 Euristiche di Nielsen (memo)
- Tabella compatta con righe alternate bianco/#FAFAFA
- Colonne: codice H (rosso, 36pt) | nome bold + descrizione grigia (8pt)
- Padding ridotto (7pt top/bottom) per stare su una pagina sola
- Fonte in fondo: "Jakob Nielsen, '10 Usability Heuristics...' (1994) — nngroup.com"

---

## Componenti custom (flowables)

### `SectionHeader(text)`
Barra accent rossa 4px + titolo navy 14pt. Usare per ogni sezione.

### `HeuristicScoreRow(code, name, score, note, width)`
Riga completa 44pt di altezza con:
- Dot colorato (radius 6) centrato verticalmente
- Codice H in alto, nome in basso (SemiBold 10pt)
- Nota right-aligned con margine prima del box
- Box punteggio: `BOX_W=44, BOX_H=30`, centrato su `(self.height - BOX_H) / 2`

### `HeuristicLegend(width)`
Striscia grigia 28pt con 4 dot + label per la scala colori.

---

## Istruzioni per la generazione

### Usa il template pre-costruito
Il template completo è in `scripts/template.py`. Leggerlo sempre come base —
non ricostruire da zero.

### Per generare un report reale:
1. Leggere `scripts/template.py` per caricare tutti gli helper e gli stili
2. Sostituire i dati di esempio con i dati reali dalla conversazione
3. Assemblare la lista `story` seguendo la struttura sopra
4. Chiamare `doc.build(story)` con il path di output corretto

### Path degli asset
```python
import os
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(SKILL_DIR, "..", "assets")
LOGO   = os.path.join(ASSETS, "logo.png")
```

### Path di output
```python
output = f"/mnt/user-data/outputs/ux-report-{nome-prodotto-kebab}.pdf"
```

---

## Margini e layout pagine interne

```python
MARGIN      = 2 * cm
header_bar  = 1.2 * cm   # banda navy in cima
footer_bar  = 1.8 * cm   # spazio footer
top_padding = 0.8 * cm   # respiro extra tra banda e contenuto

inner_frame = Frame(
    MARGIN, 1.8*cm,
    W - 2*MARGIN,
    H - 1.2*cm - 2.6*cm,   # = header + top_padding
    id='inner'
)
```

Header pagine interne: logo sinistra + titolo report destra (grigio chiaro).
Footer: "Metodo di Marri Michele — https://metodo.dev" sinistra + "Pagina N" destra.

---

## Terminologia italiana obbligatoria

| ❌ Non usare | ✅ Usare |
|-------------|---------|
| Problemi | Opportunità |
| CRITICAL | CRITICA |
| MAJOR | IMPORTANTE |
| MODERATE | MODERATA |
| Issues found | Opportunità totali |
| Next Steps | Prossimi Passi Raccomandati |
| Executive Summary | Sintesi Esecutiva |
| Priority Issues | Opportunità Prioritarie |

---

## Dopo la generazione
Presentare il file con una riga di riepilogo:
"[N] opportunità documentate su [M] euristiche. Report pronto per la condivisione."
