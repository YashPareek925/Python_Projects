import requests
import json
import csv

def fetchMovieData(apiKey, movieName):
    url=f"http://www.omdbapi.com/?apikey={apiKey}&t={movieName}"
    try:
        response=requests.get(url)
        response.raise_for_status()
        data=response.json()

        if data.get("Response")=="True":
            print(f"\nTitle:- {data['Title']}")
            print(f"Year:- {data['Year']}")
            print(f"Genre:- {data['Genre']}")
            print(f"Director:- {data['Director']}")
            print(f"IMDB Rating:- {data['imdbRating']}")
            print(f"Plot:- {data['Plot']}\n")

            # Save to CSV
            with open("movieData.csv","w",newline="",encoding="utf-8") as file:
                writer=csv.writer(file)
                writer.writerow(data.keys())
                writer.writerow(data.values())
            print("Data saved to movieData.csv")
        else:
            print(f"Error:{data.get('Error')}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed:{e}")

if __name__=="__main__":
    # Replace with your OMDb API key
    apiKey="yahanApnaKeyDaalo"
    movie=input("Enter a movie name:- ")
    fetchMovieData(apiKey, movie)