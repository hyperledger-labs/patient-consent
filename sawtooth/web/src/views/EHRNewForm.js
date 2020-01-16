var m = require("mithril")
var EHR = require("../models/EHR")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function(vnode) {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    EHR.register(vnode.attrs.client_key)
                }
            }, [
            m("label.label", "Patient pkey"),
            m("input.input[type=text][placeholder=Patient pkey]", {
                oninput: m.withAttr("value", function(value) {EHR.current.patient_pkey = value}),
                value: EHR.current.patient_pkey
            }),
            m("label.label", "id"),
            m("input.input[placeholder=id]", {
                oninput: m.withAttr("value", function(value) {EHR.current.id = value}),
                value: EHR.current.id
            }),
            m("label.label", "Field 1"),
            m("input.input[placeholder=Field 1]", {
                oninput: m.withAttr("value", function(value) {EHR.current.field_1 = value}),
                value: EHR.current.field_1
            }),
            m("label.label", "Field 2"),
            m("input.input[placeholder=Field 2]", {
                oninput: m.withAttr("value", function(value) {EHR.current.field_2 = value}),
                value: EHR.current.field_2
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", EHR.error)
        ])
    }
}