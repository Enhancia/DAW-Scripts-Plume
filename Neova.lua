function main()
 for i=0,reaper.GetNumTracks()-1 do
 reaper.ClearConsole()
    count =0
    --get the i track
    tr = reaper.GetTrack(0,i)
    track_fxparam_count = reaper.TrackFX_GetNumParams(tr, 0) -- Get number of fx in track
   
    for k = 0, track_fxparam_count-1  do -- Loop over each parameter of this track
      buf = ""
      retval, buf = reaper.TrackFX_GetParamName( tr, 0, k, buf ) 
      
      --check is the selected track have the 5 parameter plume is suppose to have
      if buf == 'track_arm' then
        track_arm_param_id =  k
      end
      if buf == 'vibrato_value' or buf == 'vibrato_intensity' or buf == 'tilt_value' or buf == 'roll_value' or buf == 'track_arm' then
        --in witch case with increment count up to 5 because we check 5 parameter
        count = count+1
      end
      --if the 5 parameter are here, we can be sure it's the good track so we save the ID in a global
      if count  ==  5 then
      
      
      end
    end
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
  reaper.defer(main)
end

main()
