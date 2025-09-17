import QtQuick

Rectangle {
    id: editorGrid
    width: 640; height: 640
    color: "lightgray"

    Grid {
        id: colorPicker
        rows: 16; columns: 16

        Repeater {
            model: 256
            Rectangle {
                width: 40; height: 40
                color: "white"
                border.color: "black"
                border.width: 1
            }
        }

    }
}