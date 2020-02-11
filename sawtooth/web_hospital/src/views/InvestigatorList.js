var m = require("mithril")
var Investigator = require("../models/Investigator")

var qrcodeurl = ''

module.exports = {
    oninit:
        function(vnode){
            Investigator.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
//        return m(".user-list", Clinic.list.map(function(clinic) {
//            return m("a.user-list-item", clinic.name) // + " " + clinic.permissions)
//        }),
//        m("label.error", Clinic.error))
        return m(".user-list", Investigator.list.map(function(investigator) {
            return m("a.user-list-item", "PUBLIC KEY: " + investigator.public_key + "; NAME: " + investigator.name,
                    m("div"),
//                    m("button", {
//                        onclick: function() {
//                            qrcodeurl='https://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=' + investigator.public_key + '&chld=H|0'
//                        }
//                    }, 'Generate QR code for Investigator Public Key: ' + investigator.public_key),
//                    m("div"),
                    m("button", {
                        onclick: function() {
                            Investigator.grant_investigator_access(investigator.public_key, vnode.attrs.client_key)
                        }
                    }, 'Grant Process Data Access'),
                    m("div"), 
                    m("button", {
                        onclick: function() {
                            Investigator.revoke_investigator_access(investigator.public_key, vnode.attrs.client_key)
                        }
                    }, 'Revoke Process Data Access')
                )
            }),
            m("div"),
            m("img", {src: qrcodeurl}),
            m("label.error", Investigator.error))
    }
}