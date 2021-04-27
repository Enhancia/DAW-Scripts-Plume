function main()
reaper.ClearConsole()
--loop for all the tracks
  getPlumeGUID()
  for i=0,reaper.GetNumTracks()-1 do
    --get the i track
    tr = reaper.GetTrack(0,i)
    --detect if this track is plume
    if reaper.GetTrackGUID(tr) == plumeGUID then
       --get track name
       nothing,name = reaper.GetTrackName(tr)
       track_fxparam_count = reaper.TrackFX_GetNumParams(tr, 0) -- Get number of parameter in the tracks
       for k = 0, track_fxparam_count-1  do -- Loop over each parameter of this track
          buf = ""
          --get parame name
          retval, buf = reaper.TrackFX_GetParamName( tr, 0, k, buf )
        
          if buf == 'track_arm' then
             trackArmParamIndex = k
             record = reaper.GetMediaTrackInfo_Value(tr,'I_RECARM')
             --record = 1 if track is armed and record = 0 if not
             if record == 1 then
                reaper.TrackFX_SetParam( tr,0,trackArmParamIndex , 0.5 )
                else
                reaper.TrackFX_SetParam( tr,0,trackArmParamIndex , 0 )
             end
           end
        end -- ENDLOOP through FX parameters
     end
  end 
  --call back to this function after 33ms and create a loop
  --comment this line and save to cut this loop
  reaper.defer(main)
end

--Function that detect if plume is added to the current project, if yes :  store plume ID in plumeGUID
function getPlumeGUID()

  for i=0,reaper.GetNumTracks()-1 do
    count =0
    --get the i track
    tr = reaper.GetTrack(0,i)
    track_fxparam_count = reaper.TrackFX_GetNumParams(tr, 0) -- Get number of fx in track
    for k = 0, track_fxparam_count-1  do -- Loop over each parameter of this track
      buf = ""
      retval, buf = reaper.TrackFX_GetParamName( tr, 0, k, buf )
      --check is the selected track have the 5 parameter plume is suppose to have
      if buf == 'vibrato_value' or buf == 'vibrato_intensity' or buf == 'tilt_value' or buf == 'roll_value' or buf == 'track_arm' then
        --in witch case with increment count up to 5 because we check 5 parameter
        count = count+1
      end
      --if the 5 parameter are here, we can be sure it's the good track so we save the ID in a global
      if count  ==  5 then
        plumeGUID = reaper.GetTrackGUID(tr)
      end
    end
  end
end

main()
