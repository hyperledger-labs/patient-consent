var m = require("mithril")
var Client = require("../models/Client")

module.exports = {

    oninit: //Client.loadList
        function(vnode){
            Client.loadList()
//            vnode.attrs.client_pkey = Client.list['clinic']
        }
    ,
    view: function(vnode) {
        return m(".user-list", [
            m("label.label", "Client public key"),
            m("input.input[type=text][placeholder=Client public key][disabled=false]", {
                value: Client.list['investigator'] //vnode.attrs.client_pkey
            }),
            m("a.user-list-item", {href: "/investigator/new/", oncreate: m.route.link}, "New Investigator"),
            m("a.user-list-item", {href: "/investigator_list/?client_key=" + Client.list['investigator'], oncreate: m.route.link}, "Investigator List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/pre_screening_check/?client_key=" + Client.list['investigator'], oncreate: m.route.link}, "Pre-Screening Check"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/trial_data_list/?client_key=" + Client.list['investigator'], oncreate: m.route.link}, "Trial Data List"),
        ])

    }
}