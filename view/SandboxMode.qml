import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    width: 300
    height: 200
    visible: true
    title: "Sandbox Mode"

    ColumnLayout {
        anchors.fill: parent

        Text {
            id: textLabel
            text: greetingsModel.text
            Layout.alignment: Qt.AlignHCenter
        }

        Button {
            text: "Click me"
            Layout.alignment: Qt.AlignHCenter
            onClicked: greetingsModel.random_greeting()
        }
    }
}
