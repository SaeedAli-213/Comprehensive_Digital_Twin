import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import Style 1.0
// import QtGraphicalEffects 1.15
import Qt5Compat.GraphicalEffects

Popup {
    signal openCamera
    signal openBattary
    signal openCarSetting
    signal openSpeedshow
    width: 1104
    height: 445
    background: Rectangle {
        anchors.fill: parent
        radius: 9
        color: Style.alphaColor(Style.black, 0.8)
    }

    contentItem: ColumnLayout {
        spacing: 8
        anchors.fill: parent
        RowLayout {
            Layout.leftMargin: 24
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            spacing: 24
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/front-defrost.svg"
                text: "Front Defrost"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/rear-defrost.svg"
                text: "Rear Defrost"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/seat.svg"
                text: "Left Seat"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/steering-wheel-warmer.svg"
                text: "Heated Steering"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/wiper.svg"
                text: "Wipers"
            }
        }

        Rectangle {
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            width: parent.width - 48
            height: 1
            color: Style.black30
        }

        RowLayout {

            Layout.leftMargin: 24
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            spacing: 24
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/dashcam.svg"
                onClicked: openCamera()
                text: "Dashcam"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/calendar.svg"
                text: "Calendar"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/messages.svg"
                text: "Messages"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/zoom.svg"
                text: "Zoom"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/video.svg"
                text: "Theater"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/toybox.svg"
                text: "Toybox"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/spotify.svg"
                text: "Spotify"
            }
        }

        RowLayout {
            Layout.leftMargin: 24
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            spacing: 24
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/caraoke.svg"
                text: "Caraoke"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/tunein.svg"
                text: "TuneIn"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/radio.svg"
                text: "Music"
            }
            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/battery1.svg"
                text: "Battary"
                onClicked: openBattary()
            }

            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/icon_battrey/Car Settings Icon.svg"
                text: "Car Setting"
                onClicked: openCarSetting()
            }

            LauncherButton {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                icon.source: "../icons/app_icons/cruise control.svg"
                text: "Speed Show"
                onClicked: openSpeedshow()
            }
        }
    }
}
