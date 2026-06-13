
import streamlit as st
from google import genai

# ── CONFIG ─────────────────────────────
st.set_page_config(layout="wide")

# ── CUSTOM CSS ─────────────────────────
st.markdown("""
<style>
body {
    background-color: #f8f5f2;
}

.card {
    padding: 15px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.title {
    font-size: 28px;
    font-weight: bold;
}

.subtitle {
    color: gray;
}

.search-box {
    border-radius: 20px;
    padding: 10px;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────
with st.sidebar:
    st.markdown("## 👋 Halo, Traveler!")
    st.caption("Mau ke mana hari ini?")

    st.markdown("---")

    menu = st.radio("Menu", ["🏠 Beranda", "🌴 Destinasi", "💬 Chat AI"])

    st.markdown("---")

    google_api_key = st.text_input("API Key", type="password")
    reset = st.button("Reset Chat")

# ── VALIDASI ───────────────────────────
if not google_api_key:
    st.info("Masukkan API key dulu ya 🔑")
    st.stop()

# ── INIT GEMINI ────────────────────────
if ("client" not in st.session_state) or (
    getattr(st.session_state, "_key", None) != google_api_key
):
    st.session_state.client = genai.Client(api_key=google_api_key)
    st.session_state._key = google_api_key
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if reset:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

# ── BERANDA ────────────────────────────
if menu == "🏠 Beranda":

    st.markdown('<div class="title">Mau jalan ke mana hari ini?</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Eksplor destinasi terbaik di Indramayu</div>', unsafe_allow_html=True)

    st.write("")

    # CARD DESTINASI (mirip "lanjutkan belajar")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image("https://source.unsplash.com/400x250/?beach")
        st.markdown("### Pantai Tirtamaya")
        st.progress(70)
        st.caption("Populer • Sunset")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image("https://source.unsplash.com/400x250/?mangrove")
        st.markdown("### Mangrove Karangsong")
        st.progress(50)
        st.caption("Edukasi • Alam")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image("https://source.unsplash.com/400x250/?island")
        st.markdown("### Pulau Biawak")
        st.progress(60)
        st.caption("Eksotis • Sejarah")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # SEARCH BAR (kayak AI prompt di gambar)
    query = st.text_input("🔍 Tanya apa saja tentang wisata Indramayu...", key="search")

    if query:
        response = st.session_state.chat.send_message(
            f"Kamu adalah guide wisata Indramayu. Jawab: {query}"
        )
        st.success(response.text)


# ── DESTINASI ─────────────────────────
elif menu == "🌴 Destinasi":

    st.markdown("## 🌴 Daftar Wisata")

    data = [
        ("Pantai Tirtamaya", "Pantai terkenal dengan sunset indah"),
        ("Karangsong", "Hutan mangrove & spot foto"),
        ("Pulau Biawak", "Pulau dengan mercusuar tua"),
    ]

    for nama, desc in data:
        st.markdown(f"""
        <div class="card">
            <h3>{nama}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")


# ── CHAT AI ───────────────────────────
elif menu == "💬 Chat AI":

    st.markdown("## 💬 AI Travel Assistant")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Tanya wisata Indramayu...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            res = st.session_state.chat.send_message(
                f"Kamu adalah pemandu wisata Indramayu. Jawab dengan santai: {prompt}"
            )
            answer = res.text
        except Exception as e:
            answer = str(e)

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
