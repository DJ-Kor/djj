echo "download start"

curl --retry 8 -s -L \
     --output kibana.tar.gz \
      https://artifacts.elastic.co/downloads/kibana/kibana-8.11.4-linux-$(arch).tar.gz

echo "download done"

# 여기에 압축풀기
# tar --strip-components=1 -zxf ./kibana.tar.gz

# kibana에 압축풀기
tar -zxf ./kibana.tar.gz 

echo "unzip done"
