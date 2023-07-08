from lib.alphavantage_api import AlphaVantageAPI


def get_api_key():
    with open("conf/api_key", "r") as f:
        return f.read()
    
def execute():
    api_key = get_api_key()
    client = AlphaVantageAPI(api_key)

    resp = client.get_daily_data_json("IBM")
    print(resp)

if __name__ == "__main__":
    execute()