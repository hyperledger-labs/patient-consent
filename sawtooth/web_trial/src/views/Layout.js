var m = require("mithril")

module.exports = {

    view: function(vnode) {
        return m("main.layout", [
            m("nav.menu", [
                m("a", {href: "/investigator", oncreate: m.route.link}, "As Investigator|"),
            ]),
            m("section", vnode.children),
        ])
    }
}