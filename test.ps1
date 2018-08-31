set-location "C:\Users\edl\johann\oo\openpose-1.3.0-win64-gpu-binaries"
#bin\OpenPoseDemo.exe --video examples\media\origin.mp4 --write_json snap\ --part_candidates --face  --model_pose COCO --write_video snap\snap.avi --keypoint_scale 4

$sourcevideo = "C:\Users\edl\johann\oo\openpose-1.3.0-win64-gpu-binaries\examples\media"

Get-ChildItem -Path $sourcevideo | ForEach-Object {
Write-Host $_.FullName 
$repertoirejson = " $($_.BaseName)\json"
Write-Host $repertoirejson -ForegroundColor green

New-Item -ItemType directory -Name $repertoirejson -Force #-WhatIf
bin\OpenPoseDemo.exe --video $_.Fullname --write_json "$repertoirejson" --write_video "$($_.BaseName)\$($_.BaseName).avi"  --part_candidates --face --keypoint_scale 4 

#echo $_ | gm 
}


