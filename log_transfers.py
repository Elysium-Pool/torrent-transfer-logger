#!/usr/bin/env python3

# When run, this script logs the peers for each torrent in qBittorrent to a sqlite database. It is useful for performing analytics on download progress and total number of downloads of other peers for torrents you are seeding/downloading.
# Run this script in a cronjob or similar minutely. 

import qbittorrentapi
import logging
import time, datetime
import json
import pandas as pd
import sqlite3

sqle = sqlite3.connect('torrent_transfer_log.sqlite')

qbt_client = qbittorrentapi.Client(host='localhost:8080', username='admin', password='adminadmin')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

try:
	qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
	print(e)

def add_torrents_log():
	""" Add the current peer log to the database. """
	logger.info("Starting add_torrents_log().")

	for torrent in qbt_client.torrents_info():
		hash = torrent.hash

		peers = qbt_client.sync_torrent_peers(hash, rid=0).peers
		val = [({'peer': key} + val) for (key, val) in dict(peers).items()]

		df = pd.DataFrame(val)
		df['log_date'] = datetime.datetime.now()
		df['torrent_hash'] = hash
		df['torrent_state'] = torrent.state
		df['torrent_name'] = torrent.name

		if len(df.index) > 0:	
			df = df.set_index(['log_date', 'torrent_hash', 'peer'])
			df.to_sql('torrent_transfer_log', con=sqle, if_exists='append')

	logger.info('Done add_torrents_log().')

if __name__ == '__main__':
	add_torrents_log()

