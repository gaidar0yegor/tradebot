# tradebot

Binance Trading Bot with Flask Web Interface

 Overview

This project is a multithreaded trading bot for the Binance exchange, featuring a Flask-based web interface. The bot makes real-time trading decisions based on the **RSI (Relative Strength Index)** and **Moving Averages** indicators and communicates with Binance API to place buy and sell orders.

 Features

- Multithreading**: Run multiple bots simultaneously, each with its own parameters.
- Real-time Data**: The bot connects to Binance's WebSocket to receive real-time candlestick data.
- Web Interface**: Users can launch and configure bots through an intuitive web interface built with Flask.
- Technical Indicators**:
  - RSI (Relative Strength Index): Used to detect overbought and oversold conditions.
  - Moving Averages (MA1, MA2, MA3): Used to analyze trends and support buy/sell decisions.
- Stop-Loss Functionality**: The bot automatically closes trades when the price falls below a set stop-loss percentage.
- Real-time Chart**: The web interface displays real-time updates for price and RSI using `Chart.js`.

 Project Structure

```
/project_directory/
├── app.py                # Flask app with multithreading and WebSocket support
├── bot_script.py         # Python script containing the main logic of the trading bot
├── config.py             # Configuration file for Binance API keys
├── /templates/           # HTML templates for the web interface
│   ├── index.html        # HTML form to input bot parameters
│   └── chart.html        # Page displaying a real-time chart
├── /static/              # Static files (e.g., CSS, JS)
```

 Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up API keys:
   - Open the `config.py` file and add your Binance API key and secret:
     ```python
     API_KEY = 'your_api_key'
     API_SECRET = 'your_api_secret'
     ```

4. Run the Flask app:
   ```
   python app.py
   ```

5. Access the web interface:
   - Open a web browser and go to `http://127.0.0.1:5000/`.

 Usage

1. On the home page, fill out the form with parameters such as:
   - RSI period
   - Trading symbol (e.g., ETHUSDT)
   - Trade quantity
   - Budget
   - Stop-loss percentage
   - Moving Averages periods (MA1, MA2, MA3)

2. After launching the bot, the web interface will display a real-time chart showing price movements and RSI data.

License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
