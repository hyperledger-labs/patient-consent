var m = require("mithril")
var DataProvider = require("../models/DataProvider")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    DataProvider.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Data Provider name]", {
                oninput: m.withAttr("value", function(value) {DataProvider.current.name = value}),
                value: DataProvider.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", DataProvider.error)
        ])
    }
}