var m = require("mithril")

var InvestigatorList = require("./views/InvestigatorList")
var InvestigatorForm = require("./views/InvestigatorForm")
var TrialDataList = require("./views/TrialDataList")
var PreScreeningCheckForm = require("./views/PreScreeningCheck")
var InvestigatorActionsList = require("./views/InvestigatorActionsList")
var Layout = require("./views/Layout")

m.route(document.body, "/investigator", {

    "/investigator_list/": {
        render: function(vnode) {
            return m(Layout, m(InvestigatorList, vnode.attrs))
        }
    },
    "/investigator/new/": {
        render: function() {
            return m(Layout, m(InvestigatorForm))
        }
    },
    "/trial_data_list": {
        render: function(vnode) {
            return m(Layout, m(TrialDataList, vnode.attrs))
        }
    },
    "/pre_screening_check": {
        render: function(vnode) {
            return m(Layout, m(PreScreeningCheckForm, vnode.attrs))
        }
    },
    "/investigator": {
        render: function() {
            return m(Layout, m(InvestigatorActionsList))
        }
    },
})