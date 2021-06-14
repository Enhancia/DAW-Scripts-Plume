#name=NeovaPlume
#the above line set the name of the script, it will be find in option=>Midi settings=>Controller Type

import playlist
import mixer
import channels
import plugins
import transport
import patterns
import device
import arrangement
import general
import launchMapPages
import ui
import sys
import midi
import utils
#the event that start the script (when the user interacte with almost everything)
def OnRefresh(flags):
    refreshAllPlumesTrackArmParameter()

#function that change is parameter "track_arm" of all plugin Plume (to 0 is it's not selected | to 1 if it is)
def refreshAllPlumesTrackArmParameter():
    trackArmId  = getTrackArmID()
    # loop over all channels (in the channel rack)
    for y in range(0,channels.channelCount()):
        #call getTrackArmId
        
        #call isPlume track to check if the current track of the loop is a Plume one
        if isPlumeTrack(y):
            #if the current channel in the loop is the one selected
            if channels.isChannelSelected(y):
                #change the plugin parameter value (value, track_arm id, channel id)
                plugins.setParamValue(1,trackArmId,y)
            else:
                plugins.setParamValue(0,trackArmId,y)

#get the id of the parameter call "track_arm" in the Plume channel
def getTrackArmID():
    #loop over all plugins (we take the channelCount because we can't know for sure how much plugin are initialized
    #but we can be sure that it's not more than the number of channel)
    for y in range(0,channels.channelCount()):
        #necessary check (or it display an error)
        if plugins.isValid(y):
            #if the name of the plugin is Plume
            if plugins.getPluginName(y) == "Plume":
                #loop over all the parameter of Plume
                for x in range(0,plugins.getParamCount(y)):
                    #if the parameter is call track_arm return it
                    if plugins.getParamName(x,y) == "track_arm":
                        return x
#check if the track is a Plume one
def isPlumeTrack(ID):
    PlumeTab = []
    for y in range(0,channels.channelCount()):
        try :
            if plugins.getPluginName(y) == "Plume":
                #if the plugin at the y indice is Plume add the indice to the array PlumeTab
                PlumeTab.append(y)
        except:
            pass
    try:
        #if we can find the ID passed in the function in the PlumeTab we return true, else we return false
        PlumeTab.index(ID)
        return True
    except:
        return False
        pass
