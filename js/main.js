

(function () {
    "use strict";

    var app = WinJS.Application;
    var activation = Windows.ApplicationModel.Activation;
    var isFirstActivation = true;

    app.onactivated = function (args) {
        if (args.detail.kind === activation.ActivationKind.voiceCommand) {
            
        }
        else if (args.detail.kind === activation.ActivationKind.launch) {
            
            if (args.detail.arguments) {
                
            }
            else if (args.detail.previousExecutionState === activation.ApplicationExecutionState.terminated) {
                
            }
        }

        if (!args.detail.prelaunchActivated) {

        }

        if (isFirstActivation) {
            
            document.addEventListener("visibilitychange", onVisibilityChanged);
            args.setPromise(WinJS.UI.processAll());

            window.setLaunchScreen();
            Ads.initAds();
            //IntersititialAds.SetupAds();

            document.getElementById("webview").addEventListener("MSWebViewScriptNotify", LevelComplete);
        }

        isFirstActivation = false;
    };

    function onVisibilityChanged(args) {
        if (!document.hidden) {
            
        }
    }

    app.oncheckpoint = function (args) {
        
    };

    app.start();

})();



function setLaunchScreen() {
    var ViewManagement = Windows.UI.ViewManagement;
    var ApplicationView = ViewManagement.ApplicationView;

    var normalWidth = 1000;
    var normalHeight = 600;

    var view = ApplicationView.getForCurrentView();
    if (view.tryEnterFullScreenMode()) {
        WinJS.log && WinJS.log("Entering full screen mode", "samples", "status");
        // The resize event will be raised when the entry to full screen mode is complete.
    } else {
        WinJS.log && WinJS.log("Failed to enter full screen mode", "samples", "error");

        var info = Windows.Graphics.Display.DisplayInformation.getForCurrentView();
        ApplicationView.preferredLaunchViewSize = { width: info.screenWidthInRawPixels, height: info.screenHeightInRawPixels };
        ApplicationView.preferredLaunchWindowingMode = Windows.UI.ViewManagement.ApplicationViewWindowingMode.preferredLaunchViewSize;
    }


}

function setScreenSize() {

    var ViewManagement = Windows.UI.ViewManagement;
    var ApplicationView = ViewManagement.ApplicationView;
    var normalWidth = 1260;
    var normalHeight = 600;

    var info = Windows.Graphics.Display.DisplayInformation.getForCurrentView();

    var view = ApplicationView.getForCurrentView();
    var t = view && view.tryResizeView({ width: normalWidth, height: normalHeight });
}


function LevelComplete(e) {
    // When a ScriptNotify event is received, append a message to outputArea to indicate that fact
    switch (e.value) {
        case "Resize":
            setScreenSize();
            break;
        case "Rate":
            showRate();
            break;
        case "OpenMoreGames":
            OpenMoreGames();
            break;
        case "Purchanse":
            DoPurchanse();
            break;
        case "showIntersititialAd":
            IntersititialAds.requestAdHandler();
            break;
        case "loadIntersititialAd":
            IntersititialAds.loadAd();
            break;
        case "ShowAds":
            ShowAds();
            break;
        default:
            break;

    }
}



function DoPurchanse() {

    var storeContext = Windows.Services.Store.StoreContext.getDefault();
    var storeId = "9n53s0cnc5xh";


    storeContext.requestPurchaseAsync(storeId).done(function (result) {
        if (result.extendedError === (0x803f6107 | 0)) {
            //SdkSample.reportExtendedError(result.extendedError);
            return;
        }

        switch (result.status) {
            case StorePurchaseStatus.alreadyPurchased:
                WinJS.log && WinJS.log("You already bought this AddOn.", "samples", "error");
                break;

            case StorePurchaseStatus.succeeded:
                WinJS.log && WinJS.log("You bought " + item.title, "samples", "status");
                break;

            case StorePurchaseStatus.notPurchased:
                WinJS.log && WinJS.log("Product was not purchased, it may have been canceled.", "samples", "error");
                break;

            case StorePurchaseStatus.networkError:
                WinJS.log && WinJS.log("Product was not purchased due to a network error.", "samples", "error");
                break;

            case StorePurchaseStatus.serverError:
                WinJS.log && WinJS.log("Product was not purchased due to a server error.", "samples", "error");
                break;

            default:
                WinJS.log && WinJS.log("Product was not purchased due to an unknown error.", "samples", "error");
                break;
        }

    });
}

function showRate() {
    var isRate = null;
    try {
        var e = window.localStorage;
        isRate = e.getItem("9n53s0cnc5xh:isRate");
    } catch (t) { }

    if (isRate == null) isRate = "0";
    if (isRate == "0") {
        var msg = "Thanks for playing!Please take the time to rate the app!";
        var msgGoBtn = "Go to rate";
        var msgCancel = "Cancel";

        var msgdlg = new Windows.UI.Popups.MessageDialog(msg);
        if (msgdlg) {

            msgdlg.defaultCommandIndex = 0;
            msgdlg.cancelCommandIndex = 1;

            msgdlg.commands.append(new Windows.UI.Popups.UICommand(msgGoBtn, function () {
                var url = new Windows.Foundation.Uri("ms-windows-store://review/?ProductId=9n53s0cnc5xh");
                Windows.System.Launcher.launchUriAsync(url);

                try {
                    var e = window.localStorage;
                    e.setItem("9n53s0cnc5xh:isRate", "1");
                } catch (t) { }
            }));

            msgdlg.commands.append(new Windows.UI.Popups.UICommand(msgCancel, function () {

            }.bind(this)));

            msgdlg.showAsync();
        }
    }
}

function OpenMoreGames() {
    var url = new Windows.Foundation.Uri("ms-windows-store://publisher/?name=EngleSoft");
    Windows.System.Launcher.launchUriAsync(url);
}

var cntAdsShow = 0;

function ShowAds() {
    /*if (cntAdsShow > 0) {
        if (cntAdsShow % 2 == 0) {
            showRate();
            //IntersititialAds.loadAd();
        } else {
           
            IntersititialAds.requestAdHandler();
        }
    }

    ++cntAdsShow;*/
    IntersititialAds.requestAdHandler();
}