var m = require("mithril")
var Clinic = require("../models/Hospital")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Hospital.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Hospital name]", {
                oninput: m.withAttr("value", function(value) {Hospital.current.name = value}),
                value: Hospital.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Hospital.error)
        ])
    }
}