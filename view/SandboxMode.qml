//import related modules
import QtQuick
import QtQuick.Controls

//window containing the application
ApplicationWindow {
    width: 640
    height: 480
    visible: true
    //title of the application
    title: "Hello World"

    //menu containing two menu items
    header: MenuBar {
        Menu {
            title: "&File"
            Action {
                text: "&Open..."
                onTriggered: console.log("Open action triggered")
            }
            MenuSeparator { }
            Action {
                text: "&Exit"
                onTriggered: Qt.quit()
            }
        }
    }

    //Content Area

    //a button in the middle of the content area
    /*Button {
        text: "Hello World"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }*/
    EditorGrid {}
    EditorSidebar {}
}