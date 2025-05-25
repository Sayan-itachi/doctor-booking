from flask import Flask, render_template_string, request, jsonify
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# Placeholder for WhatsApp API integration
WHATSAPP_API_URL = "https://api.whatsapp.com/send"
DOCTOR_PHONE = "9101136619"

# Generate appointment slots for the next 7 days
def generate_slots():
    today = datetime.today()
    slots = {}
    for i in range(7):
        day = today + timedelta(days=i)
        date_str = day.strftime('%Y-%m-%d')
        weekday = day.weekday()
        slots[date_str] = []

        if weekday == 6:
            start_hour = 10
            start_minute = 30
            end_hour = 15
        else:
            start_hour = 15
            start_minute = 0
            end_hour = 19

        current_time = datetime(day.year, day.month, day.day, start_hour, start_minute)
        end_time = datetime(day.year, day.month, day.day, end_hour, 0)

        while current_time + timedelta(hours=2) <= end_time:
            end_slot = current_time + timedelta(hours=2)
            slot_str = f"{current_time.strftime('%H:%M')} - {end_slot.strftime('%H:%M')}"
            slots[date_str].append(slot_str)
            current_time += timedelta(minutes=30)

    return slots

@app.route('/')
def index():
    slots = generate_slots()
    return render_template_string(PAGE_HTML, slots=slots)

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    name = data.get('name')
    date = data.get('date')
    time_slot = data.get('slot')
    premium = data.get('premium')

    customer_message = (
        f"\U0001F4C5 *Appointment Confirmed!*\n"
        f"\U0001F464 Name: {name}\n"
        f"\U0001F4C5 Date: {date}\n"
        f"\U0001F552 Time: {time_slot}\n"
        f"\U0001F31F Type: {'Premium' if premium else 'Standard'}\n\n"
        f"\U0001F4DE You will receive a confirmation call shortly to verify your booking and answer any questions you may have.\n"
        f"\U0001F4E9 If you need assistance, reply to this message or contact us at +91-9101136619.\n\n"
        f"\U0001F64F Thank you for trusting us. We look forward to serving you!\n\n"
        f"\U0001F501 *আপোনাৰ সময় ঠিক হৈছে!*\n"
        f"\U0001F464 নাম: {name}\n"
        f"\U0001F4C5 তাৰিখ: {date}\n"
        f"\U0001F552 সময়: {time_slot}\n"
        f"\U0001F31F ধৰণ: {'প্ৰিমিয়াম' if premium else 'ষ্টেণ্ডাৰ্ড'}\n\n"
        f"\U0001F4DE আপোনালোকক শীঘ্ৰে এটা নিশ্চিতকৰণ কল কৰা হ'ব, য'ত আপোনাৰ প্ৰশ্নৰো উত্তৰ দিয়া হ'ব।\n"
        f"\U0001F4E9 সহায়ৰ প্ৰয়োজন হ'লে, অনুগ্ৰহ কৰি এই মেছেজৰ উত্তৰ দিয়ক অথবা যোগাযোগ কৰক: +91-9101136619\n\n"
        f"\U0001F64F আপোনাৰ বিশ্বাসৰ বাবে ধন্যবাদ। আপোনাক সেৱা আগবঢ়াবলৈ আমালোক অপেক্ষাত আছো।"
    )

    send_whatsapp_message(DOCTOR_PHONE, customer_message)
    return jsonify({"success": True, "message": "Booking confirmed! You'll get a WhatsApp confirmation shortly."})

def send_whatsapp_message(number, text):
    print(f"[Simulated] Sending WhatsApp to {number}: {text}")
    # Simulate sending - replace with actual API

PAGE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doctor Appointment Booking</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #e0f7fa, #ffffff);
            margin: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            max-width: 450px;
            width: 100%;
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
            color: #00796b;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 6px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        button {
            background-color: #00796b;
            color: white;
            border: none;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #004d40;
        }
        .premium-label {
            display: flex;
            align-items: center;
            margin-top: 10px;
        }
        .premium-label input {
            width: auto;
            margin-right: 10px;
        }
        #response {
            text-align: center;
            font-weight: bold;
            color: green;
        }
    </style>
</head>
<body>
<div class="card">
    <h2>Book Your Appointment</h2>
    <input type="text" id="name" placeholder="Your Name" required>
    <select id="date" onchange="loadSlots()">
        {% for date in slots %}
        <option value="{{ date }}">{{ date }}</option>
        {% endfor %}
    </select>
    <select id="slot"></select>
    <label class="premium-label">
        <input type="checkbox" id="premium"> Book Premium (₹100)
    </label>
    <button onclick="submitBooking()">📩 Confirm Booking</button>
    <p id="response"></p>
</div>
<script>
    const allSlots = {{ slots|tojson }};
    function loadSlots() {
        const date = document.getElementById('date').value;
        const slotSelect = document.getElementById('slot');
        slotSelect.innerHTML = '';
        allSlots[date].forEach(slot => {
            const opt = document.createElement('option');
            opt.value = slot;
            opt.textContent = slot;
            slotSelect.appendChild(opt);
        });
    }
    function submitBooking() {
        const name = document.getElementById('name').value;
        const date = document.getElementById('date').value;
        const slot = document.getElementById('slot').value;
        const premium = document.getElementById('premium').checked;

        if (!name || !date || !slot) {
            document.getElementById('response').textContent = "Please fill all the fields.";
            return;
        }

        fetch('/book', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, date, slot, premium})
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('response').textContent = data.message;
        });
    }
    loadSlots();
</script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
