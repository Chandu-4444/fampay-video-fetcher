from fampay.celery import app as celery_app
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import os
from api.models import Result
import datetime


@celery_app.task
def fetch_results(query=os.environ.get("SEARCH_QUERY", "cricket")):
    # API information
    api_service_name = "youtube"
    api_version = "v3"

    # List through the API_KEY to use the one which is not expired.
    for key in os.environ.get("API_KEY").split():
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key)
        try:

            # A sentinel value to start with the first page of results.
            next_page_token = "INITIAL PAGE"

            # We'll start from fetching the recently fetched result that was stored in the database.
            # If the database is empty, we'll start from the current timestamp.
            if Result.objects.exists():
                limit_time = Result.objects.all().order_by("publish_time").first().publish_time.isoformat()
            else:
                limit_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

            while next_page_token:

                request = youtube.search().list(
                    type="video",
                    order="date",
                    publishedAfter="2010-01-01T00:00:00Z",
                    publishedBefore=limit_time,
                    part="snippet",
                    maxResults=1000,
                    q=query,
                    pageToken=None if next_page_token == "INITIAL PAGE" else next_page_token,
                )

                response = request.execute()
                next_page_token = response.get("nextPageToken", None)

                for item in response["items"]:

                    # We only want to store unique results. Not necessary, but a sanitary measure.
                    if Result.objects.values("video_id").filter(video_id=item["id"]["videoId"]).exists():
                        continue
                    else:
                        result = Result(
                            title=item["snippet"]["title"],
                            description=item["snippet"]["description"],
                            thumbnail=item["snippet"]["thumbnails"]["default"]["url"],
                            video_id=item["id"]["videoId"],
                            publish_time=item["snippet"]["publishedAt"]
                        )
                        result.save()
        except HttpError:
            print("Iterating the API keys...")
            continue
        else:
            break
