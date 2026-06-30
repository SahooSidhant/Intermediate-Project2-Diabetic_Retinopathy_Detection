import streamlit as st
from PIL import Image
from predictor import predict_image

# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="Diabetic Retinopathy Detection",
    page_icon="🩺",
    layout="wide"
)

# =====================================================
# Session State Fix (IMPORTANT)
# =====================================================

if "predict_clicked" not in st.session_state:
    st.session_state.predict_clicked = False

# =====================================================
# Custom CSS (Upgraded UI)
# =====================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

/* Header Card */
.header {
    background: linear-gradient(135deg, #F8FAFC, #EEF2FF);
    padding: 28px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    margin-bottom: 25px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.05);
}

.header h1 {
    color: #1E3A8A;
    margin-bottom: 5px;
}

.header p {
    color: #475569;
    font-size: 16px;
}

/* Result Card */
.result-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
            

.stButton > button {
    background-color: white !important;
    color: #1E3A8A !important;
    border: 2px solid #1E3A8A !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: 0.2s ease-in-out;
}

/* Hover effect */
.stButton > button:hover {
    background-color: #1E3A8A !important;
    color: white !important;
}

/* Image styling */
img {
    border-radius: 12px;
}

/* Clean spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# Header
# =====================================================

st.markdown("""
<div class="header">

<h1>🩺 Diabetic Retinopathy Detection</h1>

<p>Deep Learning-based Analysis of Retinal Fundus Images</p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# Upload Image
# =====================================================

uploaded_file = st.file_uploader(
    "📤 Upload Retinal Fundus Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None

    if st.session_state.last_uploaded_file != uploaded_file.name:
        st.session_state.predict_clicked = False
        st.session_state.last_uploaded_file = uploaded_file.name

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.markdown("---")

    left, right = st.columns([1, 1.2])



    with left:

        st.subheader("📷 Uploaded Image")

        st.image(
            image,
            caption="Fundus Image",
            use_container_width=True
        )

        predict = st.button(
            "🔍 Predict",
            use_container_width=True
        )

        if predict:
            st.session_state.predict_clicked = True

    # =====================================================
    # RIGHT COLUMN
    # =====================================================

    with right:

        if st.session_state.predict_clicked:

            with st.spinner("🧠 Analyzing retinal blood vessels, lesions and abnormalities..."):

                prediction, confidence, probabilities = predict_image(image)

            st.subheader("📊 Prediction Result")

            card1, card2 = st.columns(2)

            with card1:
                st.metric(
                    label="🩺 Diagnosis",
                    value=prediction
                )

            with card2:
                st.metric(
                    label="🎯 Confidence",
                    value=f"{confidence*100:.2f}%"
                )

            st.markdown("---")

            # =====================================================
            # Icons
            # =====================================================

            icons = {
                "No DR": "🟢",
                "Mild": "🟡",
                "Moderate": "🟠",
                "Severe": "🔴",
                "Proliferative DR": "🟣"
            }

            st.subheader("📈 Class Probabilities")

            # Sort probabilities (highest first)
            for cls, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):

                icon = icons.get(cls, "🔵")

                col1, col2 = st.columns([8, 2])

                with col1:
                    st.write(f"{icon} **{cls}**")
                    st.progress(float(prob))

                with col2:
                    st.markdown(
                        f"""
                        <div style="
                            margin-top: 22px;
                            font-weight: 600;
                            font-size: 14px;
                            text-align: right;
                            color: #FFFFFF;
                        ">
                            {prob*100:.2f}%
                        </div>
                        """,
                        unsafe_allow_html=True
                    )