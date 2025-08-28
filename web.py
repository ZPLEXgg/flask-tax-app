from flask import Flask, request
import os

app = Flask(__name__)

# --- ค่าพื้นฐาน ---
BASE_SALARY = 15000
EXP_BONUS_PER_MONTH = 1400
EXP_MAX_MONTHS = 60
EDU_BONUS = {
    "ม.6 หรือเทียบเท่า": 0,
    "ปริญญาตรี": 10000,
    "ปริญญาโท": 20000,
    "ปริญญาเอก": 30000,
}

# --- ฟังก์ชันคำนวณเงินเดือน ---
def calc_salary(months: int, education: str) -> int:
    months = max(0, int(months))
    exp_bonus = min(months, EXP_MAX_MONTHS) * EXP_BONUS_PER_MONTH
    edu_bonus = EDU_BONUS.get(education, 0)
    return BASE_SALARY + exp_bonus + edu_bonus

# --- ฟังก์ชันคำนวณภาษีรายปี ---
def calc_tax(income: int) -> int:
    tax = 0
    if income <= 150000:
        tax = 0
    elif income <= 300000:
        tax = (income - 150000) * 0.05
    elif income <= 500000:
        tax = (150000 * 0.05) + (income - 300000) * 0.1
    elif income <= 750000:
        tax = (150000 * 0.05) + (200000 * 0.1) + (income - 500000) * 0.15
    else:
        tax = (150000 * 0.05) + (200000 * 0.1) + (250000 * 0.15) + (income - 750000) * 0.2
    return int(tax)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            months = int(request.form.get("months", "0"))
            education = request.form.get("education", "ม.6 หรือเทียบเท่า")
            salary = calc_salary(months, education)
            tax = calc_tax(salary * 12)
            net_income = (salary * 12) - tax
            result = {"salary": salary, "yearly": salary * 12, "tax": tax, "net": net_income}
        except Exception:
            error = "ข้อมูลไม่ถูกต้อง กรุณากรอกใหม่"

    return f"""
    <html>
    <head>
        <title>คำนวณเงินเดือน & ภาษี</title>
        <style>
            body {{ font-family: Arial; background: linear-gradient(135deg, #6a11cb, #2575fc); padding: 30px; }}
            .container {{ max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.2); }}
            h2 {{ text-align: center; color: #333; }}
            label {{ display: block; margin-top: 10px; font-weight: bold; }}
            input, select, button {{ width: 100%; padding: 10px; margin-top: 5px; border-radius: 8px; border: 1px solid #ccc; }}
            button {{ background: linear-gradient(45deg,#ff416c,#ff4b2b); color: white; font-weight: bold; border:none; cursor:pointer; }}
            button:hover {{ background: linear-gradient(45deg,#ff4b2b,#ff416c); }}
            .result {{ margin-top: 20px; padding: 15px; background: #f1f1f1; border-radius: 8px; }}
            .error {{ color: red; }}
            .author {{ margin-top: 20px; background:#ffeaa7; padding:10px; border-radius:8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>คำนวณเงินเดือน & ภาษี</h2>
            <form method="POST">
                <label>จำนวนเดือนที่ทำงาน</label>
                <input type="number" name="months" required>
                
                <label>วุฒิการศึกษา</label>
                <select name="education">
                    <option>ม.6 หรือเทียบเท่า</option>
                    <option>ปริญญาตรี</option>
                    <option>ปริญญาโท</option>
                    <option>ปริญญาเอก</option>
                </select>
                
                <button type="submit">คำนวณ</button>
            </form>

            {"<p class='error'>" + error + "</p>" if error else ""}
            {f"""
            <div class='result'>
                <p><b>เงินเดือนต่อเดือน:</b> {result['salary']:,} บาท</p>
                <p><b>รายได้ต่อปี:</b> {result['yearly']:,} บาท</p>
                <p><b>ภาษีที่ต้องจ่าย:</b> {result['tax']:,} บาท</p>
                <p><b>รายได้สุทธิหลังหักภาษี:</b> {result['net']:,} บาท</p>
            </div>
            """ if result else ""}

            <div class="author">
                <p><b>ผู้จัดทำ:</b></p>
                <p>1. นายจารุวิทย์ เลขที่1 ห้อง406</p>
                <p>2. นายธนภัทร เลขที่8 ห้อง406</p>
                <p>3. นายนิชคุณ เลขที่11 ห้อง406</p>
                <p>4. นายวสุธรณ์ เลขที่21 ห้อง406</p>
                <p><b>โรงเรียน:</b> โรงเรียนสวนกุหลาบวิทยาลัย รังสิต</p>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
