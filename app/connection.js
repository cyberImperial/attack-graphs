const jquery = require("jquery");
const host = "http://127.0.0.1:4242";

jquery.ajax({
  type: "POST",
  data: [{
    "product" : "qemu",
    "version" : "0.13.0"
  }],
  dataType: 'json',
  url: host + "/privileges",
  success: function (data) {
    console.log(data);
  }
});
