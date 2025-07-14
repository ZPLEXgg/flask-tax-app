from flask import Flask, render_template_string, request

app = Flask(__name__)

html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Tax Calculator</title>
    <style>
        /* พื้นฐาน */
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
        }

        .container {
            background: rgba(0, 0, 0, 0.7);
            padding: 40px 50px;
            border-radius: 15px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
            width: 370px;
            text-align: center;
            position: relative;
        }

        h1 {
            margin-bottom: 5px;
            font-size: 36px;
            text-shadow: 0 2px 5px rgba(0,0,0,0.6);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }

        /* ไอคอนเงิน (SVG) */
        .icon-money {
            width: 36px;
            height: 36px;
            fill: #ffb74d;
            filter: drop-shadow(0 0 2px rgba(0,0,0,0.5));
        }

        p.description {
            margin: 8px 0 25px 0;
            font-size: 16px;
            color: #ddd;
            font-style: italic;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        }

        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            margin-bottom: 20px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            outline: none;
            box-sizing: border-box;
        }

        input[type="submit"], button {
            width: 48%;
            padding: 12px 15px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,0,0,0.4);
            transition: background 0.3s ease;
            color: white;
        }

        input[type="submit"] {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            box-shadow: 0 5px 15px rgba(255,75,43,0.6);
        }

        input[type="submit"]:hover {
            background: linear-gradient(45deg, #ff4b2b, #ff416c);
        }

        button#reset-btn {
            background: #777;
            box-shadow: 0 5px 15px rgba(100,100,100,0.6);
        }
        button#reset-btn:hover {
            background: #555;
        }

        button#authors-btn {
            margin-top: 25px;
            width: 100%;
            background: #4caf50;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.6);
            font-size: 18px;
        }
        button#authors-btn:hover {
            background: #388e3c;
        }

        /* เส้นแบ่ง */
        hr.divider {
            margin: 25px 0 15px 0;
            border: none;
            height: 1.5px;
            background: linear-gradient(to right, transparent, #ff4b2b, transparent);
            box-shadow: 0 1px 6px #ff4b2b;
        }

        /* ผลลัพธ์ */
        h2 {
            margin-bottom: 10px;
            font-size: 28px;
            text-shadow: 0 2px 5px rgba(0,0,0,0.6);
        }

        p.result {
            margin: 6px 0;
            font-weight: 600;
            font-size: 18px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.7);
        }

        /* ปุ่ม container เล็กๆ */
        .btn-group {
            display: flex;
            justify-content: space-between;
            gap: 10px;
        }

        /* Responsive มือถือ */
        @media (max-width: 480px) {
            .container {
                width: 90vw;
                padding: 30px 20px;
            }

            h1 {
                font-size: 28px;
            }

            p.description {
                font-size: 14px;
            }

            input[type="text"], input[type="submit"], button {
                font-size: 16px;
                padding: 10px 12px;
            }

            h2 {
                font-size: 24px;
            }

            p.result {
                font-size: 16px;
            }
        }

        /* Responsive แท็บเล็ต */
        @media (min-width: 481px) and (max-width: 768px) {
            .container {
                width: 70vw;
                padding: 35px 30px;
            }

            h1 {
                font-size: 32px;
            }

            p.description {
                font-size: 15px;
            }

            input[type="text"], input[type="submit"], button {
                font-size: 18px;
                padding: 11px 13px;
            }

            h2 {
                font-size: 26px;
            }

            p.result {
                font-size: 17px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>
            <svg class="icon-money" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M12 1C5.925 1 1 5.925 1 12s4.925 11 11 11 11-4.925 11-11S18.075 1 12 1zm0 20c-4.963 0-9-4.037-9-9s4.037-9 9-9 9 4.037 9 9-4.037 9-9 9zm-.5-13v2.5h-3v3h3v2.5h3v-2.5h2v-3h-2V8h-3z"/>
            </svg>
            Tax Calculator
        </h1>
        <p class="description">กรอกเงินเดือนรายเดือนของคุณ แล้วกดคำนวณภาษีได้เลย!</p>
        <form method="post" novalidate>
            <input type="text" name="salary" placeholder="Enter your monthly salary (THB)" required autocomplete="off" value="{{ salary if salary else '' }}">
            <div class="btn-group">
                <input type="submit" value="Calculate Tax">
                <button type="button" id="reset-btn" onclick="resetForm()">Reset</button>
            </div>
        </form>

        {% if tax is not none %}
        <hr class="divider">
        <h2>Results:</h2>
        <p class="result">Monthly Salary: {{ salary }} THB</p>
        <p class="result">Tax to Pay: {{ tax }} THB</p>
        <p class="result">Net Salary after Tax: {{ net_salary }} THB</p>
        {% endif %}

        <button id="authors-btn" onclick="showAuthors()">ผู้จัดทำ</button>
    </div>

    <script>
        function showAuthors() {
            alert(
                "ผู้จัดทำ:\\n\\n" +
                "1. นายจารุวิทย์ เลขที่ 1 ห้อง 406\\n" +
                "2. นายธนภัทร เลขที่ 8 ห้อง 406\\n" +
                "3. นายนิชคุณ เลขที่ 11 ห้อง 406\\n" +
                "4. นายวสุธรณ์ เลขที่ 20 ห้อง 406\\n\\n" +
                "โรงเรียนสวนกุหลาบวิทยาลัย รังสิต"
            );
        }

        function resetForm() {
            document.querySelector('input[name="salary"]').value = '';
        }
    </script>
</body>
</html>
'''

def calculate_tax(salary):
    tax = 0
    if salary <= 15000:
        tax = 0
    elif salary <= 30000:
        tax = (salary - 15000) * 0.05
    elif salary <= 50000:
        tax = (15000 * 0.05) + (salary - 30000) * 0.10
    else:
        tax = (15000 * 0.05) + (20000 * 0.10) + (salary - 50000) * 0.15
    return round(tax, 2)

@app.route('/', methods=['GET', 'POST'])
def home():
    tax = None
    salary = None
    net_salary = None
    if request.method == 'POST':
        salary_text = request.form.get('salary')
        try:
            salary = float(salary_text)
            if salary < 0:
                tax = 'Invalid salary!'
            else:
                tax = calculate_tax(salary)
                net_salary = round(salary - tax, 2)
        except:
            tax = 'Invalid input!'

    return render_template_string(html, tax=tax, salary=salary, net_salary=net_salary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
