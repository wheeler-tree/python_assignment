from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from sqlalchemy import func
from math import ceil

from lib.alphavantage_api import AlphaVantageAPI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
Data model for StockTrade
{
    "symbol": "IBM",
    "date": "2023-02-14",
    "open_price": "153.08",
    "close_price": "154.52",
    "volume": "62199013",
}
'''
class StockTrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<StockTrade {self.symbol} {self.date} {self.open_price} {self.close_price} {self.volume}>'

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "date": str(self.date),
            "open_price": str(self.open_price),
            "close_price": str(self.close_price),
            "volume": str(self.volume),
        }


@app.route('/')
def index() -> str:
    return 'Hello World!'


@app.route('/create_db')
def create_db() -> str:
    db.create_all()
    return 'Create database succeed!'


def get_api_key():
    with open("conf/api_key", "r") as f:
        return f.read()

@app.route('/retrieve_raw_data')
def retrieve_raw_data() -> str:
    api_key = get_api_key()
    client = AlphaVantageAPI(api_key)

    response = client.get_daily_data_json("IBM")
    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))
    else:
        symbol = response.json()[AlphaVantageAPI.DEFAULT_META_DATA][AlphaVantageAPI.DEFAULT_SYMBOL_DATA]
        raw_data = response.json()[AlphaVantageAPI.DEFAULT_DATA_KEY]
        process_data = []
        for date, data in raw_data.items():
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            process_data.append(StockTrade(symbol=symbol, date=date_obj, open_price=data["1. open"], close_price=data["4. close"], volume=data["6. volume"]))

        # insert data into database
        db.session.add_all(process_data)
        db.session.commit()

    return 'Retrieve data succeed!'


@app.route('/api/financial_data', methods=['GET'])
def get_financial_data():
    # Get request parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    symbol = request.args.get('symbol')
    limit = int(request.args.get('limit', 5))
    page = int(request.args.get('page', 1))

    # Query conditions
    conditions = []
    if start_date:
        conditions.append(StockTrade.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        conditions.append(StockTrade.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    if symbol:
        conditions.append(StockTrade.symbol == symbol)

    # Count total records
    count = StockTrade.query.filter(*conditions).count()

    # Pagination calculations
    offset = (page - 1) * limit
    total_pages = ceil(count / limit)

    # Query records with pagination
    records = (
        StockTrade.query
        .filter(*conditions)
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Convert records to dictionary format
    data = [record.to_dict() for record in records]

    # Construct pagination object
    pagination = {
        "count": count,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }

    # Construct response object
    response = {
        "data": data,
        "pagination": pagination,
        "info": {"error": ""}
    }

    return jsonify(response)


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    # Get request parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    symbol = request.args.get('symbol')

    # Check if any parameter is missing
    if not start_date or not end_date or not symbol:
        response = {
            "data": {},
            "info": {"error": "Missing parameters"}
        }
        return jsonify(response), 400

    # Check if the end_date is None
    if end_date is None:
        response = {
            "data": {},
            "info": {"error": "Invalid end_date"}
        }
        return jsonify(response), 400

    # Query conditions
    conditions = [
        StockTrade.date >= datetime.strptime(start_date, '%Y-%m-%d').date(),
        StockTrade.date <= datetime.strptime(end_date, '%Y-%m-%d').date(),
        StockTrade.symbol == symbol
    ]

    # Calculate statistics
    average_daily_open_price = (
        db.session.query(func.avg(StockTrade.open_price))
        .filter(*conditions)
        .scalar()
    )
    average_daily_close_price = (
        db.session.query(func.avg(StockTrade.close_price))
        .filter(*conditions)
        .scalar()
    )
    average_daily_volume = (
        db.session.query(func.avg(StockTrade.volume))
        .filter(*conditions)
        .scalar()
    )

    # Construct response object
    response = {
        "data": {
            "start_date": start_date,
            "end_date": end_date,
            "symbol": symbol,
            "average_daily_open_price": average_daily_open_price,
            "average_daily_close_price": average_daily_close_price,
            "average_daily_volume": average_daily_volume
        },
        "info": {"error": ""}
    }

    return jsonify(response)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
