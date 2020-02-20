var m = require("mithril")
var Investigator = require("../models/Investigator")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Investigator.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Investigator name]", {
                oninput: m.withAttr("value", function(value) {Investigator.current.name = value}),
                value: Investigator.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Investigator.error)
        ])
    }
}