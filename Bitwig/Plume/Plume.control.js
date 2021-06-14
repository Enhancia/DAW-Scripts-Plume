loadAPI(13);
host.defineController("Enhancia", "Plume", "0.1", "daef111e-2042-4b33-a203-2b7e7b09e09a", "Enhancia");
host.defineMidiPorts(0,0);
function init() {
   cursorTrack = host.createCursorTrack(0, 0)
   cursorTrack.arm().get()
   cursorDevice = cursorTrack.createCursorDevice()
   cursorDevice.name().get()
   Page = cursorDevice.createCursorRemoteControlsPage("nom", 8, '')
   var param = Page.getParameter(0)
   param.name().markInterested()
   println(param.name().get())
   var observer = cursorDevice.addDirectParameterValueDisplayObserver(200,function(){
     // println(id+nom)
   })
   //observer.setObservedParameterIds("track_arm")
   param.value().addValueObserver(128, function(newVal) {
      println('Param ' + 0 + ' of changed to = ' + newVal);
   });
}
//    //############################Get track list initialisation####################################
//    cursorTrack = host.createCursorTrack("lid","Cursor Track",0,0,false)
//    trackBank = host.createMainTrackBank(100,0,0)
//    trackBank.followCursorTrack(cursorTrack)
   
//    cursorTrack = host.createCursorTrack(0, 0)
//    cursorDevice = cursorTrack.createCursorDevice()
//    rcPage = cursorDevice.createCursorRemoteControlsPage("nom", 8, '')
//    param = rcPage.getParameter(0)
//    param.name().markInterested()
//    //#######################################TODO###################################################
//    track = trackBank.getTrack(0)
//    deviceBank = track.createDeviceBank(1)
//    device= deviceBank.getDevice(0)
//    device.name().markInterested()
//    device.isPlugin().markInterested()
//    //############################Start delayed function after 200 ms####################################
//    host.scheduleTask(function() {
//       delayed();
//    },200);
// }
// function delayed() {
//    println("nom"+param.name().get())
//    println("Name: "+device.name().get())
//    println("isPlugin: "+device.isPlugin().get())
   
// }
// //    tableau = []
// //    paramtab = []
// //    for(i=0; i<100;i++){
// //       tableau.push(trackBank.getTrack(i).createCursorDevice("Primary"))
// //       trackBank.getTrack(i).arm().markInterested()
// //       trackBank.getTrack(i).trackType().markInterested()
// //    }
// //    tableau.forEach(function (elem){
// //       elem.name().markInterested()
// //       paramtab.push(elem.createCursorRemoteControlsPage(37));
// //    })
// //    for (i=0;i< paramtab.length;i++){
// //       paramtab[i].pageNames().markInterested()
// //    }
// // }
// // for (i=0;i<tableau.length;i++){
// //    if(tableau[i].name().get() !== "" && tableau[i].name().get() !== null && tableau[i].name().get() == "Plume"){
// //       println("nom: "+tableau[i].name().get())
// //       println(trackBank.getTrack(i).arm().get())
// //       println("type: "+trackBank.getTrack(i).trackType().get())
// //       println(paramtab[i].pageNames().get().length)
// //    }}