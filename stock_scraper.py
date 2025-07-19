# Import necessary libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from prophet import Prophet

# --- Selenium Setup ---

# Set up the Chrome webdriver
# This will automatically download the correct driver for your Chrome version
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the local FastAPI server
driver.get("http://127.0.0.1:8000")

# --- Data Scraping ---

# Scrape data from the FastAPI server
data = []
for _ in range(100): # Scrape 100 data points
    price_string = driver.find_element(By.TAG_NAME, "body").text
    price = float(price_string.split(":")[1].strip())
    data.append({
        'ds': pd.to_datetime('today').normalize() + pd.to_timedelta(_, unit='D'),
        'y': price
    })
    driver.refresh()

df = pd.DataFrame(data)

# Close the browser
driver.quit()

# --- Prophet Forecasting ---

# Ensure the dataframe has the required 'ds' and 'y' columns
if 'ds' in df.columns and 'y' in df.columns:

    # Initialize the Prophet model
    model = Prophet()

    # Fit the model to the data
    model.fit(df)

    # Create a future dataframe for predictions
    # We'll predict for the next 30 days
    future = model.make_future_dataframe(periods=30)

    # Make predictions
    forecast = model.predict(future)

    # --- Output and Visualization ---

    # Print the forecast
    print("Forecasted Data:")
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    # Plot the forecast
    # This will open a new window with the plot
    fig1 = model.plot(forecast)

    # Plot forecast components (trend, weekly, yearly seasonality)
    fig2 = model.plot_components(forecast)

else:
    print("Dataframe does not have the required 'ds' and 'y' columns.")
