import QtQuick

Rectangle {
    id: editorSidebar
    width: 200; height: 640
    color: "lightgray"

    Grid {
        id: sidebarComponentsGrid
        rows: 8; columns: 3
        anchors.centerIn: parent
        spacing: 10
        Repeater {
            model: 24
            Rectangle {
                width: 50; height: 50
                color: "white"
                border.color: "black"
                border.width: 1
            }
        }
    }
}
