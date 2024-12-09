from flask import Flask, jsonify, request, render_template, Response
from queries import Queries
import csv
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_customers', methods=['GET'])
def get_customers():
    shopkeeper_id = request.args.get('shopkeeper_id')
    if not shopkeeper_id:
        return jsonify({'message': 'Please provide shopkeeper ID'}), 400

    try:
        customers = Queries.get_all_customers(shopkeeper_id)
        if not customers:
            return jsonify({'message': 'No customers found for this shopkeeper'}), 200

        result = [{'full_name': customer[0]} for customer in customers]
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/get_all_transactions', methods=['GET'])
def get_all_transactions():
    shopkeeper_id = request.args.get('shopkeeper_id')
    if not shopkeeper_id:
        return jsonify({'message': 'Please provide shopkeeper ID'}), 400

    try:
        transactions = Queries.get_all_transactions(shopkeeper_id)
        if not transactions:
            return jsonify({'message': 'No transactions found for this shopkeeper'}), 200

        result = []
        for transaction in transactions:
            customer_id, date, you_give, you_got = transaction
            customer_name = Queries.get_customer_name(customer_id)
            if customer_name:
                result.append({
                    'full_name': customer_name,
                    'date': date,
                    'you_give': you_give,
                    'you_got': you_got
                })

        return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/filter_transactions', methods=['GET'])
def filter_transactions():
    shopkeeper_id = request.args.get('shopkeeper_id')
    from_date = request.args.get('from_date')
    till_date = request.args.get('till_date')
    customer_name = request.args.get('customer_name')

    if not shopkeeper_id:
        return jsonify({'message': 'Please provide shopkeeper ID'}), 400

    try:
        transactions = Queries.filter_transactions(shopkeeper_id, from_date, till_date, customer_name)
        if not transactions:
            return jsonify({'message': 'No transactions found for the selected criteria'}), 200

        result = []
        for transaction in transactions:
            customer_id, date, you_give, you_got = transaction
            customer_name = Queries.get_customer_name(customer_id)
            if customer_name:
                result.append({
                    'full_name': customer_name,
                    'date': date,
                    'you_give': you_give,
                    'you_got': you_got
                })

        return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/download_report', methods=['GET'])
def download_report():
    shopkeeper_id = request.args.get('shopkeeper_id')
    from_date = request.args.get('from_date')
    till_date = request.args.get('till_date')
    customer_name = request.args.get('customer_name')

    if not shopkeeper_id:
        return jsonify({'message': 'Please provide shopkeeper ID'}), 400

    try:
        transactions = Queries.filter_transactions(shopkeeper_id, from_date, till_date, customer_name)
        if not transactions:
            return jsonify({'message': 'No transactions found for the selected criteria'}), 200

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Customer Name', 'Date', 'You Give', 'You Got'])

        for transaction in transactions:
            customer_id, date, you_give, you_got = transaction
            customer_name = Queries.get_customer_name(customer_id)
            if customer_name:
                writer.writerow([customer_name, date, you_give, you_got])

        output.seek(0)
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=transactions_report.csv"}
        )
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

