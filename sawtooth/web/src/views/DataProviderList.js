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
            return m("a.user-list-item", "PUBLIC KEY: " + dataprovider.public_key + "; NAME: " + dataprovider.name,
                    m("div"),
                    m("button", {
                        onclick: function() {
                            qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + dataprovider.public_key + '&chld=H|0'
                        }
                    }, 'Generate QR code for Data Provider Public Key: ' + dataprovider.public_key),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            DataProvider.grant_access_to_share_data(dataprovider.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant Access To Share Data'),
                    m("div"),
                    m("button", {
                        onclick: function() {
                            DataProvider.revoke_access_to_share_data(dataprovider.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke Access To Share Data')
                )
            }),
            m("div"),
            m("img", {src: qrcodeurl}),
            m("label.error", DataProvider.error))
    }
}