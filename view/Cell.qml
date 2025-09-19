// import QtQuick

// Item {
//     id: container
//     property alias cellColor: rectangle.color
//     signal clicked(cellColor: color)

//     width: 25; height: 25

//     Rectangle {
//         id: rectangle
//         border.color: "white"
//         anchors.fill: parent
//     }

//     MouseArea {
//         anchors.fill: parent
//         onClicked: container.clicked(container.cellColor)
//     }
// }

import QtQuick 2.15

Item {
    id: container
    property alias cellColor: rectangle.color
    property string gateType: ""  // "AND", "OR", "NOT", or "" for none
    signal clicked(cellColor: color)

    width: 25
    height: 25

    Rectangle {
        id: rectangle
        border.color: "white"
        anchors.fill: parent
        color: parent.cellColor
    }

    Canvas {
        anchors.fill: parent
        visible: container.gateType !== ""

        onPaint: {
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)
            ctx.strokeStyle = "black"
            ctx.lineWidth = 2

            if(container.gateType === "AND") {
                ctx.beginPath()
                ctx.rect(5, 5, 15, 15)
                ctx.arc(20, 12.5, 7.5, Math.PI/2, -Math.PI/2, true)
                ctx.stroke()
            } else if(container.gateType === "OR") {
                ctx.beginPath()
                ctx.moveTo(5, 5)
                ctx.bezierCurveTo(13, 2, 22, 12.5, 5, 22)
                ctx.lineTo(20, 22)
                ctx.stroke()
            } else if(container.gateType === "NOT") {
                ctx.beginPath()
                ctx.moveTo(5, 5)
                ctx.lineTo(23, 12.5)
                ctx.lineTo(5, 22)
                ctx.closePath()
                ctx.stroke()

                ctx.beginPath()
                ctx.arc(26, 12.5, 3, 0, 2 * Math.PI)
                ctx.stroke()
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: container.clicked(container.cellColor)
    }
}
