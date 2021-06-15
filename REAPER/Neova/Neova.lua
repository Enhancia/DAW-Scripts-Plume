function main()
 for i=0,reaper.GetNumTracks()-1 do
    --get the i track
    tr = reaper.GetTrack(0,i)
    ok,name=reaper.TrackFX_GetFXName(tr,0,"") --0=first FX name
    if name=='VSTi: Plume (Enhancia)' or name== "AUi: Plume (Enhancia)" then
    track_fxparam_count = reaper.TrackFX_GetNumParams(tr, 0) -- Get number of parameter in the tracks
      for k = 0, track_fxparam_count-1  do -- Loop over each parameter of this track
        buf = ""
        --get param name
        retval, buf = reaper.TrackFX_GetParamName( tr, 0, k, buf )
        if buf == 'track_arm' then
          trackArmParamIndex = k
          record = reaper.GetMediaTrackInfo_Value(tr,'I_RECARM')
          --record = 1 if track is armed and record = 0 if not
          if record == 1 then
            reaper.TrackFX_SetParam( tr,0,trackArmParamIndex , 1 )
            else
            reaper.TrackFX_SetParam( tr,0,trackArmParamIndex , 0 )
          end
        end
      end -- ENDLOOP through FX parameters 
    end  
  end
  --reaper.defer(main)
end

main()
