import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import Style 1.0

Rectangle {
    property int vehicalMode: 0
    property int batteryPercentage: 10

    color: "#151515"
    Layout.preferredWidth: 270
    Layout.preferredHeight: 270
    radius: 15
    RowLayout {
        anchors.centerIn: parent
        spacing: 30

        ColumnLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 20

            Text {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                text: qsTr("Battery")
                font.pixelSize: 20
                font.weight: Font.Bold
                font.family: "Lato"
                color: Style.black40
            }

            Image {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                source: {
                    switch(vehicalMode){
                    case 0:
                        return "../icons/icon_battrey/BatteryIcon.svg";
                    case 1:
                        return "../icons/icon_battrey/BatteryIcon_sports.svg";
                    case 2:
                        return "../icons/icon_battrey/BatteryIcon_normal.svg";

                    default:
                        return "../icons/icon_battrey/BatteryIcon.svg";
                    }
                }

                Image {
                    visible: vehicalMode === 0 || vehicalMode === 1
                    source: {
                        switch(vehicalMode){
                        case 0:
                            return "../icons/icon_battrey/Eco Leaf Icon.svg";
                        case 1:
                            return "../icons/icon_battrey/Sport Flag Icon_battery.svg";
                        case 2:
                            return "";

                        default:
                            return "../icons/icon_battrey/Eco Leaf Icon.svg";
                        }
                    }
                    anchors.centerIn: parent
                }
            }


            Text {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                text: qsTr("%0 %").arg(batteryPercentage)
                font.pixelSize: 20
                font.weight: Font.Bold
                font.family: "Lato"
                color: {
                    switch(vehicalMode){
                    case 0:
                        return "#4EB93D";
                    case 1:
                        return "#00A3FF";
                    case 2:
                        return "#FFFFFF";

                    default:
                        return "#4EB93D";
                    }
                }
            }
            Timer {
            interval: 3000
            repeat: true
            running: true
            onTriggered: backend.get_soc()
        }


        }


        ColumnLayout {
            spacing: 10
            Layout.alignment: Qt.AlignHCenter

            Text {
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                text: qsTr("Est. Distance")
                font.pixelSize: 20
                font.weight: Font.Bold
                font.family: "Lato"
                color: "#FFFFFF"
            }
            Text {
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                text: qsTr("240 miles left")
                font.pixelSize: 14
                font.weight: Font.Bold
                font.family: "Lato"
                color: {
                    switch(vehicalMode){
                    case 0:
                        return "#4EB93D";
                    case 1:
                        return "#00A3FF";
                    case 2:
                        return "#FFFFFF";

                    default:
                        return "#4EB93D";
                    }
                }
            }

            Item {Layout.preferredHeight: 20}

            RowLayout {
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: qsTr("with")
                    font.pixelSize: 10
                    font.weight: Font.Light
                    font.family: "Lato"
                    color: "#FFFFFF"
                }

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text:{
                        switch(vehicalMode){
                        case 0:
                            return qsTr("Normal Mode:");
                        case 1:
                            return qsTr("Normal Mode:");
                        case 2:
                            return qsTr("Echo Mode:");

                        default:
                            return qsTr("Normal Mode:");
                        }
                    }

                    font.pixelSize: 10
                    font.weight: Font.Light
                    font.family: "Lato"
                    color: {
                        switch(vehicalMode){
                        case 0:
                            return "#FFFFFF";
                        case 1:
                            return "#FFFFFF";
                        case 2:
                            return "#4EB93D";

                        default:
                            return "#FFFFFF";
                        }
                    }
                }
            }

            Text {
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                text: qsTr("205 miles left")
                font.pixelSize: 14
                font.weight: Font.Bold
                font.family: "Lato"
                color: "#FFFFFF"
            }

            Item {Layout.preferredHeight: 5}

            RowLayout {
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                Text {
                    Layout.alignment: Qt.AlignLeft
                    text: qsTr("with")
                    font.pixelSize: 10
                    font.weight: Font.Light
                    font.family: "Lato"
                    color: "#FFFFFF"
                }

                Text {
                    Layout.alignment: Qt.AlignLeft
                    text:{
                        switch(vehicalMode){
                        case 0:
                            return qsTr("Sport Mode:");
                        case 1:
                            return qsTr("Echo Mode:");
                        case 2:
                            return qsTr("Sport Mode:");

                        default:
                            return qsTr("Sport Mode:");
                        }
                    }

                    font.pixelSize: 10
                    font.weight: Font.Light
                    font.family: "Lato"
                    color: {
                        switch(vehicalMode){
                        case 0:
                            return "#00A3FF";
                        case 1:
                            return "#4EB93D";
                        case 2:
                            return "#00A3FF";

                        default:
                            return "#00A3FF";
                        }
                    }
                }
            }

            Text {
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                text: qsTr("168 miles left")
                font.pixelSize: 14
                font.weight: Font.Bold
                font.family: "Lato"
                color: "#FFFFFF"
            }
        }
    }
    Connections {
        target: backend
        function onSoc_signal(value) {
            batteryPercentage = value
        }
    }

}
