var m = require("mithril")

var EHR = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/ehrs",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            EHR.error = ""
            EHR.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            EHR.error = e.message
            EHR.list = []
        })
    },

    current: {},

//    close: function(clientKey) {
//        return m.request({
//            method: "POST",
//            url: "/api/claims/close",
//            data: Claim.current,
//            headers: {
//                'ClientKey': clientKey
//            },
//            useBody: true,
//        })
//        .then(function(items) {
//            EHR.error = ""
//        })
//        .catch(function(e) {
//            console.log(e)
//            EHR.error = e.message
//        })
//    },
//
//    update: function(clientKey) {
//        return m.request({
//            method: "POST",
//            url: "/api/claims/update",
//            data: Claim.current,
//            headers: {
//                'ClientKey': clientKey
//            },
//            useBody: true,
//        })
//        .then(function(items) {
//            Claim.error = ""
//        })
//        .catch(function(e) {
//            console.log(e)
//            Claim.error = e.message
//        })
//    },

    register: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/ehrs",
            data: EHR.current,
            headers: {
                'ClientKey': clientKey
            },
            useBody: true,
        })
        .then(function(items) {
            EHR.error = ""
        })
        .catch(function(e) {
            console.log(e)
            EHR.error = e.message
        })
    }
}

module.exports = EHR