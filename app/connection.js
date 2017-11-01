let request = require("request")

// JSON to be passed to the QPX Express API
let requestData = [{
    "product": "qemu",
    "version": "0.13.0"
}]

let url = "http://127.0.0.1:4242"

request({
    url: url + "/privileges",
    method: "POST",
    json: requestData
}, function (error, response, body) {
        if (!error && response.statusCode === 200) {
            console.log(body)
        } else {
            console.log("error: " + error)
            console.log("response.statusCode: " + response.statusCode)
            console.log("response.statusText: " + response.statusText)
        }
    }
);
