# Google Drivac

## HELP ARCHIVE TEAM!
**ARCHIVE TEAM NEEDS YOU!**

Help lend some processing power to crawl/download more Google Drive links.

For details please see https://datahorde.org/help-archive-team-archive-public-google-drive-files-before-september-13

## Vaccinate Against Link Rot!
On Sep 13 2021, Google Drive will forcibly private a lot of publicly shared URLs, details are available here:
https://workspaceupdates.googleblog.com/2021/06/drive-file-link-updates.html

Important Note: [Google Docs, Sheets, and Slides files are **not** impacted by this change](https://support.google.com/a/answer/10685032)

Luckily, if you access a shared link before that date, your Google account will be able to continue accessing it after the deadline. Google-Drivac is a tool to associate a Google account with a list of Google Drive links.

Install requirements with:
```bash
$pip install -r requirements.txt
```
Help:
```bash
$python gdrivac.py -h
```

### Acknowledgements:
[Pyxia](https://github.com/Pyxia-Code), author of [mf-dl](https://gitgud.io/Pyxia/mf-dl/-/blob/master/mfdl.py), which was a very good reference for gdrivac.
