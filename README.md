# autotok
Tool to automate tiktok content creation and upload. This tool allows you to setup multiple tiktok accounts in accounts.csv. The tool will search youtube using the predefined search parameters, download the video, edit it into parts, and upload them to tiktok.

# Disclaimer
This was a tool that I created years ago for personal use so please don't mind the messy code and repo structure. 

DO NOT use this tool to post copywrited content to TikTok for ad revenue. It is illegal and your account may be banned.

# setup instructions
1) **Install python dependencies**
    
    ```
    pip install selenium
    pip install google-api-python-client
    pip install moviepy
    pip install tiktok-uploader
    ```

2) **Setup Google API**
    
    Create a youtube API session and copy your api key. Paste your api key into contentFinder.py line 6.

3) **Enter tiktok account info into accounts.csv**
    
    Follow the format listed in the example row. Remove the example row when done.

4) **Fetch cookies**
    
    Run
    ```
    python cookies.py
    ```
    This will login to each account in a selenium browser to clone the cookies. This allows for seamless uploading without the need to login. Wait for the program to enter the username and password. Then, complete the capcha. Continue to complete the capchas until all your accounts have been logged in. The cookies should be saved in /cookies/. 

5) **Download secondary videos**
    
    If you wish to use editing style 2, you will need to create a directory "/secondary" and use the included youtube-dl tool to download videos to be used as the secondary videos to play under your main video.

# Usage
Run the tool with:
```
python main.py
```
The main menu will have a button for each account. Click on the account your wish to upload on. The tool will find a youtube video matching the search terms for that account. You can modify the number/length of parts to divide the video into and click yes. The tool will edit the videos into multiple parts and upload to your tiktok account. You can queue up multiple videos for multiple tiktok accounts at once. This way, you can let the tool edit and upload overnight for easy content creation.

# Editing Styles
### Style 1
Slightly zoom in on the main video, add a blurred background of the video, add a title, divide into parts. Example:
![](/assets/editStyle1.png)

### Style 2
Stack main video on top of random video from secondary folder, then edit everything else the same as style 1. Example:
![](/assets/editStyle2.png)