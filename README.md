# push-api-sdk-tutorial

This project follows the Pushing single items and batches of items tutorial at https://levelup.coveo.com/learn/courses/using-the-push-api/lessons/using-the-push-api-sdk-for-python.

Following the steps in the tutorial wasn't easy, as a few adjustments were needed.

Under "SET UP YOUR PROJECT" 

Step 2: (Recommended) Create and activate a Python virtual environment for your project.  Instead of following the tutorial code, the code below works for me.

$ python -mvenv env
$ source env/Scripts/activate

Note: not mentioned in the tutorial, but to deactivate the virtual environment, type "deactivate" in the command line
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

Step 3: Run this command in your terminal to install the SDK:

$ pip install git+https://github.com/coveo-labs/SDK-Push-Python

When I ran the above command using my work computer (which is behind a firewall), I received an error msg
I tried running this line on my personal computer, and it works

When you clone this repo, I initially place the directory in my project env folder, whereas coveopush is needed in Python's 'site-packages' folder.  In my case, it is "C:\Python310\Lib\site-packages"

If you place the packages anywhere else and run your Python script (later in the tutorial), you will receive a coveopush module not found error.  After moving the coveopush folder to its proper location ("C:\Python310\Lib\site-packages"), the "module not found" error was resolved.   I began receiving other "modules not found" errors.  After placing the folder from my project's site-packages directory to Python's site-packages directory, I no longer received module not found errors.

I found this out from where the requests and jsonpickle were located after following Step 4.

NOTE:  I have included the required modules in this repo under 'python_packages_for_Coveo' for your convenience.

       - certifi
       - charset_normalizer
       - coveopush
       - idna
       - jsonpickle
       - requests
       - urllib3

====================================

The tutorial steps under "To push a single document" were straightforward.  After creating pushOneItem.py and typing "python pushOneItem.py" in the terminal, I received no errors unless one or more of your src_id, org_id, or api_key is invalid.

Once the required credentials are met, the python script runs.  However, when I few the Log Browser, I received an error.  After changing the source from secure to public in my Coveo dashboard, the new entry was successfully added to the employees' database.

In the end, it wasn't that I didn't understand the tutorial nor that my Python "add new record" was incorrect; I just encountered a few security permission issues along the way.  I hope to resolve later why the record didn't insert when using a secure source.