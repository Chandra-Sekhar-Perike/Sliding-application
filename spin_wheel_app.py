import streamlit as st
from datetime import datetime, timedelta
import base64

# Function to encode an image to Base64
def get_img_as_base64(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

# Paths to your local images
background_image_path = "background_img.jpg"  # Replace with your background image filename
logo1_image_path = "college_logo.jpg"  # Replace with your logo image filename
logo2_image_path = "talos_logo.jpeg"  # Replace with your logo image filename


# Encode the images
background_base = get_img_as_base64(background_image_path)
logo1_base = get_img_as_base64(logo1_image_path)
logo2_base = get_img_as_base64(logo2_image_path)

# Google Doc links
links = [
    {"label": "TRAVEL", "url": "https://docs.google.com/document/d/1/example1"},
    {"label": "FOOD", "url": "https://docs.google.com/document/d/2/example2"},
    {"label": "HEALTH", "url": "https://docs.google.com/document/d/3/example3"},
    {"label": "EDUCATION", "url": "https://docs.google.com/document/d/4/example4"},
    {"label": "GROCERY", "url": "https://docs.google.com/document/d/5/example5"},
]

# Streamlit Page Configuration
st.set_page_config(
    page_title="Plot-A-Thon Spin Wheel",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize session state for last spin time if not present
if 'last_spin_time' not in st.session_state:
    st.session_state.last_spin_time = None

# Cooldown Logic
cooldown_period = timedelta(minutes=4)
time_now = datetime.now()

# Calculate time remaining for cooldown
if st.session_state.last_spin_time:
    time_remaining = cooldown_period - (time_now - st.session_state.last_spin_time)
else:
    time_remaining = timedelta(0)

button_disabled = time_remaining.total_seconds() > 0

# Inject CSS directly into Streamlit
st.markdown(
    f"""
    <style>
        /* Override Streamlit's default body settings */
        body {{
            margin: 0;
            padding: 0;
            background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                              url("data:image/jpeg;base64,{background_base}");
            background-size: cover; /* Ensure background image covers the screen */
            background-position: center; /* Center the image */
            background-repeat: no-repeat; /* Do not repeat the image */
            height: 100vh;
            width: 100vw;
            overflow: hidden; /* Prevent unwanted scrollbars */
        }}
        /* Style for Streamlit's main app container */
        .stApp {{
            background: none;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }}
         /* Logo styling */
        .logo-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
            width: 100%;
        }}
        .logo {{
            width: 10%;
            max-width: 100px;
            height: auto;
            border-radius: 50%;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Inject HTML directly into Streamlit
st.markdown(
    f"""
    <div class="logo-container">
        <img class="logo" src="data:image/png;base64,{logo1_base}" alt="College Logo">
        <img class="logo" src="data:image/png;base64,{logo2_base}" alt="Talos Logo">
    </div>
    <h2 style="text-align: center; color: White;">PLOT-O-THON</h2>
    <h6 style="text-align: center; color: White;">A Technical Event organized by</h6>
    <h3 style="text-align: center; color: White;">Department of ARTIFICIAL INTELLIGENCE & DATA SCIENCE</h3>
    """,
    unsafe_allow_html=True,
)

# Render your custom content
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Slide Box</title>
    <style>
        /* Container for all content */
            .content {{
                position: relative;
                z-index: 10;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                width: 100%;
                text-align: center;
            }}

            .box-container {{
                position: relative;
                width: 90%;
                height: 150px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 20px;
            }}

            .box {{
                width: 120px;
                height: 100%;
                background: #333;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 18px;
                border-radius: 10px;
            }}

            .highlighted {{
                background-color: #FFD700;
            }}

            .pointer {{
                position: absolute;
                top: -20px;
                left: 50%;
                transform: translateX(-50%);
                width: 40px;
                height: 20px;
                background: #333;
                clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
            }}

            button {{
                margin-top: 20px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
            }}

            button:hover {{
                background: #0056b3;
            }}

            button:disabled {{
                background-color: #cccccc;
                cursor: not-allowed;
            }}
    </style>
</head>
<body>
    <div class="content">
        <!-- Box Container -->
        <div class="box-container" id="box-container">
            <div class="box">{links[0]['label']}</div>
            <div class="box">{links[1]['label']}</div>
            <div class="box">{links[2]['label']}</div>
            <div class="box">{links[3]['label']}</div>
            <div class="box">{links[4]['label']}</div>
        </div>

        <!-- Pointer and Spin Button -->
        <div class="pointer" id="pointer"></div>
        <button id="spin-btn" {"disabled" if button_disabled else ""}>Spin the Boxes</button>
    </div>

    <script>
        const links = {links};
        const boxContainer = document.getElementById("box-container");
        const spinBtn = document.getElementById("spin-btn");
        const boxes = document.querySelectorAll(".box");
        const pointer = document.getElementById("pointer");

        let isSpinning = false;
        let interval;
        let lastBoxIndex = -1;

        // Handle spinning logic
        spinBtn.addEventListener("click", () => {{
            if (isSpinning) return;

            isSpinning = true;
            const duration = Math.floor(Math.random() * (5000 - 3000 + 1)) + 3000;  // Random time between 3 and 5 seconds

            // Remove any previous highlights
            boxes.forEach((box, index) => {{
                box.classList.remove("highlighted");
            }})

            // Start moving the pointer across the boxes
            let counter = 0;
            interval = setInterval(() => {{
                boxes.forEach((box, index) => {{
                    box.classList.remove("highlighted");
                }})
                boxes[counter].classList.add("highlighted");
                pointer.style.left = "calc(" + (counter * 20) + "% + 10px)"; // Move pointer

                counter++;
                if (counter >= boxes.length) counter = 0;
            }}, 200);  // Move every 200ms

            // After the spin duration, stop the interval and show the selected box
            setTimeout(() => {{
                clearInterval(interval);
                lastBoxIndex = counter === 0 ? boxes.length - 1 : counter - 1;  // The box the pointer stops at
                boxes[lastBoxIndex].classList.add("highlighted");
                pointer.style.left = "calc(" + (lastBoxIndex * 20) + "% + 10px)";
                isSpinning = false;

                // Disable the button during cooldown
                spinBtn.disabled = true;

                // Save the current spin time
                const lastSpinTime = new Date().toISOString();
                document.cookie = "last_spin_time=" + lastSpinTime + "; path=/";

                // Ask user if they want to visit the selected link
                const selectedBoxLabel = boxes[lastBoxIndex].innerText;
                const selectedDoc = links.find(link => link.label === selectedBoxLabel);
                const userConfirmed = window.confirm("🎉 You landed on: " + selectedDoc.label + ". Do you want to visit the link?");
                if (userConfirmed) {{
                    window.open(selectedDoc.url, "_blank");
                }}

                // Enable the spin button after 4 minutes
                setTimeout(() => {{
                    spinBtn.disabled = false;
                }}, 240000);  // 4 minutes in milliseconds
            }}, duration);
        }});
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=700)
