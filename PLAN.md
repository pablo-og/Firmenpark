# Invoice Service Plan - Firmenpark

## Project Overview
- **Project name**: Firmenpark - Rechnungsgenerator
- **Type**: Web application (Flask)
- **Core functionality**: Generate ZUGFeRD invoices for German businesses
- **Target users**: German small businesses, freelancers

## Technical Stack
- Flask (existing)
- Bootstrap 5 (existing)
- SQLite (existing)
- ZUGFeRD PDF generation
- Blueprint structure

## Features

### 1. Invoice Form
- Rechnungsnummer (autoincrement)
- Rechnungsdatum
- Leistungsdatum (optional)
- From: Ihre Firmendaten (from env/config)
- To: Kundendaten
  - Firmenname *
  - Adresse
  - PLZ, Stadt
  - E-Mail (optional)
- Line Items (dynamisch)
  - Beschreibung *
  - Menge *
  - Einzelpreis *
  - MwSt-Satz (19% / 7% / 0%)
- Zwischensumme
- MwSt-Betrag
- Gesamtbetrag (Endpreis)
- Notiz (optional)

### 2. Tax Rates
- 19% (standard)
- 7% (reduced)
- 0% (tax-free)

### 3. ZUGFeRD Output
- PDF file with embedded XML
- German ZUGFeRD 2.1 standard
- Downloads as .pdf file

### 4. Invoice Number
- Stored in database
- Auto-increment on each new invoice
- Configurable prefix (e.g., "RE-2026-")

### 5. Configuration (.env)
```
INVOICE_PREFIX=RE-2026-
INVOICE_START=1001
```

## UI/UX

### Navigation
- Add "Rechnung" link to nav (next to Termin-Generator)

### Invoice Page
- Form with all fields
- Dynamic line items (add/remove)
- Real-time calculation preview
- "Rechnung erstellen" button

### Responsive
- Mobile-friendly form
- Burger menu works

## File Structure
```
firmenpark/
├── app/
│   ├── blueprints/
│   │   ├── main/ (existing)
│   │   └── invoice/ (new)
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── header.html
│   │   ├── nav.html
│   │   ├── footer.html
│   │   └── invoice/
│   │       └── index.html (new)
│   ├── utils/
│   │   ├── ics_generator.py (existing)
│   │   └── invoice_generator.py (new)
│   ├── models.py (add InvoiceCounter)
│   └── config.py (add invoice config)
├── .env (add INvoice settings)
├── .env.example
└── requirements.txt (add reportlab)
```

## Implementation Steps

### Step 1: Setup
- Add `reportlab` to requirements.txt
- Update .env with invoice settings
- Update .env.example

### Step 2: Database
- Add InvoiceCounter model

### Step 3: Blueprint
- Create invoice blueprint
- Add routes (/rechnung)

### Step 4: Templates
- Add nav link
- Create invoice form page

### Step 5: Invoice Generator
- Calculate totals
- Generate ZUGFeRD PDF

### Step 6: Testing
- Test invoice generation
- Verify PDF output

## Acceptance Criteria
- [ ] Invoice form loads at /rechnung
- [ ] Autoincrement works
- [ ] Tax calculation correct
- [ ] ZUGFeRD PDF downloads
- [ ] Responsive on mobile
- [ ] Navigation works
