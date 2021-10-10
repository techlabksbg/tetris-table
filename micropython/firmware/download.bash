url=`curl https://micropython.org/download/esp32/ | grep GENERIC | grep -v unstable | grep 2021 | cut -f2 -d\" | head -n 1`
echo "Downloading $url"
file=`basename "$url"`
curl "https://micropython.org$url" -o "$file"

