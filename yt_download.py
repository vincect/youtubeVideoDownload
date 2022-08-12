from pytube import YouTube
from sys import argv
import os
from pydoc import describe
import shutil
from datetime import datetime

while True:
    print(
        "#############################################################################"
    )
    print(
        "########                                                             ########"
    )
    print(
        "########               Please choose option to download              ########"
    )
    print(
        "########                                                             ########"
    )
    print(
        "########                    Choose a option:                         ########"
    )
    print(
        "########                                                             ########"
    )
    print(
        "########        1) Download single link                              ########"
    )
    print(
        "########        2) Download from file youtube.txt                    ########"
    )
    print(
        "########        3) Exit                                              ########"
    )
    print(
        "########                                                             ########"
    )
    print(
        "#############################################################################"
    )
    chosen_element = input("Enter a number from 1 to 3: ")
    if int(chosen_element) == 1:
        while True:

            link = input(
                "Enter the URL of the video you want to download(or Enter to quite): \n>> "
            )
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            print("Title:", yt.title)
            print("Author:", yt.author)
            print("Published date:", yt.publish_date.strftime("%Y-%m-%d"))
            print("Number of views:", yt.views)
            print("Length of video:", yt.length, "seconds")
            yd = yt.streams.get_highest_resolution()
            yd.download()
            # Write to log file to keep track
            with open("youtube.log", "a+", encoding="utf-8") as f:
                f.write("# " + yt.title + "\n")
                f.write(link + "\n")
            # break
    elif int(chosen_element) == 2:
        # ----------- Version 1------------------------
        # # Open file in read mode
        # yt_file = open('youtube.txt', 'r')

        # # Read
        # yt_data = yt_file.read()

        # # Replace and spit the text
        # yt_file_list = yt_data.split('\n')

        # # Close the file
        # yt_file.close()

        # for link in yt_file_list:
        #     yt = YouTube(link)
        #     print(f'Title: {yt.title}')
        #     print(f'Views: {yt.views}')
        #     #yd = yt.streams.get_by_resolution(resolution=1080)
        #     yd = yt.streams.get_highest_resolution()
        #     yd.download()
        # ----------- Version 1------------------------
        with open("youtube.txt", "r") as f:
            for link in f:
                # Ignore line with begin #
                if not link.startswith("#"):
                    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
                    print("Title:", yt.title)
                    print("Author:", yt.author)
                    print("Published date:", yt.publish_date.strftime("%Y-%m-%d"))
                    print("Number of views:", yt.views)
                    print("Length of video:", yt.length, "seconds")
                    yd = yt.streams.get_highest_resolution()
                    yd.download()
                    # Write to log file to keep track
                    with open("youtube.log", "a+", encoding="utf-8") as wf:
                        wf.write("# " + yt.title + "\n")
                        wf.write(link + "\n")
    elif int(chosen_element) == 3:
        # Get the current Directory
        parentDir = os.getcwd()

        # Create 'process' folder in current folder
        os.makedirs("process", exist_ok=True)
        # Create 'complete' folder in current folder
        os.makedirs("complete", exist_ok=True)

        processPath = os.path.join(parentDir, "process")
        completePath = os.path.join(parentDir, "complete")

        # Print all mp4 the file in 'parentDir'
        # for f in glob.glob(os.path.join(parentDir, '*.mp4')):
        #    print(f)

        # All mp4 files in 'parentDir'
        allfiles = os.listdir(parentDir)
        mp4Files = [fname for fname in allfiles if fname.endswith(".mp4")]
        # print (mp4Files)

        # Move all mp4 files to 'processPath'
        for f in mp4Files:
            # print(os.path.join(parentDir, f))
            shutil.move(os.path.join(parentDir, f), processPath)

        # Change to 'processFolder' and change name file
        os.chdir(processPath)
        for f in os.listdir():
            fTitle, fExt = os.path.splitext(f)
            fTitle = fTitle.title()
            fExt = fExt.lower()
            newName = "{}{}".format(fTitle, fExt)
            os.rename(f, newName)
            # Move all processed mp4 files to 'completePath'
            # shutil.move(os.path.join(processPath, newName), completePath)
            shutil.copy2(os.path.join(processPath, newName), completePath)
            os.remove(os.path.join(processPath, newName))
        break
    else:
        print("Sorry, the value entered must be a number from 1 to 3, then try again!")
