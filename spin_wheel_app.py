import streamlit as st
from datetime import datetime, timedelta
from streamlit.components.v1 import html
import time

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

# Header Section
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image("college_logo.jpg", width=100)
with col2:
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Plot-A-Thon by TALOS</h1>", unsafe_allow_html=True)
with col3:
    st.image("talos_logo.jpeg", width=100)

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

# Display Cooldown Message if the button is disabled
cooldown_placeholder = st.empty()
if button_disabled:
    while button_disabled:
        minutes, seconds = divmod(time_remaining.total_seconds(), 60)
        cooldown_placeholder.markdown(f"⏳ **Please wait {int(minutes)} minutes and {int(seconds)} seconds** before spinning again.")
        time.sleep(1)  # Refresh every second
        time_now = datetime.now()
        time_remaining = cooldown_period - (time_now - st.session_state.last_spin_time)
        button_disabled = time_remaining.total_seconds() > 0
    cooldown_placeholder.empty()  # Clear the message once the cooldown ends

# Generate the HTML for the fixed boxes with a sliding box
box_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide Box</title>
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-size: cover;
            background-position: center center;
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
    <div class="box-container" id="box-container">
        <!-- Fixed boxes will be here -->
        <div class="box">{links[0]['label']}</div>
        <div class="box">{links[1]['label']}</div>
        <div class="box">{links[2]['label']}</div>
        <div class="box">{links[3]['label']}</div>
        <div class="box">{links[4]['label']}</div>
    </div>
    <div class="pointer" id="pointer"></div>
    <button id="spin-btn" {('disabled' if button_disabled else '')}>Spin the Boxes</button>

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
            }});

            // Start moving the pointer across the boxes
            let counter = 0;
            interval = setInterval(() => {{
                boxes.forEach((box, index) => {{
                    box.classList.remove("highlighted");
                }});
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

# Embed the sliding box HTML into Streamlit
html(box_html, height=400)
