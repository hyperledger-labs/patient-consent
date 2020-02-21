var m = require("mithril")

var EHR = {
    list: [],
    sharedDataList: [],
    error: "",
//    loadList: function(clientKey) {
//        return m.request({
//            method: "GET",
//            url: "/api/ehrs",
//            headers: {
//                'ClientKey': clientKey
//            }
//        })
//        .then(function(result) {
//            EHR.error = ""
//            EHR.list = result.data
//        })
//        .catch(function(e) {
//            console.log(e)
//            EHR.error = e.message
//            EHR.list = []
//        })
//    },

    screening_data: function(investigatorPKey, inclExclCriteria) {   //i.e Investigator
        return m.request({
            method: "GET",
            url: "/api/pre_screening_data?" + inclExclCriteria,
            headers: {
                'ClientKey': investigatorPKey
            }
        })
        .then(function(result) {
            console.log("Get Pre-screening data")
            EHR.error = ""
            EHR.sharedDataList = result.data
        })
        .catch(function(e) {
            console.log(e)
            EHR.error = e.message
            EHR.sharedDataList = []
        })
    },

    current: {}

}

module.exports = EHR