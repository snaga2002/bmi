from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>BMI Calculator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    <style>
        body {
            background: linear-gradient(135deg, #72edf2 10%, #5151e5 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .bmi-card {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 15px;
            padding: 30px;
            width: 350px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            text-align: center;
        }
        .output {
            font-weight: bold;
            font-size: 1.5rem;
            margin-top: 20px;
        }
        input[type=range] {
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="bmi-card">
        <h2>BMI Calculator</h2>
        <form method="POST" action="/">
            <div class="mb-3 text-start">
                <label for="weight" class="form-label">Weight (kg): <span id="weightVal">{{ weight }}</span></label>
                <input type="range" class="form-range" min="30" max="150" step="0.1" id="weight" name="weight" value="{{ weight }}" oninput="weightVal.innerText = this.value" />
            </div>
            <div class="mb-3 text-start">
                <label for="height" class="form-label">Height (cm): <span id="heightVal">{{ height }}</span></label>
                <input type="range" class="form-range" min="100" max="220" step="0.1" id="height" name="height" value="{{ height }}" oninput="heightVal.innerText = this.value" />
            </div>
            <button type="submit" class="btn btn-primary w-100">Calculate</button>
        </form>

        {% if bmi is not none %}
        <div class="output">
            Your BMI: <span>{{ bmi }}</span><br />
            Status: <span class="{{ color_class }}">{{ category }}</span>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "text-warning"
    elif 18.5 <= bmi < 25:
        return "Healthy", "text-success"
    elif 25 <= bmi < 30:
        return "Overweight", "text-danger"
    else:
        return "Obese", "text-danger"

@app.route("/", methods=["GET", "POST"])
def home():
    bmi = None
    category = None
    color_class = ""
    weight = 70
    height = 170
    if request.method == "POST":
        try:
            weight = float(request.form.get("weight", 70))
            height = float(request.form.get("height", 170))
            bmi = calculate_bmi(weight, height)
            category, color_class = bmi_category(bmi)
        except Exception:
            bmi = None
            category = None
            color_class = ""
    return render_template_string(TEMPLATE, bmi=bmi, category=category, color_class=color_class, weight=weight, height=height)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
