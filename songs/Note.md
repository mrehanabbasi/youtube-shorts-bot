Make sure to name your songs as follows: audio1.mp3/audio2.mp3/audio3.mp3...

Use the following script in PowerShell to rename the files:
```PowerShell
Get-ChildItem *.mp3 | ForEach-Object -begin { $count=1 } -process { rename-item $_ -NewName "audio$count.mp3"; $count++ }
```
