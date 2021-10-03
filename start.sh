echo "Cloning Repo, Please Wait..."
git clone -b master https://github.com/ZauteKm/Instagram.git /Instagram
cd /Instagram
echo "Installing Requirements..."
pip3 install -r requirements.txt
echo "Starting Bot, Please Wait..."
python3 main.py
