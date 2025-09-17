import QtQuick

Item {
    id: container
    property alias cellColor: rectangle.color
    signal clicked(cellColor: color)

    width: 25; height: 25

    Rectangle {
        id: rectangle
        border.color: "white"
        anchors.fill: parent
    }

    MouseArea {
        anchors.fill: parent
        onClicked: container.clicked(container.cellColor)
    }
}