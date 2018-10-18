# README

## PLEASE FOLLOW THE INSTRUCTIONS GIVEN BELOW TO TEST THE PROGRAM

1. Place/clone/extract the contents of the project to a directory of your choice.
2. Open terminal and go to the directory.
3. Since the data in the zip is already processed and ready to be used you dont need to run the ParseAndFormatData.py
4. Open the directory in the terminal and enter the command "python3 smoothing.py"
4.a. if it fails to run due to missing peakutils dependency, please run the following command to install the missing dependency:
"sudo pip install peakutils"
Then enter the command "python3 smoothing.py" to try again

5. It will ask you to enter a file name for input data:
Either enter one of the data file mentioned in the list below (these are the parts of files from the actual data set that we found to be consistent and hence we have selected )
Input options:
HD7924_sample.vels
HD108874_sample.vels
HD156668_sample.vels
HIP74995_sample.vels

Or type in the name of the file you want to load (see filenames from the "keck_vels_binned" directory)

Sample input:
HD1461_KECK.vels

6. Then it'll ask you to enter a window size (default is 21), you can enter any ODD value in it. This shall return you an estimate of time period. You can try out with various window size to get a suitable value of the initial guess.

7. You can use this value as the initial guess for P(time period) for the next step.

8. Then in terminal type the command "python3 TimePeriodDetector.py"

9. It will ask you to enter the star name: Type in the name of the star system you wanted to test(the names can be found in th "opdir_binned/" folder you have extracted)
Sample input:
HD7924
HD1461
HD156668

10. Then it will ask for an initial guess of the time period, type in the value you found from the previous program or the value that you think is your best guess for the time period by looking at the data.

11. Wait for the code to finish executing, this might take some time based on the size of the data set. When the code is done executing the "starname.png" image is created in the same directory as the python file and you will be shown a graph showing the plot of Chi square versus the time period.

12. The spikes you notice shall correspond to the probable exoplanet time periods in that star system under test.



## ADDITIONAL NOTES:

If you want to extract and process the data from scratch, follow these steps before the above steps
extract the keck_vels_binned.tar.gz in the same dir as the python files
The directory structure should look something like this

parentdir/keck_vels_binned
parentdir/keck_vels_binned.tar.gz
parentdir/ParseAndFormatData.py
parentdir/READ ME.txt
parentdir/smoothing.py
parentdir/TimePeriodDetector.py

The open this directoory in terminal and execute the command "python ParseAndFormatData.py"

It will convet all the *.vels file to csv files and dump it in the opdir_binned folder

Then you can continue from step 4 above and follow the same procedure for rest of the testing process.



