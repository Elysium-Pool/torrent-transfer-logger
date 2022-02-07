# torrent-transfer-logger
A tool for logging the peers connected to qBittorrent, transferring the same files as you

## Setup/Usage
* Install requirements (`pip install -r requirements.txt`).
* Duplicate `config_sample.json` to `config.json`. Fill `config.json` as applicable.
* Run `log_transfers.py` to create the sqlite database and log into a table in that database.
* Add a cron job.

## Next Steps
In the future, useful analysis may include:
* For each torrent in the table, see how many have a download progress greater than 0.2 (thus, they likely downloaded the file).
* Calculate total seed ratios with the total amount uploaded.
* See how many IP addresses/peers have a high progress for multiple torrents, and thus are potentially subscribed to an RSS feed in common.
