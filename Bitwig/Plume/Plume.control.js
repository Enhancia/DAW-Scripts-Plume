loadAPI(13);
load("RemoteControlHandler.js")

host.defineController("Enhancia", "Plume", "0.1", "daef111e-2042-4b33-a203-2b7e7b09e09a", "Enhancia");
host.defineMidiPorts(1,0)
function init() {
   //############################Script initialisation####################################
   host.getMidiInPort(0).setMidiCallback(onMidiPort1);
   noteIn = host.getMidiInPort(0).createNoteInput("Notes")
   noteIn.setShouldConsumeEvents(false)
   transport = host.createTransport();
   //############################Event if play button is press####################################
   transport.isPlaying().addValueObserver(function (value) {
      delayed()
   })
   //############################Event if record button is press####################################
   transport.isArrangerRecordEnabled().addValueObserver(function (value) {
      delayed()
   })
   //############################Get track list initialisation####################################
   cursorTrack = host.createCursorTrack("lid","Cursor Track",0,0,false)
   trackBank = host.createMainTrackBank(100,0,0)
   trackBank.followCursorTrack(cursorTrack)

   //############################TODO####################################
   trackTab = []
   cursorDeviceTab = []
   cursorRemoteControlsPagetab = []
   for (i=0;i<100;i++){
      //array of tracks
      trackTab.push(trackBank.getTrack(i))
      //array of cursorDevice
      cursorDeviceTab.push(trackTab[i].createCursorDevice("Primary"))
      //array of cursorRemoteCrontrolsPage
      cursorRemoteControlsPagetab.push(cursorDeviceTab[i].createCursorRemoteControlsPage(8))
   }
   trackTab.forEach(function (element) {
      element.arm().markInterested()
      element.trackType().markInterested()
   })
   specificPluginDevicetab = []
   parameterTab = []
   for (i=0; i< cursorDeviceTab.length;i++){
      cursorDeviceTab[i].name().markInterested()
      specificPluginDevicetab[i]  = cursorDeviceTab[i].createSpecificVst2Device(2)
      parameterTab[i] = specificPluginDevicetab[i].createParameter(0)
      parameterTab[i].name().markInterested()
   }

   //############################Start delayed function after 200 ms####################################
   host.scheduleTask(function() { delayed(); }, 200);
}

function delayed() {
   for (i=0;i<100;i++){
      if(cursorDeviceTab[i].name().get() !== "" && cursorDeviceTab[i].name().get()!==null){
         println("nom: "+cursorDeviceTab[i].name().get())
         println(trackTab[i].arm().get())
         println("type: "+trackTab[i].trackType().get())
         println("param"+parameterTab[i].name().get())
         println("param "+parameterTab[i].name().get())
      }
   }
}

//    tableau = []
//    paramtab = []
//    for(i=0; i<100;i++){
//       tableau.push(trackBank.getTrack(i).createCursorDevice("Primary"))
//       trackBank.getTrack(i).arm().markInterested()
//       trackBank.getTrack(i).trackType().markInterested()
//
//    }
//    tableau.forEach(function (elem){
//       elem.name().markInterested()
//       paramtab.push(elem.createCursorRemoteControlsPage(37));
//    })
//    for (i=0;i< paramtab.length;i++){
//       paramtab[i].pageNames().markInterested()
//    }
// }

   // for (i=0;i<tableau.length;i++){
   //    if(tableau[i].name().get() !== "" && tableau[i].name().get() !== null && tableau[i].name().get() == "Plume"){
   //       println("nom: "+tableau[i].name().get())
   //       println(trackBank.getTrack(i).arm().get())
   //       println("type: "+trackBank.getTrack(i).trackType().get())
   //       println(paramtab[i].pageNames().get().length)
   //    }
   //
   // }

function onMidiPort1(status, data1,data2) {
   remoteControlHandler .handleMidi(status, data1, data2)
}
function flush() {
}
function exit() {
}