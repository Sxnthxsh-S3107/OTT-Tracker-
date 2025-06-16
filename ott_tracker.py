import requests

# 🔑 Replace with your TMDB API key
TMDB_API_KEY = "f6a5fe67ba66b63db1ce69c0af4d20f6"

# Ask user for platform name
platform_name = input("Enter OTT platform (like Netflix, Amazon Prime Video, Hotstar): ").lower()

# Function to fetch platform IDs from TMDB
def get_provider_id(name):
    url = f"https://api.themoviedb.org/3/watch/providers/movie?api_key={TMDB_API_KEY}&language=en-US&watch_region=IN"
    response = requests.get(url)
    data = response.json()

    for provider in data["results"]:
        if provider["provider_name"].lower() == name:
            return provider["provider_id"]
    return None

provider_id = get_provider_id(platform_name)

if provider_id:
    print(f"\n✅ Provider ID for {platform_name.title()}: {provider_id}")
else:
    print(f"\n❌ Could not find provider ID for {platform_name}. Try Netflix, Amazon Prime Video, etc.")
import datetime

# 📅 Date range: today and 7 days ago
today = datetime.date.today()
last_week = today - datetime.timedelta(days=7)

def get_recent_releases(content_type):  # 'movie' or 'tv'
    url = f"https://api.themoviedb.org/3/discover/{content_type}?api_key={TMDB_API_KEY}&language=en-US&sort_by=popularity.desc"
    url += f"&with_watch_providers={provider_id}&watch_region=IN"
    url += f"&release_date.gte={last_week}&release_date.lte={today}" if content_type == "movie" else f"&first_air_date.gte={last_week}&first_air_date.lte={today}"

    response = requests.get(url)
    data = response.json()

    results = data.get("results", [])
    return results

# 🍿 Fetch movies and TV shows
movies = get_recent_releases("movie")
tv_shows = get_recent_releases("tv")

# 🎬 Print Movies
print("\n🎬 Latest Movies:")
if movies:
    for m in movies[:5]:  # show top 5 only
        title = m.get('title', 'Unknown Title')
        rating = m.get('vote_average', 'N/A')
        release = m.get('release_date', 'N/A')
        overview = m.get('overview', 'No description available.')
        
        print(f"\n🎞️ {title} ({release})")
        print(f"⭐ IMDb Rating: {rating}/10")
        print(f"📖 Overview: {overview}")
        print("-" * 60)
else:
    print("No new movies found.")

# 📺 Print TV Shows
print("\n📺 Latest TV Series:")
if tv_shows:
    for tv in tv_shows[:5]:  # show top 5 only
        title = tv.get('name', 'Unknown Name')
        rating = tv.get('vote_average', 'N/A')
        release = tv.get('first_air_date', 'N/A')
        overview = tv.get('overview', 'No description available.')
        
        print(f"\n📺 {title} ({release})")
        print(f"⭐ IMDb Rating: {rating}/10")
        print(f"📖 Overview: {overview}")
        print("-" * 60)
else:
    print("No new TV shows found.")
