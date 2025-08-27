from flask import Flask, request, jsonify, redirect, render_template_string

app = Flask(__name__)

BASE_SALARY = 15000
EXP_BONUS_PER_MONTH = 1400
EXP_MAX_MONTHS = 60

EDU_BONUS = {
    "ม.6 หรือเทียบเท่า": 0,
    "ปริญญาตรี": 10000,
    "ปริญญาโท": 20000,
    "ปริญญาเอก": 30000,
}

def calc_salary(months: int, education: str) -> int:
    months = max(0, int(months))
    exp_bonus = min(months, EXP_MAX_MONTHS) * EXP_BONUS_PER_MONTH
    edu_bonus = EDU_BONUS.get(education, 0)
    return BASE_SALARY + exp_bonus + edu_bonus

# หน้าแรก
@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None
    if request.method == "POST":
        try:
            months = int(request.form.get("months", "0"))
            education = request.form.get("education", "ม.6 หรือเทียบเท่า")
            result = calc_salary(months, education)
        except (ValueError, TypeError):
            error = "กรุณากรอกจำนวนเดือนเป็นตัวเลข"

    html = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>คำนวณเงินเดือน</title>
        <style>
            body { font-family: sans-serif; background: #f9f9f9; padding: 30px; text-align: center; }
            form { background: white; padding: 20px; display: inline-block; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            input, select { padding: 10px; margin: 10px 0; width: 250px; }
            button { padding: 10px 20px; background: #ff6f61; border: none; color: white; font-weight: bold; cursor: pointer; border-radius: 5px; }
            button:hover { background: #ff4b3e; }
            .error { color: red; }
            .result { margin-top: 20px; font-size: 1.2em; font-weight: bold; }
            .nav { margin-top: 30px; }
            .nav a { margin: 0 10px; color: #555; text-decoration: none; font-weight: bold; }
            .nav a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>💰 โปรแกรมคำนวณเงินเดือน</h1>
        <form method="POST">
            <div>
                <label>ระบุจำนวนเดือนประสบการณ์:</label><br>
                <input type="number" name="months" min="0" max="100" required>
            </div>
            <div>
                <label>ระดับการศึกษา:</label><br>
                <select name="education">
                    {% for edu in edu_bonus.keys() %}
                        <option value="{{ edu }}">{{ edu }}</option>
                    {% endfor %}
                </select>
            </div>
            <button type="submit">คำนวณ</button>
        </form>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        {% if result %}
            <div class="result">💸 เงินเดือนที่ได้: {{ result }} บาท</div>
        {% endif %}

        <div class="nav">
            <a href="/about">👨‍👩‍👦‍👦 ผู้จัดทำ</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html,
        error=error,
        result=result,
        edu_bonus=EDU_BONUS
    )

# API สำหรับคำนวณแบบ JSON
@app.route("/api/calc", methods=["POST"])
def api_calc():
    data = request.get_json(force=True, silent=True) or {}
    months = int(data.get("months", 0))
    education = data.get("education", "ม.6 หรือเทียบเท่า")
    return jsonify({
        "salary": calc_salary(months, education),
        "base": BASE_SALARY,
        "exp_bonus_per_month": EXP_BONUS_PER_MONTH,
        "exp_capped_months": EXP_MAX_MONTHS,
        "education_bonus": EDU_BONUS.get(education, 0)
    })

# หน้าเกี่ยวกับผู้จัดทำ
@app.route("/about")
def about():
    authors = [
        "1. นายจารุวิทย์ เลขที่ 1 ห้อง 406",
        "2. นายธนภัทร เลขที่ 8 ห้อง 406",
        "3. นายนิชคุณ เลขที่ 11 ห้อง 406",
        "4. นายวสุธรณ์ เลขที่ 20 ห้อง 406",
    ]
    school = "🏫 โรงเรียนสวนกุหลาบวิทยาลัย รังสิต"

    html = """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>ผู้จัดทำ</title>
        <style>
            body { font-family: sans-serif; background: #fff8f0; padding: 30px; text-align: center; }
            .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); display: inline-block; }
            h1 { color: #ff6f61; }
            ul { list-style: none; padding: 0; font-size: 1.1em; }
            li { margin: 5px 0; }
            .school { margin-top: 20px; font-weight: bold; font-size: 1.2em; color: #333; }
            a { display: inline-block; margin-top: 20px; text-decoration: none; color: #555; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>👨‍💻 ผู้จัดทำ</h1>
            <ul>
                {% for a in authors %}
                    <li>{{ a }}</li>
                {% endfor %}
            </ul>
            <div class="school">{{ school }}</div>
            <a href="/">⬅ กลับหน้าคำนวณ</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, authors=authors, school=school)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
