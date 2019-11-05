var m = require("mithril")
var DataProvider = require("../models/DataProvider")

var qrcodeurl = ''

module.exports = {
    oninit:
        function(vnode){
            DataProvider.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
//        return m(".user-list", Clinic.list.map(function(clinic) {
//            return m("a.user-list-item", clinic.name) // + " " + clinic.permissions)
//        }),
//        m("label.error", Clinic.error))
        return m(".user-list", DataProvider.list.map(function(dataprovider) {
            return m("a.user-list-item", dataprovider.public_key + " " + dataprovider.name,
                    m("div"),
                    m("button", {
                        onclick: function() {
                            qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + dataprovider.public_key + '&chld=H|0'
                        }
                    }, 'Generate QR code for Hospital Public Key: ' + dataprovider.public_key)
                )
            }),
            m("div"),
            m("img", {src: qrcodeurl}),
            m("label.error", DataProvider.error))
    }
}