import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

class TravelAnalyzer:
    def __init__(self, db_name="travel.db"):
        self.db_name = db_name

    def load_data(self):
        """Reads data from SQLite into a DataFrame"""
        conn = sqlite3.connect(self.db_name)
        # We load all data
        df = pd.read_sql("SELECT * FROM hotels", conn)
        conn.close()
        return df

    def analyze_correlation(self):
        """Creates a scatter plot of Price vs Rating"""
        df = self.load_data()
        
        if df.empty:
            print("No data in database!")
            return

        print(f"Analyzing {len(df)} hotels...")
        
        # Create the Graph
        plt.figure(figsize=(10, 6))
        
        # Scatter plot: X axis = Price, Y axis = Rating
        plt.scatter(df['price'], df['rating'], alpha=0.6, c='blue', edgecolors='k')
        
        plt.title("Travel Analysis: Price vs Review Rating")
        plt.xlabel("Price (Yen)")
        plt.ylabel("Rating (0-5)")
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Save the graph as an image file
        filename = "analysis_result.png"
        plt.savefig(filename)
        print(f"Graph saved as '{filename}'")
        
        # Calculate and print a simple statistic
        avg_price = df['price'].mean()
        avg_rating = df['rating'].mean()
        print(f"Average Price: {avg_price:.0f} Yen")
        print(f"Average Rating: {avg_rating:.2f} / 5.0")

# --- EXECUTION ---
if __name__ == "__main__":
    analyzer = TravelAnalyzer()
    analyzer.analyze_correlation()