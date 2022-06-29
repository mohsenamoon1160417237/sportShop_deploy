#!/bin/sh +x

docker run -d \
--name=sportShop_openVpn \
--cap-add=NET_ADMIN \
-p 8181:8181 \
-p 3000:3000 \
-p 5432:5432 \
-p 80:80 \
-p 443:443 \
--device=/dev/net/tun \
-v "/$(pwd)/helpers/vpn:/data/vpn" \
--restart=unless-stopped \
ghcr.io/wfg/openvpn-client
