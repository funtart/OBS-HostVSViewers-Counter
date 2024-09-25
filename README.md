# Obscounter + Countdown Timer + Sound Alerts

Python implementation of hotkey counter in OBS Studio.

![prevew](counter.gif)

# Requirements

For Windows install [python3.6](https://www.python.org/downloads/release/python-368/) 64 or 32 bit depending on your OBS. Since 28 version OBS Studio supports most 3.x Python versions.

# Installation 

1. Download [source code](https://github.com/upgradeQ/Obscounter/archive/master.zip).
2. Unzip the file to be able to access `points_counter_timer.py`. Remember the file location because you will need this later.

# Usage

1. On OBS, under Sources, click + to create a new text source (below, you will see Text GDI+). You may leave it blank.

![image](https://user-images.githubusercontent.com/2420577/214267000-44e091a0-eadb-43a2-ac68-d8763b172320.png)

2. On the OBS menu, click `Tools > Scripts`

![image](https://user-images.githubusercontent.com/2420577/214267186-562deac4-ee82-46df-8ebc-5278f9429f64.png)

3. Under the `Python Settings` tab, make sure the Python path is configured.

![image](https://user-images.githubusercontent.com/2420577/214267353-7155c08d-f9eb-4053-a17f-34ada6af86f5.png)

4. Under the `Scripts` tab, click the + sign to add this script.

![image](https://user-images.githubusercontent.com/2420577/214267447-cb5de6cc-5b98-44d6-bb5f-cccff76be836.png)

5. Close the scripts window, and return to your OBS window and configure OBS settings by clicking `File > Settings`.

6. Configure the hotkeys.

![ui](https://i.imgur.com/UobLYdS.png)

![hotkeys](https://i.imgur.com/dEC2Y6M.png)

## How do I use more counters?

If you need additional counters, duplicate the `points_counter_timer.py` file and save it with a new filename (e.g. `points_counter_timer2.py`), and repeat the process.


