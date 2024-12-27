# Twitter Trending Topics Scraper

This project is a web application that scrapes the top 5 trending topics from Twitter's "What's Happening" section using Selenium and a proxy server. The results, including the timestamp and the proxy IP used, are stored in MongoDB and displayed on a user-friendly HTML page.

## Features

- **Web Scraping**: Uses Selenium to log in to Twitter and scrape trending topics.
- **Proxy Support**: Implements ProxyMesh to send requests via a proxy server.
- **MongoDB Integration**: Stores the scraped topics along with metadata in a MongoDB database.
- **Web Interface**: Provides an HTML page to trigger the scraping script and display results dynamically.
- **JSON Record Display**: Displays the MongoDB record as a JSON extract on the webpage.

## Prerequisites

Before running this project, ensure you have the following:
- Python installed on your system.
- MongoDB instance (local or hosted) with the connection URI.
- ProxyMesh credentials.
- Twitter account credentials.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/qbikle/twitter-trending.git
   cd twitter-trending
   ```

2. **Install Dependencies**:
   Use `requirements.txt` to install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment**:
   Update the required credentials in the `app.py` file:
   ```python
   MONGO_URI = "YourMongoDBURI"
   proxy_address = "YourProxyAddress"
   proxy_username = "YourProxyUsername"
   proxy_password = "YourProxyPassword"
   twitter_username = "TwitterUsername"
   twitter_password = "TwitterPassword"
   twitter_mail = "TwitterMail"
   ```

4. **Run the Application**:
   Start the Flask app:
   ```bash
   python app.py
   ```

5. **Access the Web Interface**:
   Open your browser and navigate to `http://127.0.0.1:5000/`.

## How to Use

1. **Trigger the Script**:
   - On the webpage, click the **"Click here to run the script"** button. This will:
     - Log in to Twitter using the provided credentials.
     - Scrape the top 5 trending topics.
     - Store the results in MongoDB.

2. **View Results**:
   - The results are displayed in the following format:
     ```
     These are the most happening topics as on {Date and Time of end of Selenium Script}:
     - Name of trend1: Topic1
     - Name of trend2: Topic2
     - Name of trend3: Topic3
     - Name of trend4: Topic4
     - Name of trend5: Topic5

     The IP address used for this query was: XXX.XXX.XXX.XXX

     Here’s a JSON extract of this record from the MongoDB:
     [
       {
         "_id": { "XXX": "XXXXXXX" },
         "topics": ["Topic1", "Topic2", "Topic3", "Topic4", "Topic5"],
         "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
         "proxy_ip": "XXX.XXX.XXX.XXX"
       }
     ]
     ```

3. **Run Again**:
   - Click the button again to refresh the data.

## File Structure

```
Twitter-Trending-Scraper/
├── app.py                 # Flask backend and Selenium script
├── templates/
│   └── index.html         # HTML template for the web interface
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Dependencies

- `Flask`: Web framework.
- `Selenium`: Web scraping automation.
- `selenium-wire`: Proxy support for Selenium.
- `pymongo`: MongoDB integration.
- `webdriver-manager`: Manages WebDriver installations.

## Notes

- Ensure the Twitter credentials are valid and have access to the "What's Happening" section.
- MongoDB must be accessible using the provided `MONGO_URI`.
- ProxyMesh credentials must be active for proper functionality.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
