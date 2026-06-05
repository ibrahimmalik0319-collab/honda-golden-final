import streamlit as st
import sqlite3
import json
import smtplib
from email.message import EmailMessage

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Golden Honda Showroom", layout="centered", page_icon="🏍️")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .main, .block-container {
    background-color: #080808 !important;
    color: #F0EDE8 !important;
    font-family: 'Outfit', sans-serif !important;
}

.block-container {
    padding: 1rem 1rem 4rem !important;
    max-width: 100% !important;
}

/* ─── HIDE SIDEBAR COMPLETELY ─── */
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"]  { display: none !important; }

/* ─── TOP NAV ─── */
.topnav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #0D0D0D;
    border: 1px solid #1E1E1E;
    border-radius: 14px;
    padding: 0.7rem 1.2rem;
    margin-bottom: 1.2rem;
    gap: 1rem;
    flex-wrap: wrap;
}
.topnav-brand {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: #DC0000;
    letter-spacing: 0.08em;
    white-space: nowrap;
}
.topnav-brand span { color: #555; font-size: 0.65rem; letter-spacing: 0.15em; font-family: 'Outfit',sans-serif; display:block; margin-top:-4px; }

/* ─── STREAMLIT SELECT for nav — override label ─── */
div[data-testid="stSelectbox"] > label { display: none !important; }

/* ─── HERO ─── */
.hero-wrapper {
    position: relative;
    background: linear-gradient(135deg, #0D0D0D 0%, #1A0000 55%, #0D0D0D 100%);
    border: 1px solid #2C0000;
    border-radius: 16px;
    padding: 2rem 1.5rem 1.8rem;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.hero-wrapper::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(220,0,0,0.2) 0%, transparent 65%);
    pointer-events: none;
}
.hero-wrapper::after {
    content: 'HONDA';
    position: absolute;
    bottom: -14px; right: 10px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 18vw, 8rem);
    color: rgba(220,0,0,0.05);
    letter-spacing: 0.1em;
    pointer-events: none;
    line-height: 1;
}
.hero-eyebrow {
    font-size: 0.65rem;
    color: #DC0000;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 600;
    margin: 0 0 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 22px; height: 2px;
    background: #DC0000;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(2.2rem, 10vw, 3.8rem) !important;
    letter-spacing: 0.06em;
    color: #FFFFFF !important;
    margin: 0 0 0.3rem !important;
    line-height: 1 !important;
}
.hero-title span { color: #DC0000; }
.hero-tagline {
    font-size: clamp(0.72rem, 2.5vw, 0.88rem);
    color: #555;
    letter-spacing: 0.04em;
    margin: 0.5rem 0 0;
}
.hero-chips {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.hero-chip {
    background: rgba(220,0,0,0.1);
    border: 1px solid rgba(220,0,0,0.22);
    color: #FF6666;
    font-size: 0.62rem;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    font-weight: 600;
}

/* ─── SECTION HEADING ─── */
.section-heading {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(1.5rem, 6vw, 2rem) !important;
    letter-spacing: 0.06em;
    color: #FFFFFF !important;
    margin-bottom: 0.15rem !important;
    display: flex;
    align-items: center;
    gap: 12px;
}
.section-heading::before {
    content: '';
    display: inline-block;
    width: 4px; height: 24px;
    background: linear-gradient(180deg, #DC0000, #880000);
    border-radius: 3px;
    flex-shrink: 0;
}
.section-desc {
    color: #555;
    font-size: 0.8rem;
    margin-bottom: 1.4rem;
    margin-left: 18px;
    letter-spacing: 0.03em;
}

/* ─── STAT PILLS ─── */
.stat-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin: 0.8rem 0 1.4rem;
}
.stat-pill {
    background: linear-gradient(145deg, #141414, #1A1A1A);
    border: 1px solid #252525;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    text-align: center;
    min-width: 90px;
    flex: 1;
    position: relative;
    overflow: hidden;
}
.stat-pill::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #DC0000, transparent);
}
.stat-pill .val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(1rem, 4vw, 1.5rem);
    color: #DC0000;
    display: block;
    line-height: 1;
}
.stat-pill .lbl {
    font-size: 0.6rem;
    color: #484848;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    display: block;
    margin-top: 4px;
    font-weight: 600;
}

/* ─── BIKE CARD ─── */
.bike-card {
    background: linear-gradient(145deg, #111111, #171717);
    border: 1px solid #232323;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.8rem;
    transition: border-color 0.25s, transform 0.25s;
    position: relative;
    overflow: hidden;
}
.bike-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #DC0000, #660000);
    border-radius: 3px 0 0 3px;
}
.bike-card:hover { border-color: #DC0000; transform: translateX(3px); }
.bike-name {
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.95rem, 3.5vw, 1.15rem);
    color: #F0EDE8;
    margin: 0 0 4px;
}
.bike-price {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(1rem, 4vw, 1.3rem);
    color: #DC0000;
    letter-spacing: 0.05em;
    white-space: nowrap;
}
.bike-badge {
    background: rgba(220,0,0,0.12);
    border: 1px solid rgba(220,0,0,0.22);
    color: #FF6666;
    font-size: 0.6rem;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 700;
    white-space: nowrap;
}

/* ─── SHOWCASE CARD ─── */
.showcase-card {
    background: linear-gradient(145deg, #111111, #181818);
    border: 1px solid #232323;
    border-radius: 16px;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
    margin-bottom: 1.2rem;
}
.showcase-card:hover {
    border-color: #DC0000;
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(220,0,0,0.18);
}
.card-img-wrap {
    background: linear-gradient(135deg, #0F0F0F, #180000);
    padding: 1.2rem;
    text-align: center;
}
.card-img-wrap img {
    width: 100%;
    max-height: 300px;
    object-fit: contain;
    display: block;
}
.card-body { padding: 1rem 1.2rem; }
.card-name {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1rem, 4vw, 1.2rem);
    color: #F0EDE8;
    margin: 0 0 3px;
}
.card-price {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(1.1rem, 5vw, 1.5rem);
    color: #DC0000;
    letter-spacing: 0.05em;
}
.card-specs {
    font-size: 0.7rem;
    color: #484848;
    margin-top: 0.5rem;
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    font-weight: 500;
}
.card-footer {
    border-top: 1px solid #1E1E1E;
    padding: 0.7rem 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #0E0E0E;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.stock-indicator {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.stock-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
.stock-dot.high { background: #44BB44; box-shadow: 0 0 5px rgba(68,187,68,0.5); }
.stock-dot.low  { background: #CCAA33; box-shadow: 0 0 5px rgba(204,170,51,0.5); }
.stock-dot.none { background: #CC3333; box-shadow: 0 0 5px rgba(204,51,51,0.5); }
.stock-high { color: #44BB44 !important; }
.stock-low  { color: #CCAA33 !important; }
.stock-none { color: #CC3333 !important; }

/* ─── DETAIL GRID ─── */
.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-top: 1rem;
}
.detail-item {
    background: linear-gradient(145deg, #111111, #161616);
    border: 1px solid #1F1F1F;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    position: relative;
    overflow: hidden;
}
.detail-item::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, #DC0000, transparent);
}
.detail-label {
    font-size: 0.62rem;
    color: #444;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.25rem;
    font-weight: 700;
}
.detail-value {
    font-family: 'Playfair Display', serif;
    font-size: clamp(0.9rem, 3.5vw, 1.1rem);
    color: #F0EDE8;
}

/* ─── COMPARE TABLE ─── */
.compare-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.2rem;
    border-radius: 10px;
    overflow: hidden;
    font-size: clamp(0.72rem, 2.5vw, 0.9rem);
}
.compare-table th {
    background: linear-gradient(135deg, #1A0000, #220000);
    color: #DC0000;
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(0.8rem, 3vw, 1rem);
    letter-spacing: 0.08em;
    padding: 0.8rem 0.8rem;
    text-align: left;
    border-bottom: 2px solid #DC0000;
}
.compare-table th:first-child { color: #555; font-family: 'Outfit',sans-serif; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }
.compare-table td {
    padding: 0.7rem 0.8rem;
    border-bottom: 1px solid #191919;
    color: #B0ADA8;
    word-break: break-word;
}
.compare-table td:first-child {
    color: #555;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
}
.compare-table tr:nth-child(even) td { background: rgba(255,255,255,0.018); }
.compare-table tr:last-child td { border-bottom: none; }

/* ─── RECEIPT ─── */
.receipt-box {
    background: #0C0C0C;
    border: 1px solid #1E1E1E;
    border-radius: 12px;
    padding: 1.4rem 1.4rem;
    font-family: 'Courier New', monospace;
    font-size: clamp(0.68rem, 2.5vw, 0.83rem);
    color: #888;
    line-height: 1.9;
    border-left: 3px solid #DC0000;
    overflow-x: auto;
}
.receipt-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    color: #DC0000;
    letter-spacing: 0.12em;
    margin-bottom: 0.8rem;
}

/* ─── INPUTS ─── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #111111 !important;
    border: 1px solid #252525 !important;
    border-radius: 10px !important;
    color: #F0EDE8 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #DC0000 !important;
    box-shadow: 0 0 0 3px rgba(220,0,0,0.1) !important;
}
label {
    color: #555 !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ─── BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, #DC0000, #AA0000) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 16px rgba(220,0,0,0.28) !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #FF1111, #CC0000) !important;
    box-shadow: 0 8px 24px rgba(220,0,0,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ─── ALERTS ─── */
.stSuccess > div, .stInfo > div, .stWarning > div, .stError > div {
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
}
.stSuccess > div { background: #081208 !important; border: 1px solid #163016 !important; color: #55BB55 !important; }
.stInfo > div    { background: #080C18 !important; border: 1px solid #151E3A !important; color: #5588CC !important; }
.stWarning > div { background: #141200 !important; border: 1px solid #302A00 !important; color: #CCAA33 !important; }
.stError > div   { background: #140808 !important; border: 1px solid #300000 !important; color: #CC4444 !important; }

hr { border-color: #181818 !important; margin: 1.5rem 0 !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #2C0000; border-radius: 3px; }

/* ─── CONTACT GRID ─── */
.contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-top: 1rem;
}
.contact-card {
    background: linear-gradient(145deg, #111111, #171717);
    border: 1px solid #1F1F1F;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    transition: border-color 0.2s;
}
.contact-card:hover { border-color: #2C0000; }
.contact-card .ci { font-size: 1.4rem; margin-bottom: 0.4rem; display: block; }
.contact-card .cl { font-size: 0.6rem; color: #444; text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 0.2rem; font-weight: 700; }
.contact-card .cv { font-family: 'Playfair Display', serif; font-size: clamp(0.85rem, 3vw, 1.05rem); color: #F0EDE8; }
.contact-card .cs { font-size: 0.72rem; color: #555; margin-top: 0.2rem; }
.map-wrapper { border-radius: 14px; overflow: hidden; border: 1px solid #1E1E1E; margin-top: 1.2rem; }

/* ─── FEATURE GRID ─── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.8rem;
    margin: 1.2rem 0;
}
.feature-card {
    background: linear-gradient(145deg, #111111, #181818);
    border: 1px solid #1E1E1E;
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: border-color 0.25s, transform 0.25s;
}
.feature-card:hover { border-color: #3C0000; transform: translateY(-3px); }
.feature-card .fc-icon { font-size: 1.6rem; margin-bottom: 0.4rem; display: block; }
.feature-card .fc-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(0.85rem, 3vw, 1.05rem);
    letter-spacing: 0.08em;
    color: #DDD;
    margin-bottom: 0.25rem;
}
.feature-card .fc-desc { font-size: 0.68rem; color: #444; line-height: 1.5; }

/* ─── PURCHASE PREVIEW ─── */
.purchase-preview {
    display: flex;
    gap: 1rem;
    align-items: center;
    background: linear-gradient(145deg, #111111, #181818);
    border: 1px solid #232323;
    border-radius: 14px;
    padding: 1.2rem;
    margin: 0.8rem 0 1.4rem;
    flex-wrap: wrap;
}
.purchase-preview img {
    width: 120px;
    height: 90px;
    object-fit: contain;
    border-radius: 10px;
    background: #0D0000;
    padding: 6px;
    border: 1px solid #1E1E1E;
    flex-shrink: 0;
}
.pp-name { font-family: 'Playfair Display', serif; font-size: clamp(1.1rem, 4vw, 1.4rem); color: #F0EDE8; margin: 0 0 3px; }
.pp-price { font-family: 'Bebas Neue', sans-serif; font-size: clamp(1.2rem, 5vw, 1.6rem); color: #DC0000; letter-spacing: 0.05em; }

/* ─── WHATSAPP FLOAT ─── */
.whatsapp-float {
    position: fixed;
    bottom: 20px; right: 16px;
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #25D366, #1AA851);
    color: #fff !important;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    padding: 11px 18px 11px 14px;
    border-radius: 50px;
    text-decoration: none !important;
    box-shadow: 0 6px 24px rgba(37,211,102,0.4);
    animation: wa-pulse 2.8s infinite;
}
@keyframes wa-pulse {
    0%, 100% { box-shadow: 0 6px 24px rgba(37,211,102,0.4); }
    50%       { box-shadow: 0 6px 32px rgba(37,211,102,0.7); }
}

/* ─── MOBILE RESPONSIVE ─── */
@media (max-width: 600px) {
    .block-container { padding: 0.6rem 0.5rem 5rem !important; }
    .hero-wrapper { padding: 1.4rem 1rem 1.4rem; border-radius: 12px; }
    .contact-grid { grid-template-columns: 1fr; }
    .feature-grid { grid-template-columns: 1fr 1fr; }
    .detail-grid  { grid-template-columns: 1fr; }
    .purchase-preview { flex-direction: column; align-items: flex-start; }
    .purchase-preview img { width: 100%; height: 160px; }
    .topnav { border-radius: 10px; padding: 0.6rem 0.8rem; }
    .topnav-brand { font-size: 1.2rem; }
    .whatsapp-float { bottom: 14px; right: 12px; padding: 10px 14px 10px 12px; font-size: 0; }
    .whatsapp-float svg { margin: 0; }
    table { font-size: 0.7rem !important; }
    .compare-table th, .compare-table td { padding: 0.55rem 0.5rem !important; }
}

@media (max-width: 400px) {
    .feature-grid { grid-template-columns: 1fr; }
    .stat-pill { min-width: 70px; padding: 0.6rem 0.5rem; }
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── WHATSAPP BUTTON ───
WA_NUMBER = "923196971162"
st.markdown(f"""
<a class="whatsapp-float" href="https://wa.me/{WA_NUMBER}?text=Hello!%20I%20am%20interested%20in%20buying%20a%20Honda%20bike." target="_blank" title="Chat on WhatsApp">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
  </svg>
  <span>Chat on WhatsApp</span>
</a>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("showroom.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bikes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, type TEXT, price TEXT,
    engine TEXT, fuel_avg TEXT, top_speed TEXT,
    stock INTEGER, color_stock TEXT DEFAULT '{}'
)
""")
try:
    cursor.execute("ALTER TABLE bikes ADD COLUMN color_stock TEXT DEFAULT '{}'")
    conn.commit()
except Exception:
    pass
conn.commit()

# ---------------- ADMIN ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ---------------- BIKE DATA ----------------
BIKE_IMAGES = {
    "Honda CD 70": {
        "Red":   "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/CD70Red.webp",
        "Black": "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/CD70Black.webp",
        "Blue":  "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/CD70Blue.webp"
    },
    "CD 70 Dream": {
        "Red":    "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/cd-70-dream-red.webp",
        "Black":  "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/cd-70-dream-black.webp",
        "Silver": "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/cd-70-dream-silver.webp"
    },
    "Honda CG125": {
        "Red":   "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/cg125-red-product-picture.webp",
        "Black": "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/cg125-black-product-picture.webp",
        "Blue":  "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/cg125-blue-product-picture.webp"
    },
    "Honda Pridor 100": {
        "Red":   "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/Red-product.webp",
        "Black": "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/black-product.webp",
        "Blue":  "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/blue-product.webp"
    },
    "Honda CB 150F": {
        "Red":    "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/CB150F-red-1.webp",
        "Black":  "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/CB150F-Black-1.webp",
        "Blue":   "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/CB150F-blue-1.webp",
        "Silver": "https://www.atlashonda.com.pk/wp-content/uploads/2021/04/CB150F-silver-1.webp"
    }
}

DEFAULT_COLORS = {
    "Honda CD 70":      ["Red","Black","Blue"],
    "CD 70 Dream":      ["Red","Black","Silver"],
    "Honda CG125":      ["Red","Black","Blue"],
    "Honda Pridor 100": ["Red","Black","Blue"],
    "Honda CB 150F":    ["Red","Black","Blue","Silver"],
}
COLOR_HEX = {
    "Red":"#CC2222","Black":"#111111","Blue":"#1133CC",
    "Silver":"#AAAAAA","White":"#EEEEEE","Green":"#116611",
    "Orange":"#CC5500","Yellow":"#CCAA00","Brown":"#664422"
}

if "selected_colors" not in st.session_state:
    st.session_state.selected_colors = {}

# ---------------- HELPERS ----------------
def normalize(t): return t.lower().replace(" ","")
def parse_price(p):
    d = "".join(filter(str.isdigit, p))
    return int(d) if d else 0

def get_all_bikes():
    cursor.execute("SELECT * FROM bikes"); return cursor.fetchall()

def get_bike_names():
    cursor.execute("SELECT name FROM bikes"); return [r[0] for r in cursor.fetchall()]

def get_bike_by_name(name):
    for b in get_all_bikes():
        if normalize(name)==normalize(b[1]): return b
    return None

def get_color_stock(bike):
    try: return json.loads(bike[8]) if bike[8] else {}
    except: return {}

def get_colors_for_bike(bike):
    cs = get_color_stock(bike)
    return list(cs.keys()) if cs else DEFAULT_COLORS.get(bike[1],["Red","Black"])

def get_stock_for_color(bike, color):
    cs = get_color_stock(bike)
    return cs.get(color, bike[7]) if cs else bike[7]

def recommend(budget):
    return sorted(get_all_bikes(), key=lambda b: abs(parse_price(b[3])-budget))[:3]

def get_bike_by_name_check(name):
    for b in get_all_bikes():
        if normalize(name) in normalize(b[1]): return b
    return None

def update_stock(bike_id, new_stock, cs_dict):
    cursor.execute("UPDATE bikes SET stock=?,color_stock=? WHERE id=?",(new_stock,json.dumps(cs_dict),bike_id))
    conn.commit()

def delete_bike(bike_id):
    cursor.execute("DELETE FROM bikes WHERE id=?",(bike_id,)); conn.commit()

def add_bike(name,btype,price,engine,fuel,speed,total,cs_dict):
    cursor.execute("INSERT INTO bikes (name,type,price,engine,fuel_avg,top_speed,stock,color_stock) VALUES (?,?,?,?,?,?,?,?)",
                   (name,btype,price,engine,fuel,speed,total,json.dumps(cs_dict))); conn.commit()

def get_image(bike_name, color):
    imgs = BIKE_IMAGES.get(bike_name,{})
    return imgs.get(color, list(imgs.values())[0] if imgs else "")

def send_order_email(subject, body):
    try:
        msg = EmailMessage()
        msg["Subject"]=subject; msg["From"]="ibrahimmalik6371162@gmail.com"
        msg["To"]="ibrahimmalik6371162@gmail.com"; msg.set_content(body)
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as s:
            s.login("ibrahimmalik6371162@gmail.com","gfch xzvz jyqh ucpe"); s.send_message(msg)
    except: pass

# ---------------- SAMPLE DATA ----------------
def add_sample_data():
    cursor.execute("SELECT COUNT(*) FROM bikes")
    if cursor.fetchone()[0]==0:
        bikes=[
            ("Honda CD 70","Commuter","PKR 159,900/=","70cc","60 km/l","75 km/h",15,
             json.dumps({"Red":6,"Black":5,"Blue":4})),
            ("CD 70 Dream","Commuter","PKR 170,900/=","72cc","65 km/l","75 km/h",20,
             json.dumps({"Red":8,"Black":7,"Silver":5})),
            ("Honda CG125","Commuter","PKR 295,000/=","125cc","35 km/l","100 km/h",10,
             json.dumps({"Red":4,"Black":4,"Blue":2})),
            ("Honda Pridor 100","Commuter","PKR 211,900/=","100cc","50 km/l","95 km/h",3,
             json.dumps({"Red":1,"Black":1,"Blue":1})),
            ("Honda CB 150F","Mid-range","PKR 503,900/=","150cc","35 km/l","115 km/h",2,
             json.dumps({"Red":1,"Black":1,"Blue":0,"Silver":0})),
        ]
        cursor.executemany("INSERT INTO bikes VALUES (NULL,?,?,?,?,?,?,?,?)",bikes)
        conn.commit()

add_sample_data()

# ============================================================
#  TOP NAV — replaces sidebar on all screen sizes
# ============================================================
nav_options = [
    "🏠 Home","🖼️ Showcase","🏍️ View Bikes","📋 Details",
    "💡 Recommend","⚖️ Compare","📦 Availability",
    "🛒 Purchase","💳 EMI Calc","📍 Contact","🔐 Admin"
]

col_brand, col_nav = st.columns([1, 2])
with col_brand:
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#DC0000;
                letter-spacing:0.08em;line-height:0.9;padding:0.3rem 0;">
      GOLDEN HONDA
      <span style="display:block;font-family:'Outfit',sans-serif;font-size:0.6rem;
                   color:#444;letter-spacing:0.18em;text-transform:uppercase;margin-top:2px;">
        Showroom · Multan
      </span>
    </div>
    """, unsafe_allow_html=True)
with col_nav:
    menu = st.selectbox("", nav_options, label_visibility="collapsed")

menu_key = menu.split(" ", 1)[-1].strip()

st.markdown('<div style="height:0.2rem"></div>', unsafe_allow_html=True)

# ─── HERO ───
st.markdown("""
<div class="hero-wrapper">
  <p class="hero-eyebrow">Smart Bike Buying Experience</p>
  <h1 class="hero-title">Golden <span>Honda</span><br>Showroom</h1>
  <p class="hero-tagline">Multan's premier Honda dealership — quality bikes, transparent pricing</p>
  <div class="hero-chips">
    <span class="hero-chip">✓ Genuine Honda</span>
    <span class="hero-chip">✓ EMI Available</span>
    <span class="hero-chip">✓ Multan, PK</span>
    <span class="hero-chip">✓ After-sale Service</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
#  HOME
# ============================================================
if menu_key == "Home":
    st.markdown('<div class="section-heading">Welcome</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Explore our premium Honda lineup, compare models, and buy with confidence.</p>', unsafe_allow_html=True)

    bikes  = get_all_bikes()
    prices = [parse_price(b[3]) for b in bikes]
    total_stock = sum(b[7] for b in bikes)

    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-pill"><span class="val">{len(bikes)}</span><span class="lbl">Models</span></div>
      <div class="stat-pill"><span class="val">{total_stock}</span><span class="lbl">In Stock</span></div>
      <div class="stat-pill"><span class="val">PKR {min(prices)//1000}K</span><span class="lbl">From</span></div>
      <div class="stat-pill"><span class="val">PKR {max(prices)//1000}K</span><span class="lbl">Top</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
      <div class="feature-card">
        <span class="fc-icon">🏍️</span>
        <div class="fc-title">Wide Selection</div>
        <div class="fc-desc">70cc to 150cc — all genuine Honda models.</div>
      </div>
      <div class="feature-card">
        <span class="fc-icon">💳</span>
        <div class="fc-title">Easy EMI</div>
        <div class="fc-desc">Flexible installment plans, low down payment.</div>
      </div>
      <div class="feature-card">
        <span class="fc-icon">🔧</span>
        <div class="fc-title">Genuine Parts</div>
        <div class="fc-desc">100% authentic with manufacturer warranty.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
#  BIKE SHOWCASE
# ============================================================
elif menu_key == "Showcase":
    st.markdown('<div class="section-heading">Bike Showcase</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Select a colour to see per-colour stock</p>', unsafe_allow_html=True)

    bikes = get_all_bikes()
    cols  = st.columns(2)

    for idx, bike in enumerate(bikes):
        with cols[idx % 2]:
            bike_name = bike[1]
            colors    = get_colors_for_bike(bike)
            sk        = f"sc_{bike_name}"
            if sk not in st.session_state:
                st.session_state[sk] = colors[0]

            sel_color  = st.session_state[sk]
            image_url  = get_image(bike_name, sel_color)
            clr_stock  = get_stock_for_color(bike, sel_color)
            dot_cls    = "high" if clr_stock>5 else ("low" if clr_stock>0 else "none")
            sc_cls     = "stock-high" if clr_stock>5 else ("stock-low" if clr_stock>0 else "stock-none")

            st.markdown(f"""
            <div class="showcase-card">
              <div class="card-img-wrap">
                <img src="{image_url}" alt="{bike_name}" onerror="this.style.display='none'"/>
              </div>
              <div class="card-body">
                <p class="card-name">{bike_name}</p>
                <p class="card-price">{bike[3]}</p>
                <div class="card-specs">
                  <span>⚙️ {bike[4]}</span><span>⛽ {bike[5]}</span><span>🏁 {bike[6]}</span>
                </div>
              </div>
              <div class="card-footer">
                <span class="stock-indicator {sc_cls}">
                  <span class="stock-dot {dot_cls}"></span>{sel_color}: {clr_stock} units
                </span>
                <span class="bike-badge">{bike[2]}</span>
              </div>
            </div>""", unsafe_allow_html=True)

            btn_cols = st.columns(len(colors))
            for i, color in enumerate(colors):
                with btn_cols[i]:
                    if st.button(color, key=f"sc_{bike_name}_{color}"):
                        st.session_state[sk] = color
                        st.rerun()

            wa_msg = f"Hello! I am interested in {bike_name} in {sel_color} colour."
            st.markdown(f"""
            <a href="https://wa.me/{WA_NUMBER}?text={wa_msg.replace(' ','%20')}" target="_blank"
               style="display:inline-flex;align-items:center;gap:7px;background:#25D366;color:#fff;
                      font-family:'Outfit',sans-serif;font-size:0.72rem;font-weight:700;
                      padding:8px 16px;border-radius:8px;text-decoration:none;letter-spacing:0.05em;
                      margin:0.4rem 0 1rem;">
              💬 WhatsApp Inquiry
            </a>""", unsafe_allow_html=True)
            st.markdown("---")


# ============================================================
#  VIEW BIKES
# ============================================================
elif menu_key == "View Bikes":
    st.markdown('<div class="section-heading">Available Bikes</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Complete Honda inventory</p>', unsafe_allow_html=True)
    for b in get_all_bikes():
        sc  = "stock-high" if b[7]>5 else ("stock-low" if b[7]>0 else "stock-none")
        dot = "high" if b[7]>5 else ("low" if b[7]>0 else "none")
        st.markdown(f"""
        <div class="bike-card">
          <div><p class="bike-name">{b[1]}</p><span class="bike-badge">{b[2]}</span></div>
          <div style="text-align:right">
            <p class="bike-price">{b[3]}</p>
            <span class="stock-indicator {sc}"><span class="stock-dot {dot}"></span>{b[7]} units</span>
          </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
#  BIKE DETAILS
# ============================================================
elif menu_key == "Details":
    st.markdown('<div class="section-heading">Bike Details</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Full specifications for any model</p>', unsafe_allow_html=True)

    selected = st.selectbox("Select a Model", get_bike_names())
    if st.button("Show Details"):
        bike = get_bike_by_name(selected)
        if bike:
            colors    = get_colors_for_bike(bike)
            first_img = get_image(bike[1], colors[0])
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,#111,#181818);border:1px solid #232323;border-radius:16px;overflow:hidden;margin-top:1rem;">
              <div style="background:linear-gradient(135deg,#0D0D0D,#180000);padding:1.5rem;text-align:center;">
                <img src="{first_img}" style="max-height:220px;max-width:100%;object-fit:contain;"
                     onerror="this.src='';this.style.display='none'"/>
              </div>
              <div style="padding:1.2rem 1.4rem;">
                <div style="display:flex;align-items:baseline;gap:0.8rem;flex-wrap:wrap;margin-bottom:0.3rem;">
                  <span style="font-family:'Playfair Display',serif;font-size:1.6rem;color:#F0EDE8;">{bike[1]}</span>
                  <span class="bike-badge">{bike[2]}</span>
                </div>
                <p class="bike-price" style="font-size:1.5rem;margin-bottom:1rem;">{bike[3]}</p>
                <div class="detail-grid">
                  <div class="detail-item"><div class="detail-label">Engine</div><div class="detail-value">{bike[4]}</div></div>
                  <div class="detail-item"><div class="detail-label">Fuel Average</div><div class="detail-value">{bike[5]}</div></div>
                  <div class="detail-item"><div class="detail-label">Top Speed</div><div class="detail-value">{bike[6]}</div></div>
                  <div class="detail-item"><div class="detail-label">Total Stock</div>
                    <div class="detail-value {'stock-high' if bike[7]>5 else 'stock-low'}">{bike[7]} units</div></div>
                </div>
            """, unsafe_allow_html=True)
            cs = get_color_stock(bike)
            if cs:
                rows = "".join(
                    f"""<div class="detail-item" style="display:flex;justify-content:space-between;align-items:center;">
                          <div><div class="detail-label">Colour</div><div class="detail-value">{c}</div></div>
                          <div style="text-align:right"><div class="detail-label">Stock</div>
                            <div class="detail-value {'stock-high' if s>5 else 'stock-low' if s>0 else 'stock-none'}">{s} units</div></div>
                        </div>"""
                    for c,s in cs.items()
                )
                st.markdown(f"""
                <div style="margin-top:0.8rem;">
                  <p style="font-size:0.62rem;color:#555;text-transform:uppercase;letter-spacing:0.12em;font-weight:700;margin-bottom:0.6rem;">
                    Per-Colour Availability
                  </p>
                  <div class="detail-grid">{rows}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)


# ============================================================
#  RECOMMENDATION
# ============================================================
elif menu_key == "Recommend":
    st.markdown('<div class="section-heading">Recommendation</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Find the perfect bike for your budget</p>', unsafe_allow_html=True)

    prices = [parse_price(b[3]) for b in get_all_bikes()]
    st.info(f"📊  Price range: PKR {min(prices):,} – PKR {max(prices):,}")
    budget = st.number_input("Your Budget (PKR)", min_value=50000, step=5000)

    if st.button("Find Best Matches"):
        for i, r in enumerate(recommend(budget)):
            medal = ["🥇","🥈","🥉"][i]
            diff  = abs(parse_price(r[3])-budget)
            sc    = "stock-high" if r[7]>5 else ("stock-low" if r[7]>0 else "stock-none")
            st.markdown(f"""
            <div class="bike-card">
              <div>
                <p style="font-size:0.65rem;color:#555;margin:0 0 3px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;">
                  {medal} Match #{i+1}
                </p>
                <p class="bike-name">{r[1]}</p>
                <div style="display:flex;gap:0.8rem;flex-wrap:wrap;margin-top:5px;">
                  <span style="font-size:0.68rem;color:#555;">⚙️ {r[4]}</span>
                  <span style="font-size:0.68rem;color:#555;">⛽ {r[5]}</span>
                  <span style="font-size:0.68rem;color:#555;">🏁 {r[6]}</span>
                </div>
              </div>
              <div style="text-align:right;flex-shrink:0;">
                <p class="bike-price">{r[3]}</p>
                <span style="font-size:0.65rem;color:#555;display:block;">±PKR {diff:,}</span>
                <span class="stock-indicator {sc}" style="display:inline-flex;margin-top:3px;">{r[7]} units</span>
              </div>
            </div>""", unsafe_allow_html=True)


# ============================================================
#  COMPARE
# ============================================================
elif menu_key == "Compare":
    st.markdown('<div class="section-heading">Compare Bikes</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Side-by-side specification comparison</p>', unsafe_allow_html=True)

    names = get_bike_names()
    col1, col2 = st.columns(2)
    with col1: b1 = st.selectbox("Model A", names, key="cmp1")
    with col2: b2 = st.selectbox("Model B", names, key="cmp2")

    if st.button("Compare Now"):
        bike1 = get_bike_by_name(b1)
        bike2 = get_bike_by_name(b2)
        features = ["Category","Price","Engine","Fuel Average","Top Speed","Total Stock"]
        vals1 = [bike1[2],bike1[3],bike1[4],bike1[5],bike1[6],f"{bike1[7]} units"]
        vals2 = [bike2[2],bike2[3],bike2[4],bike2[5],bike2[6],f"{bike2[7]} units"]
        rows = "".join(f"<tr><td>{f}</td><td>{v1}</td><td>{v2}</td></tr>" for f,v1,v2 in zip(features,vals1,vals2))
        st.markdown(f"""
        <table class="compare-table">
          <thead><tr><th>Spec</th><th>{bike1[1]}</th><th>{bike2[1]}</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

        cs1 = get_color_stock(bike1); cs2 = get_color_stock(bike2)
        if cs1 or cs2:
            all_c = sorted(set(list(cs1.keys())+list(cs2.keys())))
            crow  = "".join(f"<tr><td>{c}</td><td>{cs1.get(c,'—')} units</td><td>{cs2.get(c,'—')} units</td></tr>" for c in all_c)
            st.markdown(f"""
            <p style="font-size:0.62rem;color:#555;text-transform:uppercase;letter-spacing:0.1em;font-weight:700;margin:1.2rem 0 0.4rem;">
              Per-Colour Stock
            </p>
            <table class="compare-table">
              <thead><tr><th>Colour</th><th>{bike1[1]}</th><th>{bike2[1]}</th></tr></thead>
              <tbody>{crow}</tbody>
            </table>""", unsafe_allow_html=True)


# ============================================================
#  AVAILABILITY
# ============================================================
elif menu_key == "Availability":
    st.markdown('<div class="section-heading">Availability</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Real-time per-colour stock</p>', unsafe_allow_html=True)

    name = st.selectbox("Select a Model", get_bike_names())
    if st.button("Check Stock"):
        bike = get_bike_by_name(name)
        if bike:
            stock = bike[7]
            if stock>5: st.success(f"✅  {name} — {stock} total units in stock")
            elif stock>0: st.warning(f"⚠️  {name} — Only {stock} unit(s) left!")
            else: st.error(f"❌  {name} — Out of stock")
            cs = get_color_stock(bike)
            if cs:
                pills = "".join(
                    f"""<div class="stat-pill">
                          <span class="val {'stock-high' if s>5 else 'stock-low' if s>0 else 'stock-none'}">{s}</span>
                          <span class="lbl">{c}</span>
                        </div>"""
                    for c,s in cs.items()
                )
                st.markdown(f'<div class="stat-row" style="margin-top:1rem;">{pills}</div>', unsafe_allow_html=True)


# ============================================================
#  PURCHASE
# ============================================================
elif menu_key == "Purchase":
    st.markdown('<div class="section-heading">Purchase Bike</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Complete your order below</p>', unsafe_allow_html=True)

    selected = st.selectbox("Select a Model", get_bike_names())
    bike     = get_bike_by_name(selected)

    if bike:
        colors       = get_colors_for_bike(bike)
        chosen_color = st.selectbox("Colour Variant", colors)
        clr_stock    = get_stock_for_color(bike, chosen_color)
        image_url    = get_image(bike[1], chosen_color)

        st.markdown(f"""
        <div class="purchase-preview">
          <img src="{image_url}" alt="{bike[1]}" onerror="this.src='';this.style.display='none'"/>
          <div>
            <p class="pp-name">{bike[1]}</p>
            <span class="bike-badge">{bike[2]}</span>
            <p class="pp-price">{bike[3]}</p>
            <div style="display:flex;gap:0.8rem;flex-wrap:wrap;margin-top:6px;">
              <span style="font-size:0.68rem;color:#555;">⚙️ {bike[4]}</span>
              <span style="font-size:0.68rem;color:#555;">⛽ {bike[5]}</span>
              <span style="font-size:0.68rem;color:#555;">🏁 {bike[6]}</span>
            </div>
            <span style="font-size:0.72rem;margin-top:6px;display:block;" class="{'stock-high' if clr_stock>0 else 'stock-none'}">
              {chosen_color} — {clr_stock} units available
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

        max_qty = max(clr_stock,1)
        col1, col2 = st.columns(2)
        with col1:
            name_  = st.text_input("Full Name")
            phone  = st.text_input("Phone Number")
        with col2:
            email  = st.text_input("Email Address")
            qty    = st.number_input("Quantity",1,max_qty)

        if st.button("Place Order →"):
            if clr_stock==0:
                st.error("❌ This colour is currently out of stock.")
            else:
                total = parse_price(bike[3])*qty
                order_text = f"""
CUSTOMER    : {name_}
PHONE       : {phone}
EMAIL       : {email}

BIKE        : {bike[1]}
COLOUR      : {chosen_color}
ENGINE      : {bike[4]}
UNIT PRICE  : {bike[3]}
QUANTITY    : {qty}
─────────────────────────────────
TOTAL       : PKR {total:,}
"""
                st.success("✅  Order placed successfully!")
                st.markdown(f"""
                <div class="receipt-box">
                  <div class="receipt-header">ORDER RECEIPT</div>
                  <pre style="margin:0;font-family:inherit;color:#888;white-space:pre-wrap;">{order_text}</pre>
                </div>""", unsafe_allow_html=True)
                wa_msg = f"Hello!%20Order:%0A{bike[1]}%20({chosen_color})%0AQty:{qty}%0ATotal:PKR%20{total:,}%0AName:{name_}%0APhone:{phone}"
                st.markdown(f"""
                <a href="https://wa.me/{WA_NUMBER}?text={wa_msg}" target="_blank"
                   style="display:inline-flex;align-items:center;gap:8px;margin-top:1rem;
                          background:#25D366;color:#fff;font-family:'Outfit',sans-serif;
                          font-size:0.78rem;font-weight:700;padding:11px 22px;border-radius:10px;
                          text-decoration:none;letter-spacing:0.06em;">
                  📲 Confirm via WhatsApp
                </a>""", unsafe_allow_html=True)
                send_order_email(f"New Order — {bike[1]}", order_text)


# ============================================================
#  EMI CALCULATOR
# ============================================================
elif menu_key == "EMI Calc":
    st.markdown('<div class="section-heading">EMI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Plan your monthly installments</p>', unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)
    with col1: price  = st.number_input("Bike Price (PKR)",min_value=0,step=1000)
    with col2: down   = st.number_input("Down Payment (PKR)",min_value=0,step=1000)
    with col3: months = st.number_input("Tenure (Months)",min_value=1,max_value=60,value=12)

    if st.button("Calculate EMI"):
        if price>0 and months>0:
            loan=price-down; emi=loan/months
            st.markdown(f"""
            <div class="stat-row" style="margin-top:1.2rem;">
              <div class="stat-pill"><span class="val">PKR {price:,.0f}</span><span class="lbl">Price</span></div>
              <div class="stat-pill"><span class="val">PKR {down:,.0f}</span><span class="lbl">Down</span></div>
              <div class="stat-pill"><span class="val">PKR {loan:,.0f}</span><span class="lbl">Loan</span></div>
              <div class="stat-pill" style="border-top-color:#DC0000;">
                <span class="val" style="font-size:clamp(0.9rem,4vw,1.4rem);">PKR {emi:,.0f}</span>
                <span class="lbl">Monthly EMI</span>
              </div>
            </div>""", unsafe_allow_html=True)
            st.success(f"💳  Monthly: **PKR {emi:,.2f}** × {months} months")


# ============================================================
#  CONTACT
# ============================================================
elif menu_key == "Contact":
    st.markdown('<div class="section-heading">Contact & Location</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Visit us or get in touch anytime</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-grid">
      <div class="contact-card">
        <span class="ci">📍</span><div class="cl">Address</div>
        <div class="cv">Golden Honda Showroom</div>
        <div class="cs">Jalilabad Colony, Dera Adda, Multan</div>
      </div>
      <div class="contact-card">
        <span class="ci">📞</span><div class="cl">Phone / WhatsApp</div>
        <div class="cv">+92 319 6971162</div>
        <div class="cs">9 AM – 8 PM (Sat – Mon)</div>
      </div>
      <div class="contact-card">
        <span class="ci">🕐</span><div class="cl">Showroom Hours</div>
        <div class="cv">9:00 AM – 8:00 PM</div>
        <div class="cs">Sat – Mon · Closed Friday</div>
      </div>
      <div class="contact-card">
        <span class="ci">✉️</span><div class="cl">Email</div>
        <div class="cv" style="font-size:0.85rem;">ibrahimmalik6371162@gmail.com</div>
        <div class="cs">Reply within 24 hours</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="map-wrapper">
      <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d256.33105903402566!2d71.45064901015597!3d30.186680578046154!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x393b3161273d92d1%3A0xbee0020b9a5e138d!2s5FP2%2BJ76%2C%20Chowk%20Dera%20Ada%2C%20Jalilabad%20Jalilabad%20Colony%2C%20Multan%2C%2060000%2C%20Pakistan!5e0!3m2!1sen!2s!4v1780582208080!5m2!1sen!2s"
        width="100%" height="380" style="border:0;display:block;" allowfullscreen="" loading="lazy">
      </iframe>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <a href="https://wa.me/{WA_NUMBER}?text=Hello!%20I%20want%20to%20visit%20Golden%20Honda.%20Please%20share%20directions." target="_blank"
       style="display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,#25D366,#1AA851);
              color:#fff;font-family:'Outfit',sans-serif;font-size:0.82rem;font-weight:700;
              padding:12px 22px;border-radius:10px;text-decoration:none;letter-spacing:0.06em;
              box-shadow:0 5px 18px rgba(37,211,102,0.35);">
      💬 Get Directions on WhatsApp
    </a>""", unsafe_allow_html=True)


# ============================================================
#  ADMIN
# ============================================================
elif menu_key == "Admin":
    st.markdown('<div class="section-heading">Admin Login</div>', unsafe_allow_html=True)

    if not st.session_state.admin_logged_in:
        col1, col2 = st.columns([1,2])
        with col1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login →"):
                if username==ADMIN_USERNAME and password==ADMIN_PASSWORD:
                    st.session_state.admin_logged_in=True; st.rerun()
                else: st.error("❌  Invalid credentials")
    else:
        st.success("🔓  Logged in as Administrator")
        st.markdown("---")

        st.markdown('<div class="section-heading">Inventory Manager</div>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Update colour-wise stock or remove bikes</p>', unsafe_allow_html=True)

        for b in get_all_bikes():
            with st.expander(f"🏍️  {b[1]}  —  {b[3]}"):
                st.markdown(f'<span class="bike-badge">{b[2]}</span>', unsafe_allow_html=True)
                cs     = get_color_stock(b)
                colors = get_colors_for_bike(b)
                new_cs = {}
                st.markdown("**Update Stock Per Colour:**")
                c_cols = st.columns(min(len(colors),3))
                for i,color in enumerate(colors):
                    with c_cols[i % min(len(colors),3)]:
                        new_cs[color] = st.number_input(
                            f"{color}", min_value=0,
                            value=cs.get(color,0), key=f"cs_{b[0]}_{color}"
                        )
                new_total = sum(new_cs.values())
                st.markdown(f"**Total Stock:** {new_total} units")
                uc1,uc2 = st.columns(2)
                with uc1:
                    if st.button("💾 Update", key=f"upd_{b[0]}"):
                        update_stock(b[0],new_total,new_cs)
                        st.success("Updated!"); st.rerun()
                with uc2:
                    if st.button("🗑️ Delete", key=f"del_{b[0]}"):
                        delete_bike(b[0]); st.rerun()

        st.markdown("---")
        st.markdown('<div class="section-heading">Add New Model</div>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Add a bike with colour-wise stock</p>', unsafe_allow_html=True)

        col1,col2 = st.columns(2)
        with col1:
            n = st.text_input("Model Name")
            t = st.text_input("Type (e.g. Commuter)")
            p = st.text_input("Price (e.g. PKR 250,000/=)")
            e = st.text_input("Engine (e.g. 125cc)")
        with col2:
            f_  = st.text_input("Fuel Average (e.g. 45 km/l)")
            sp  = st.text_input("Top Speed (e.g. 105 km/h)")
            num_colors = st.number_input("Colour Variants", min_value=1, max_value=6, value=3)

        st.markdown("**Colour Variants & Stock:**")
        color_cols  = st.columns(int(num_colors))
        all_c_names = list(COLOR_HEX.keys())
        new_cs_dict = {}
        for i in range(int(num_colors)):
            with color_cols[i]:
                cname = st.selectbox(f"Colour {i+1}", all_c_names, index=i%len(all_c_names), key=f"nc_{i}")
                cqty  = st.number_input(f"Stock ({cname})", min_value=0, value=5, key=f"nq_{i}")
                new_cs_dict[cname] = cqty

        total_new = sum(new_cs_dict.values())
        st.markdown(f"**Total Stock:** {total_new} units")

        if st.button("➕  Add Bike"):
            if n and t and p:
                add_bike(n,t,p,e,f_,sp,total_new,new_cs_dict)
                st.success(f"✅  {n} added!"); st.rerun()
            else: st.warning("Fill in Name, Type, and Price.")

        st.markdown("---")
        if st.button("🔒 Logout"):
            st.session_state.admin_logged_in=False; st.rerun()
