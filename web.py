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
            background: rgba(0, 0, 0, 0.6);
            padding: 40px 50px;
            border-radius: 15px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            width: 350px;
            text-align: center;
        }

        h1 {
            margin-bottom: 30px;
            font-size: 36px;
            text-shadow: 0 2px 5px rgba(0,0,0,0.5);
        }

        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            margin-bottom: 25px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            outline: none;
            box-sizing: border-box;
        }

        input[type="submit"] {
            width: 100%;
            padding: 12px 15px;
            font-size: 20px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(255,75,43,0.6);
            transition: background 0.3s ease;
        }

        input[type="submit"]:hover {
            background: linear-gradient(45deg, #ff4b2b, #ff416c);
        }

        /* อนิเมชัน pulse เวลากดปุ่ม */
        @keyframes pulse {
          0% {
            box-shadow: 0 0 0 0 rgba(255, 75, 43, 0.7);
          }
          70% {
            box-shadow: 0 0 20px 10px rgba(255, 75, 43, 0);
          }
          100% {
            box-shadow: 0 0 0 0 rgba(255, 75, 43, 0);
          }
        }

        input[type="submit"]:active {
          animation: pulse 0.7s ease-out;
        }

        p, h2 {
            margin: 10px 0;
            font-weight: 600;
            text-shadow: 0 1px 3px rgba(0,0,0,0.7);
        }

        /* Responsive สำหรับมือถือ */
        @media (max-width: 480px) {
            .container {
                width: 90vw;
                padding: 30px 20px;
            }

            input[type="text"], input[type="submit"] {
                font-size: 16px;
                padding: 10px 12px;
            }

            h1 {
                font-size: 28px;
            }

            h2, p {
                font-size: 18px;
            }
        }

        /* Responsive สำหรับแท็บเล็ต */
        @media (min-width: 481px) and (max-width: 768px) {
            .container {
                width: 70vw;
                padding: 35px 30px;
            }

            input[type="text"], input[type="submit"] {
                font-size: 18px;
                padding: 11px 13px;
            }

            h1 {
                font-size: 32px;
            }

            h2, p {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Tax Calculator</h1>
        <form method="post" novalidate>
            <input type="text" name="salary" placeholder="Enter your monthly salary (THB)" required>
            <input type="submit" value="Calculate Tax">
        </form>
        {% if tax is not none %}
        <h2>Results:</h2>
        <p>Monthly Salary: {{ salary }} THB</p>
        <p>Tax to Pay: {{ tax }} THB</p>
        <p>Net Salary after Tax: {{ net_salary }} THB</p>
        {% endif %}
    </div>
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

