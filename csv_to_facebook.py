import pandas as pd

def generate_facebook_post(csv_path, location, name, host, num_guests):
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Remove the timestamp column
    df = df.iloc[:, 1:]

    # Convert all values to numeric, forcing errors to NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Compute statistics
    beer_stats = df.agg(['mean', 'min', 'max']).T
    beer_stats.columns = ['Avg', 'Min', 'Max']

    # Drop rows with only NaN values
    beer_stats = beer_stats.dropna()

    # Sort by average score (descending)
    beer_stats = beer_stats.sort_values(by='Avg', ascending=False)

    # Format the Facebook post
    post = f"🍺 {name} hos {location} 🍺\n"
    post += (
        f"I går afholdte {host} \"{name}\" hos {location}, "
        f"hvor {num_guests} deltagere fik fornøjelsen af at smage på nogle fantastiske øl! 🍻\n\n"
    )
    post += (
        "Øllene blev bedømt 1-10. Her er de rangeret fra højeste til laveste gennemsnit, "
        "sammen med deres laveste og højeste karakter:\n\n"
    )

    medals = ["🔥 Topscoreren 🔥", "🥈", "🥉"]
    for i, (beer, row) in enumerate(beer_stats.iterrows()):
        medal = medals[i] if i < 3 else "🍺"
        post += f"{medal} {beer}\n"
        post += (
            f"📉 Laveste: {int(row['Min'])} | "
            f"📈 Højeste: {int(row['Max'])} | "
            f"📊 Gennemsnit: {row['Avg']:.1f}\n\n"
        )

    post += "Tak til alle der deltog og var med til at skabe en hyggelig aften! Hvilken øl var jeres favorit?"

    return post


if __name__ == "__main__":
    print("=== Facebook Beer Tasting Post Generator ===\n")

    csv_file = input("Path to CSV file: ").strip()
    location = input("Event location: ").strip()
    name = input("Event name: ").strip()
    host = input("Event host(s): ").strip()

    while True:
        try:
            num_guests = int(input("Number of guests: ").strip())
            break
        except ValueError:
            print("Please enter a valid number.")

    post = generate_facebook_post(csv_file, location, name, host, num_guests)
    print("\n--- Generated Post ---\n")
    print(post)
