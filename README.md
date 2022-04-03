# Website Score Tool + SERP Parser

###### Made by @dkrwng ([GitHub](https://github.com/drkwng) | [Fiverr](https://www.fiverr.com/drkwng))

##Deploy
1. Install Docker:
`sudo apt-get update`
`sudo apt install docker.io`
`systemctl enable docker`
2. Clone the Git repo: https://github.com/drkwng/news-parse-and-score.git
3. Install docker-compose:
`sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
4. Apply executable permissons to the binary: `sudo chmod +x /usr/local/bin/docker-compose`
5. Create `.env` file in the root folder (just copy `.sample-env`). Change these vars values in file:
- POSTGRES_PASSWORD
- SECRET_KEY (you can generate it [here](https://djecrety.ir/))
- SERP_API (put your [VALUE SERP](https://www.valueserp.com/) API KEY)
6. Make `run.sh` in web_app folder executable: `sudo chmod +x run.sh`
7. Build Docker containers: `sudo docker-compose build`
8. Start website: `sudo docker-compose -d up`
9. Enter web_app container: `sudo docker exec -it <container_id> /bin/sh`
To get <container_id> type in terminal: `sudo docker ps`
10. Create superuser (while being in the web_app docker container): `python manage.py createsuperuser`
11. Load dump data: `python manage.py loaddump`

___________________________________

## How to use

1. Go to `/admin` URL and Sign In.
2. In "Queries" add your search query and location.
3. Then select the query (checkbox), choose "Get SERP Data" in dropdown on the top of the page and press "Go".
4. The parser will make requests to all websites with available=True param in "Websites" catalogue.
You can re-check available website status by selecting it in checkbox and choosing "Check website available status" in dropdown on the top of the page.
5. In "Query Check" you can score websites (1-10) and make notes lean on SERP Data by the search query. Filter by query and date will help you be more efficient. 
6. Website name, URL, score and some other data you can also see on website frontend by clicking a certain query on Homepage.


By @dkrwng ([GitHub](https://github.com/drkwng) | [Fiverr](https://www.fiverr.com/drkwng))