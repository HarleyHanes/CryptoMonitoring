#!/bin/bash
cd ~/var/CryptoMonitoring
/opt/bitnami/python/bin/python3  monitoringScripts/updateMarket.py
/opt/bitnami/python/bin/python3  monitoringScripts/updateMetrics.py
