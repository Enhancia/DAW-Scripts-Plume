function RemoteControlHandler (cursorDevice, remoteControlsBank)
{
    this.cursorDevice = cursorDevice;
    this.remoteControlsBank = remoteControlsBank;

    var i;
    for (i = 0; i < this.remoteControlsBank.getParameterCount (); i++)
        this.remoteControlsBank.getParameter (i).name().markInterested ();

    this.cursorDevice.isEnabled ().markInterested ();
    this.cursorDevice.isWindowOpen ().markInterested ();
}

RemoteControlHandler.prototype.getName = function ()
{
    return "Device Mode";
}

RemoteControlHandler.prototype.setIndication = function (enable)
{
    var i;
    for (i = 0; i < this.remoteControlsBank.getParameterCount (); i++)
        this.remoteControlsBank.getParameter (i).setIndication (enable);
}

RemoteControlHandler.prototype.handleMidi = function (status, data1, data2)
{
        for (i = 0; i < this.remoteControlsBank.getParameterCount (); i++)
            println(this.remoteControlsBank.getParameter (i).name().get());

}