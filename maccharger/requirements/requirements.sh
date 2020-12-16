echo Installer for linux by Castellani Davide >> ./../log/log.log

sudo apt-get install net-tools -y >> ./../log/log.log
sudo apt-get install python3 -y >> ./../log/log.log
sudo apt-get install python3-pip -y >> ./../log/log.log
sudo pip3 install -r ./requirements.txt >> ./../log/log.log

echo >> ./../log/log.log
